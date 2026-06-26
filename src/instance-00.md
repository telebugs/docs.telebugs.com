# Instance Settings

Instance settings help you keep a self-hosted Telebugs server healthy over time.
They are global to the whole installation, not per-project.

Telebugs keeps these controls in the admin UI instead of hiding them behind
environment variables. Go to **Settings** > **Instance**.

This chapter covers ingest protection, error retention, artifact retention,
purge types, and disk usage monitoring.

## Ingest Protection

Ingest protection limits how many incoming errors Telebugs accepts per minute.
It protects the server during error storms, such as a runaway deploy or a noisy
endpoint that suddenly starts raising thousands of exceptions.

When ingest protection is enabled and the limit is reached, Telebugs returns
`429 Too Many Requests` with a `Retry-After` header. Rate-limited errors are not
written to the ingest queue and do not create background jobs.

The default is enabled at **3,000 accepted errors per minute**. That is 50 errors
per second, which matches the sustained processing baseline for a small 2 vCPU /
4 GB RAM VPS in Telebugs benchmarks. Larger servers can safely use a higher
limit.

The Ingest Protection page also shows lightweight counters for accepted and
rate-limited errors in the current minute and the last hour.

## Error Retention Policy

Error retention controls how long reports and their details (backtraces,
breadcrumbs, tags, notes, etc.) are stored.

Enable automatic cleanup to prevent unlimited growth. Cleanup jobs run nightly
at 2 AM server time. You can also trigger manual purges immediately.

### Enabling Error Retention

Go to **Settings** > **Instance** > **Error Retention**.

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

Go to **Settings** > **Instance** > **Artifact Retention**.

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

Stats refresh automatically after cleanups.

Telebugs runs a nightly `VACUUM` job to reclaim unused space when there's enough
free disk (database size + 10% buffer).

**Important:** All automatic and manual purges are irreversible. Export critical
data if needed before cleanup.

For quick cleanup, use the **Danger Zone** in [project settings][3] to purge all
error data or note attachments manually.

Retention policies can also be managed programmatically via the
[REST API](rest-api-11-data-retention.md).

[3]: /projects-04-project-settings.md
