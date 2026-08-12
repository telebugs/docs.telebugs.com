# Source Maps

Source maps allow Telebugs to resolve minified JavaScript and TypeScript stack
traces back to the original source code. This makes errors from production
builds readable, showing the real files, line numbers, and context instead of
the bundled or minified versions.

Telebugs supports two source map workflows:

- **Uploaded source maps** are attached to a release. This is the recommended
  workflow for private maps, deterministic deploys, and the most reliable
  debugging experience.
- **Hosted source map discovery** retrieves maps that your asset server already
  makes anonymously available over public HTTPS. This workflow is optional and
  must be authorized for each exact origin by an instance admin.

## Understanding Source Maps

Source maps are files created by bundlers such as Webpack, Vite, and Rollup.
They map minified or transpiled code back to the original source files.

Without source maps, stack traces point to generated bundles. With a matching
map, Telebugs can show original filenames, line and column numbers, function
names, and code from `sourcesContent` when the map contains it.

Enable source map output in your bundler configuration, for example
`devtool: 'source-map'` in Webpack or `sourcemap: true` in Vite.

## Integrating Source Maps with Releases

Uploaded source maps are attached to a specific release so they apply only to
errors from that version. Releases remain the recommended choice when maps are
private, when asset URLs are reused between deploys, or when your production
asset server should not publish `.map` files.

Access releases from the project dashboard through the **Releases (N)** link
in the top-right (see [Individual Project View][1]). Create the release first
(see [Releases][2]), then upload the generated files and maps to it.

An uploaded artifact always takes precedence over hosted discovery. Telebugs
does not make a hosted request when an uploaded map resolves the report.

## Uploading Source Maps

You can upload source maps manually in the UI or automatically with Sentry CLI.
Telebugs supports legacy direct uploads and modern artifact bundles, with
compatibility coverage for Sentry CLI 2.58.6 and 3.6.2.

### Manual Upload

1. Open the desired release in the releases list.
2. Click **Attach artifacts** or drag and drop files.
3. Select the generated files and `.map` files, then upload them. Multiple files
   are supported.

### Automated Upload (Recommended)

1. Get your personal API key from **Account Settings → API access**. It starts
   with `tlbgs_`.
2. Set these environment variables:

   ```bash
   export SENTRY_URL=https://your-telebugs-instance.com
   export SENTRY_AUTH_TOKEN=tlbgs_your-api-key-here
   export SENTRY_PROJECT=your-project-id
   export SENTRY_ORG=unused # Required for compatibility; the value is ignored
   ```

3. Upload source maps:

   ```sh
   sentry-cli sourcemaps upload --release=v1.2.3 ./path/to/maps
   ```

4. If your build does not already reference the source maps, inject the
   references first:

   ```sh
   sentry-cli sourcemaps inject ./dist
   sentry-cli sourcemaps upload --release=v1.2.3 ./dist
   ```

New reports from that release use the uploaded maps automatically. Uploading
artifacts to an existing release also retries unresolved historical reports
that identify that release.

Uploads are subject to Telebugs' fixed [Ingestion and Upload Limits][3].
Reuploading identical bytes to the same release and artifact name is safe and
does not create a duplicate. Different bytes at an existing name return `409
Conflict`; use the correct release or deliberately delete the incorrect
artifact.

## Hosted Source Map Discovery

Hosted discovery is useful when your generated JavaScript and `.map` files are
already public. It does not publish, proxy, or expose a source map. It only lets
your Telebugs server retrieve an asset that an unauthenticated internet client
could already retrieve.

Do not make a private map public just to use this feature. Keep private or
protected maps private and use the upload workflow instead.

### Configure Hosted Discovery

Only an instance admin can authorize an origin:

1. Open the project, then select **Project Settings → Hosted source maps**.
2. Enter an exact origin such as `https://assets.example.com`.
3. Select **Authorize origin**.
4. Trigger a new production error and check its **Source map** status.

An origin consists only of `https://`, an ASCII hostname, and an optional
non-standard port. These are valid examples:

```text
https://assets.example.com
https://assets.example.com:8443
```

Wildcards, IP addresses, paths, queries, fragments, usernames, passwords, and
plain HTTP are rejected. For example, `https://*.example.com`,
`https://assets.example.com/maps`, and `https://127.0.0.1` are not accepted.

Authorize every origin that Telebugs must contact. If the generated bundle is
on `https://assets.example.com` but its map points to
`https://maps.example.net/app.js.map`, add both exact origins.

Removing an origin immediately prevents new hosted resolutions and removes
cached maps associated with it. Work already queued rechecks authorization
before applying or storing a map. Reports that were resolved earlier retain
their stored remapped frames.

The instance-wide emergency switch is under **Instance → Hosted source maps**.
Turning it off disables network discovery and use of hosted-map caches across
all projects. Uploaded release artifacts continue to work.

### Discovery Order and Behavior

For a new JavaScript report, Telebugs uses this order:

1. A matching uploaded release or debug-ID artifact.
2. A fresh authorized hosted-map cache entry.
3. Cold hosted discovery.

Cold discovery considers at most two distinct top in-app JavaScript bundle
URLs. Telebugs fetches a bundle and discovers its map from, in order:

1. the `SourceMap` response header;
2. the legacy `X-SourceMap` response header; or
3. one unambiguous trailing `sourceMappingURL` comment.

Relative map URLs are resolved against the bundle URL. A map on another origin
is fetched only when that exact origin is also authorized. Inline `data:` maps
are not supported.

Successfully retrieved maps are stored privately in Telebugs. A map whose
debug ID was verified against the report remains cached until artifact
retention removes it. Other successful maps are revalidated after 10 minutes
with ETag or Last-Modified when the asset server provides one. A negative result
is cached for 5 minutes.

Only new reports enter hosted discovery automatically. Telebugs does not scan
historical reports when an origin is added. To retry one older report, open it,
select the report actions menu, and choose **Retry source map**. This action is
admin-only and cannot bypass any origin, network, size, rate, disk, or instance
safety rule.

### Security and Privacy

Hosted discovery fails closed:

- Telebugs connects only to an exact authorized HTTPS origin.
- Every DNS lookup must return only globally routable addresses. Private,
  loopback, link-local, reserved, multicast, IPv4-mapped private, and mixed
  public/private answers are rejected.
- Telebugs pins a validated address for the connection while verifying the TLS
  certificate against the original hostname.
- Redirects and compressed responses are rejected. Environment proxy settings
  are not used.
- Requests contain no cookies, credentials, authorization headers, event
  headers, referrer, or customer secrets.
- Telebugs never follows `sources` or `sourceRoot` entries and never downloads
  original source files. Original code is shown only when the map itself
  contains `sourcesContent`.
- Request URLs, hostnames, network addresses, headers, queries, response
  bodies, source code, and report content are not written to hosted-discovery
  telemetry.

Private networks, authenticated maps, custom headers, redirects, inline maps,
CSS maps, Wasm maps, and sectioned source maps are not supported. Use uploaded
artifacts when a deployment does not meet these rules.

### Hosted Discovery Limits

| Boundary | Limit |
| --- | ---: |
| Authorized origins per project | 10 |
| Bundle candidates per report | 2 |
| URL length | 2 KiB |
| Generated JavaScript response | 8 MiB |
| Source map response | 32 MiB |
| DNS timeout | 1 second |
| Connection timeout | 2 seconds |
| Read timeout | 3 seconds |
| Shared report budget | 10 seconds |
| Hosted maps cached per project | 500 |
| Network fetches per project | 10/minute and 100/hour |
| Network fetches per instance | 60/minute |

Transient network failures are retried once within the same 10-second report
budget. Permanent validation and security failures are not retried
automatically. Hosted network work runs on a separate single-worker queue, so a
slow asset server does not delay error ingestion or uploaded source maps.

### Hosted Discovery Statuses and Troubleshooting

The report page shows one of these statuses:

| Status | Meaning |
| --- | --- |
| **Unprocessed** | Hosted or uploaded source map processing has not run. |
| **Queued** | Processing is waiting on a background worker. |
| **Fetching** | Telebugs is processing an uploaded map or performing hosted discovery. |
| **Resolved** | At least one frame was mapped to original source. |
| **Not found** | No candidate, reference, file, or applicable mapping was found. |
| **Failed** | A network, server, size, or map-validation failure occurred safely. |
| **Blocked** | An authorization, instance, disk, debug-ID, or network safety rule prevented processing. |

The same status appears as `Source Map Status` in **View as Markdown**. When a
failure reason is available, Markdown also includes `Source Map Failure Code`.
The codes are grouped below with the action to take:

- `candidate_not_found`, `map_not_found`, `http_not_found`,
  `mapping_not_found`, `cached_not_found`: verify the JavaScript frame URL,
  deployment, source map reference, and mapping. Wait five minutes or use the
  admin retry after correcting the deployment.
- `origin_not_allowed`, `invalid_url`, `invalid_map_reference`,
  `hosted_fetching_disabled`: authorize the exact bundle and map origins, use a
  supported external map URL, or re-enable the instance switch.
- `non_public_address`, `redirect_rejected`, `compression_rejected`,
  `pinning_unavailable`, `invalid_request_header`: the request did not satisfy
  the hosted security boundary. Change the public asset response or use an
  uploaded map; retry cannot override the boundary.
- `debug_id_mismatch`: deploy the map that belongs to the reported bundle, or
  upload the correct release artifacts.
- `disk_pressure`: restore free disk space above the instance safety floor.
- `dns_failure`, `network_error`, `timeout`, `http_unavailable`, `rate_limited`:
  correct the public DNS/server problem or wait for the temporary condition to
  clear, then retry.
- `response_too_large`: reduce the generated bundle or map below the documented
  boundary, or use uploaded artifacts.
- `http_error`, `invalid_map`, `artifact_processing_failed`,
  `unexpected_error`: verify that the response is a supported version-3 source
  map. If a valid uploaded map still fails, inspect the Jobs dashboard and
  Telebugs logs for the bounded error class.

## Managing Source Maps

Uploaded source maps appear as artifacts on the release details page. From
there you can view or download an artifact, delete an incorrect artifact, or
delete the release and all of its maps.

Hosted maps are private cache entries and have no download interface. They are
counted as artifacts for disk usage and retention. Time-based cleanup uses
their last-use time, and disk-based cleanup removes least-recently-used hosted
maps before uploaded release artifacts.

Use meaningful release versions and immutable asset filenames. Immutable URLs
make both uploaded and hosted source map matching more reliable.

[1]: /projects-02-individual-project-view.md
[2]: /releases-00.md
[3]: /instance-05-ingestion-and-upload-limits.md
