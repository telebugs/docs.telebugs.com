# Instance Settings

Instance settings help you keep a self-hosted Telebugs server healthy over time.
They are global to the whole installation, not per-project.

Telebugs keeps these controls in the admin UI instead of hiding them behind
environment variables. Open the profile menu, then go to **Instance**.

This chapter covers ingest protection, error retention, artifact retention,
purge types, and disk usage monitoring.

## Ingest Protection

Ingest protection controls how many incoming errors Telebugs accepts and when it
should temporarily pause intake to protect the instance.

It protects the server during error storms, such as a runaway deploy or a noisy
endpoint that suddenly starts raising thousands of exceptions. It also protects
the instance when workers fall behind or disk space gets low.

When an ingest protection check is enabled and a limit is reached, Telebugs
returns `429 Too Many Requests` with a `Retry-After` header. Rejected errors are
not written to the ingest queue and do not create background jobs.

The default rate limit is **3,000 accepted errors per minute**. That is 50 errors
per second, which matches the sustained processing baseline for a small 2 vCPU /
4 GB RAM VPS in Telebugs benchmarks. Larger servers can safely use a higher
limit.

Ingest protection has three checks:

- **Accepted errors per minute**: Caps incoming error intake.
- **Maximum queued errors**: Pauses intake when too many errors are waiting to be
  processed. The default is 10,000 queued errors, which gives a small VPS a few
  minutes to catch up before the queue grows without bounds.
- **Minimum free disk space**: Pauses intake before disk space gets dangerously
  low. The default floor is 2,048 MB free.

The disk check looks at free space on the filesystem that contains the SQLite
database. If another app, log file, backup, or service fills that same
filesystem, Telebugs sees the lower free space and can pause intake. If you put
large files on a separate mount, monitor that mount separately. You can manage
these settings through the UI or the [Ingest Protection REST API](rest-api-11-data-retention.md#update-ingest-protection-policy).

SQLite's `VACUUM` command may need free disk space up to twice the current
database size to compact safely. Telebugs shows this as SQLite maintenance
status in the **Disk protection** card. That maintenance status is advisory: it
does not pause intake by itself. Intake pauses when free disk space falls below
your configured **Minimum free disk space** value.

The Ingest Protection page is organized into one status card and three
guardrail cards:

- **Status**: Shows whether Telebugs is accepting errors, rate limiting, paused
  by queued errors, or paused by disk pressure.
- **Rate limit**: Shows rate-limit counters, then lets you enable the accepted
  errors per minute limit and set the limit.
- **Queue protection**: Shows queued-error counters, then lets you enable the
  queued-errors limit and set the limit.
- **Disk protection**: Shows free disk space, the pause threshold, SQLite
  maintenance status, and disk-pressure counters. It also lets you enable the
  free disk space limit, set the limit, and recheck disk space immediately.

Each guardrail card has its own save button. Saving one card only updates that
card's settings.

For incident-specific help, see:

- [Rate Limit Active](instance-01-ingest-rate-limit-active.md)
- [Queue Protection Active](instance-02-queue-protection-active.md)
- [Disk Space Low](instance-03-disk-space-low.md)

### How the Checks Work Together

Telebugs checks ingest protection before it writes the incoming error to the
ingest queue or creates a background job.

If more than one protection would apply at the same time, Telebugs uses this
order:

1. **Disk pressure**
2. **Queued errors**
3. **Accepted errors per minute**

Disk pressure wins because a full disk can make SQLite and background jobs
unhealthy. Queue pressure comes next because it means Telebugs is accepting
errors faster than workers can process them. The per-minute rate limit is the
normal front-door throttle for error storms.

When a request is rejected, Telebugs returns `429 Too Many Requests` and a
`Retry-After` header. The request is not written to `ingest_payloads` and no
processing job is enqueued.

### How to Tell What Is Happening

Open the profile menu, then go to **Instance** > **Ingest Protection**.

When Telebugs is actively limiting or pausing incoming errors, admins also see a
banner at the top of the app. The banner links back to Ingest Protection so the
reason is not hidden during an incident.

The cards show:

- **Status card**: Current status, accepted errors last hour, and rate-limited
  errors last hour.
- **Rate limit card**: Accepted errors this minute, errors limited by the rate
  limit this minute, and errors limited by the rate limit last hour.
- **Queue protection card**: Current queued errors, errors limited by queued
  errors this minute, and errors limited by queued errors last hour.
- **Disk protection card**: Free disk space, the current pause threshold,
  SQLite maintenance status, errors limited by low disk space this minute, and
  errors limited by low disk space last hour. Use **Recheck disk space** after
  freeing disk if the page still shows an old value.

During an incident, the fastest read is:

1. Check the **Status** card.
2. Check which guardrail card has an increasing “Limited by...” counter.
3. Check **Queued errors** and **Free disk space** in their guardrail cards.

### Example Error Storm

Suppose Telebugs is running on a small 2 vCPU / 4 GB RAM VPS with the defaults:

- Accepted errors per minute: `3,000`
- Maximum queued errors: `10,000`
- Minimum free disk space: `2,048 MB`

An app deploy starts sending 12,000 errors per minute.

At first, Telebugs accepts up to 3,000 errors per minute and starts returning
`429 Too Many Requests` for the rest. The **Limited by rate limit last hour**
counter climbs.

If workers fall behind and queued errors reach 10,000, Telebugs pauses intake
because of queue pressure. The **Status** changes to queued-error pressure and
the **Limited by queued errors last hour** counter starts climbing.

If disk space also drops below the safe threshold, disk pressure takes over. The
**Status** changes to disk pressure and the **Limited by low disk space last
hour** counter climbs. Disk pressure takes precedence over the other checks
until free disk space recovers.

### Recommended Starting Points

These are starting points, not promises. Disk speed, payload size, read traffic,
retention settings, and background job throughput all matter. Use `bin/load`
from the source tree to benchmark your own server when you want confidence.

| Server size | Accepted errors per minute | Maximum queued errors | Minimum free disk space |
| --- | ---: | ---: | ---: |
| 2 vCPU / 4 GB RAM / 40 GB disk | 3,000 | 10,000 | 2,048 MB |
| 4 vCPU / 8 GB RAM / 80 GB disk | 6,000 | 20,000 | 4,096 MB |
| 8 vCPU / 16 GB RAM / 160 GB disk | 12,000 | 40,000 | 8,192 MB |
| 16 vCPU / 32 GB RAM / 320 GB disk | 24,000 | 80,000 | 16,384 MB |

For low-end VPSes, use the defaults unless you have measured otherwise.

For larger servers, scale the accepted-errors-per-minute setting with your
measured sustained processing rate. A simple starting point is:

```text
accepted errors per minute = sustained processed errors per second * 60
```

The queued-errors value should usually represent a few minutes of backlog, not
hours. If it is too low, Telebugs pauses during harmless bursts. If it is too
high, a storm can leave a long drain time and a large database write backlog.

For disk space, keep the configured minimum at roughly 5% of the disk, with
2,048 MB as the minimum. The **SQLite maintenance status** row may still say
that SQLite needs more free space to compact the database. That is a maintenance
warning, not an ingest pause by itself.

### Tuning Advice

If **Limited by rate limit last hour** climbs but queued errors stay low, the
instance is healthy and the rate limit is doing its job. Raise the rate limit
only if the server has headroom and you are comfortable accepting more storm
traffic.

If **Limited by queued errors last hour** climbs, Telebugs is accepting errors
faster than workers can process them. Lower the accepted-errors-per-minute value,
increase server resources, or investigate slow disk/background processing.

If **Limited by low disk space last hour** climbs, do not only raise the disk
threshold. First free disk space, enable or tighten retention, run maintenance
when safe, or increase disk size. Disk pressure means Telebugs is protecting the
SQLite database and job queues from operating too close to full disk.

Ingest protection is a brake, not cleanup. Pair it with error retention and
artifact retention so Telebugs does not grow forever after the storm passes.

## Error Retention Policy

Error retention controls how long reports and their details (backtraces,
breadcrumbs, tags, notes, etc.) are stored.

Enable automatic cleanup to prevent unlimited growth. Cleanup jobs run nightly
at 2 AM server time. You can also trigger manual purges immediately.

### Enabling Error Retention

Open the profile menu, then go to **Instance** > **Error Retention**.

Toggle **Enable automatic error cleanup** and save. The UI shows when the next
cleanup will run.

### Time-Based Cleanup

Delete reports older than a set number of days.

Choose:

- **Full purge**: Removes everything (including notes and attachments).
  Historical details are lost.
- **Partial purge**: Keeps basic metadata for graphs and counts, but deletes
  heavy details like stack traces and contexts.

**Example:** A 90-day partial purge keeps stats for reports older than 90 days
but removes the full payloads.

### Disk-Based Cleanup

Triggers when the database file grows too large (full purge only, oldest reports
first).

Set the limit as:

- Absolute size (e.g., 10 GB)
- Percentage of total disk (e.g., 35%)

Runs alongside time-based rules if both are enabled.

## Artifact Retention Policy

Artifacts (mainly source maps attached to releases) have separate retention
rules.

### Enabling Artifact Retention

Open the profile menu, then go to **Instance** > **Artifact Retention**.

Toggle **Enable automatic artifact cleanup**.

### Time-Based Artifact Cleanup

Deletes artifacts from releases older than the set period, but only if no recent
error reports reference them.

### Disk-Based Artifact Cleanup

Triggers when total artifact storage exceeds the limit (absolute GB or
percentage).

Deletes from oldest inactive releases first.

### Purge on New Release

Optional: When uploading a new release, automatically delete artifacts from
excess old releases (keep only the newest N, e.g., 20).

Oldest inactive releases are removed first.

## Monitoring and Maintenance

The Instance section shows live stats:

- Total and free disk space
- Database size and percentage used
- Artifact size and count
- Total report count
- Accepted and rate-limited ingest counts
- SQLite maintenance status

Stats refresh automatically after cleanups.

Telebugs runs a nightly `VACUUM` job to reclaim unused space when there's enough
free disk. SQLite may need free space up to roughly twice the current database
size to compact safely.

### Maintenance Activity

Open the profile menu, then go to **Instance** > **Maintenance Activity**.

The **Recent maintenance activity** list shows destructive maintenance work
across the whole instance. It helps admins answer what cleanup ran, whether it
finished, who or what started it, and what it deleted.

Telebugs records scheduled and manual error purges, artifact purges, note
attachment purges, and database `VACUUM` runs. Each entry shows the task name,
status, short result, project scope, actor, source, and timestamp. Statuses can
be **Running**, **Completed**, **Failed**, or **Skipped**.

Click an entry to open a linkable detail page. Detail pages show UTC started
and finished timestamps plus safe summary fields, such as cutoff date, deleted
counts, database size, free disk space, or a short error class.

This is intentionally not a full audit log. Telebugs does not store deleted
report titles, exception messages, stack traces, payloads, or every deleted row
in this history. If the list says **No data**, no tracked maintenance has run
yet, or the previous records were older than 90 days and have been pruned.

The list uses cursor pagination, so older records are available without loading
the entire history at once. Maintenance activity records are kept for 90 days
and pruned daily.

**Important:** All automatic and manual purges are irreversible. Export critical
data if needed before cleanup.

For quick cleanup, use the **Danger Zone** in [project settings][3] to purge all
error data or note attachments manually.

Retention policies can also be managed programmatically via the
[REST API](rest-api-11-data-retention.md).

[3]: /projects-04-project-settings.md
