# Ingestion and Upload Limits

Telebugs applies fixed safety limits to each new error report, envelope, artifact,
and artifact bundle. These boundaries keep memory, CPU, disk, SQLite, and the job
queue predictable on a small self-hosted server.

The limits are per object, not account quotas. They do not restrict how many
projects, releases, or error reports you can keep. They are intentionally not
configurable: an operator cannot accidentally remove the safety boundary while
trying to fix an unrelated capacity problem.

## Event Requests

Telebugs accepts uncompressed requests and requests using `gzip` or
zlib-wrapped `deflate`. Encoding names are case-insensitive. Brotli, Zstandard,
and requests with more than one content encoding are not supported.

| Object | Limit |
| --- | ---: |
| Request body before decompression | 16 MiB |
| Request body after decompression | 16 MiB |
| Envelope or item header line | 8 KiB |
| Items in one envelope | 16 |
| Event items in one envelope | 1 |
| Event JSON | 1 MiB |
| Minidump items in one envelope | 1 |
| Retained minidump | 12 MiB |
| JSON nesting | 64 levels |
| JSON key | 1 KiB |
| General string value | 64 KiB |
| Indexed or displayed string value | 8 KiB |

Telebugs rejects a request before durable acceptance when its wire or decoded
body, framing, JSON, or binary item cannot be handled safely. A valid envelope
with no supported event is acknowledged but is not added to the processing
queue. An empty request body remains a successful no-op.

### Occurrence Identity and Duplicate Deliveries

Telebugs calls this value the occurrence ID. In Sentry-compatible ingestion it
is the `event_id` from the envelope header, falling back to the event payload
when the header does not provide one. Telebugs accepts a 32-character
hexadecimal ID or a standard hyphenated UUID and stores the value as 32
lowercase hexadecimal characters. If neither location provides an ID,
Telebugs generates a UUIDv4 when it accepts the report. A present but malformed
`event_id` is rejected with `400 Bad Request` and
`X-Sentry-Error: invalid_event_id` before the request enters the durable ingest
queue.

A successfully accepted report returns `200 OK` with its canonical occurrence
ID:

```json
{"id":"69b345eb156342a496e5880afee01452"}
```

Occurrence IDs are unique within one project. Delivering the same ID again to that
project does not create another report, increment occurrence totals, send
another notification, or retain another minidump. If duplicate deliveries
contain different data, the first payload successfully persisted by Telebugs
wins. The same ID may be used independently by different projects.

## Event Details Retained

Large but valid event collections are handled differently from an oversized
request. Telebugs accepts the event and deterministically keeps the most useful
subset:

| Collection | Retained |
| --- | ---: |
| Exceptions | 32: first 16 and last 16 |
| Threads | 64, prioritizing crashed and current threads |
| Frames in one stack trace | 200: first 100 and last 100 |
| Frames across the event | 1,000 |
| Breadcrumbs | Most recent 100 |
| Tags | First 100 |
| Contexts | First 50 |
| Additional data entries | First 100 |
| Modules or dependencies | First 500 |
| Debug images | First 500 |
| Persisted event-detail rows | 2,500 |

Tag keys are limited to 200 bytes and tag values to 2 KiB. Telebugs preserves
the input order of retained entries and shortens strings only at valid UTF-8
boundaries. Grouping and persistence use the same normalized event, so sending
the same oversized event repeatedly still produces stable grouping.

### Ingestion Warning

When Telebugs shortens strings or leaves collection entries out, the report
page shows an **Ingestion warning** above the report details. The warning means
the error was accepted, but some diagnostic detail exceeded a safety boundary.
It names the affected sections and shows how many entries were omitted or
strings were shortened.

The same bounded summary is included when you use **View as**:

- JSON: `details.ingest_truncations`
- XML: `<ingest_truncations>`
- Markdown: an **Ingestion warning** section

The warning does not indicate a broken SDK or failed report. If the omitted
details are important, reduce noisy breadcrumbs, repeated frames, oversized
custom context, or other high-volume event data at the SDK.

## Pending Event Queue

Telebugs pauses new event intake when pending decoded payloads reach **512
MiB**, even if the configurable queued-error count check is disabled. The
existing queued-error count limit remains configurable and defaults to 10,000.

Open **Instance** > **Ingest Protection** to see:

- queued errors;
- queued payload bytes;
- the fixed queued-byte ceiling;
- bounded-ingest rejections in the last hour;
- truncated events in the last hour.

The queued-byte ceiling is read-only. It bounds memory, disk, and drain-time
exposure without adding another setting that operators must tune.

## Artifact and Source Map Uploads

The following limits apply to new release artifacts, source maps, chunks, and
ZIP bundles:

| Object | Limit |
| --- | ---: |
| Direct or UI multipart request | 64 MiB |
| Files in one UI release upload | 32 |
| Artifact file or ZIP entry | 32 MiB |
| Chunk | 8 MiB |
| Chunk request | 10 MiB and one chunk |
| Chunks in one bundle | 8 |
| Bundle assembly request | 1 MiB |
| Compressed bundle | 64 MiB |
| Expanded bundle | 128 MiB |
| ZIP entries, including directories and ignored metadata | 2,000 |
| Bundle manifest | 1 MiB |
| Compression ratio | 100:1 |
| Artifact logical name or path | 1,024 bytes |
| Stored filename | 255 bytes |
| Staged incomplete chunks across the instance | 1 GiB |
| Incomplete chunk lifetime | 24 hours |
| Bundle assembly scratch space | 384 MiB above the configured free-disk floor |

Telebugs counts ZIP entries and expanded bytes while reading them instead of
trusting archive metadata. It rejects path traversal, absolute paths,
backslashes, invalid UTF-8, NUL bytes, duplicate paths, ambiguous manifest
matches, encrypted entries, links, devices, CRC errors, and inconsistent size
metadata. A ZIP file stored inside a bundle is ordinary artifact content; it is
not recursively expanded.

Existing stored artifacts remain readable even when they are larger than a new
upload limit.

### Reuploads and Conflicts

Uploading identical bytes to the same artifact name and release is idempotent.
Telebugs returns the existing artifact instead of storing a duplicate.

Uploading different bytes to an existing name in the same release returns
`409 Conflict`. An artifact-bundle conflict aborts the entire bundle, so a
release is never left half-updated. Delete the incorrect artifact deliberately
or publish the new content under the correct release version.

Modern Sentry CLI clients use artifact bundles. Legacy 2.x clients can use the
direct release-file API. Telebugs has compatibility coverage for both Sentry CLI
2.58.6 and 3.6.2. See [Source Maps](release-01-source-maps.md) for setup and
upload commands.

## HTTP Responses and Retries

| Status | Meaning | What the sender should do |
| --- | --- | --- |
| `200 OK` | Report accepted into the durable ingest queue; response JSON contains its occurrence ID | No retry needed |
| `400 Bad Request` | Malformed occurrence ID (`event_id`), compression, envelope, JSON, checksum, archive, manifest, or path | Fix the payload; do not retry it unchanged |
| `409 Conflict` | An artifact name already contains different bytes in that release | Correct the release or artifact; do not retry unchanged |
| `413 Content Too Large` | A byte, depth, item, file, entry, or expansion boundary was exceeded | Reduce the object; do not retry it unchanged |
| `415 Unsupported Media Type` | Unsupported or multiple content encodings | Send an uncompressed, gzip, or deflate request |
| `429 Too Many Requests` | Temporary rate, queue, staged-byte, or disk pressure | Retry after the advertised delay |
| `5xx` | Temporary server or storage failure | Retry with normal SDK backoff |

Permanent event-ingestion failures include an `X-Sentry-Error` reason and no
retry header. A `429` response includes `Retry-After` and
`X-Sentry-Rate-Limits`. Sentry SDKs should drop permanent `400`, `413`, and
`415` responses, while retrying `429` and transient `5xx` responses.

## Troubleshooting

- For repeated `413` responses, reduce one event, attachment, minidump, source
  map, artifact, or archive. Retrying identical bytes cannot succeed.
- For `415`, remove multiple encodings or use identity, gzip, or deflate.
- For `429`, check **Instance** > **Ingest Protection**. Let the queue drain,
  restore free disk space, or wait for the rate window before retrying.
- For artifact `409`, verify the release version and artifact name. Do not
  overwrite a source map from an already-published release accidentally.
- If queued payload bytes remain high, inspect the Jobs dashboard and
  SQLite/Active Storage errors before increasing worker concurrency.
- If bundle assembly reports disk pressure, restore at least the configured
  free-disk floor plus 384 MiB of scratch space.

These fixed limits are safety boundaries for individual objects. Use retention
policies and ingest protection for long-term storage and traffic management.
