# Liveness, Readiness, and Status

Telebugs exposes two small, unauthenticated HTTP checks and one detailed local
command. The HTTP responses never include database names, paths, queue counts,
error messages, or other diagnostic details.

## Liveness: `/up`

`GET /up` returns `200` when the Rails web application boots and can answer a
request. Use it to decide whether the web process should be restarted.

Liveness does not prove that Telebugs can write data, process queues, or send
notifications.

## Readiness: `/ready`

`GET /ready` and `HEAD /ready` return:

- `200` with `ready` when the installation is ready; or
- `503` with `not ready` when an essential local dependency is unavailable.

Responses use `text/plain` and `Cache-Control: no-store`. Results are cached in
the web process for up to 10 seconds to keep the check cheap.

Readiness checks:

- primary, cache, and queue database access;
- pending database migrations;
- application encryption keys that can read stored notification configuration;
- readability and writability of database and file storage;
- measurable free disk space above the configured intake floor;
- disk or queue protection that has paused intake;
- a fresh Solid Queue dispatcher and workers for error processing and notifications; and
- error or notification jobs that have remained ready or claimed for more than
  five minutes.

Normal rate limiting does not make the instance unready. A single permanently
failed notification delivery also does not make it unready: the app can still
ingest and other destinations can still deliver.

Do not put external email, push, or webhook requests inside a readiness probe.
Those services can be slow or unavailable without making the local Telebugs
installation unsafe to run.

## Detailed Local Status

Run this over SSH on the Telebugs host:

```bash
telebugs status
```

It distinguishes a running container, a responding web app, and an instance
ready to ingest and notify. It prints fixed reason codes for database access,
migrations, storage, disk, intake, worker heartbeats, and queue latency. It also
shows an advisory warning when notification deliveries have permanently failed.

For scripts:

```bash
telebugs status --json
```

The command exits nonzero when the container is stopped, `/up` fails, or
readiness fails. A notification failure warning alone does not change readiness
or the exit status.

Keep this detailed output local to operators. The reason codes avoid report
payloads, email addresses, webhook URLs, secrets, and exception messages, but a
local diagnostic command should still not become a public endpoint.

## External Monitoring

For the simplest setup, monitor `/ready` from outside the server and alert after
more than one failed check so a restart or update does not create noise. Monitor
`/up` separately only if you need to distinguish a dead web process from an
unready dependency.

The host or an external tool remains responsible for:

- host reachability, CPU, memory, inode, and filesystem capacity;
- Docker and operating-system service health;
- DNS and TLS certificate expiry;
- backup recency and off-server replication;
- restore-drill records;
- network access from every application that sends errors; and
- end-to-end tests of the notification destinations your team relies on.

Telebugs intentionally does not provide a configurable health dashboard,
metrics store, paging system, or vendor-specific monitoring integration. Use
the two stable HTTP checks with the monitoring system you already operate.
