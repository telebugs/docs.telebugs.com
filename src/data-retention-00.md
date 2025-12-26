# Data Retention

Data retention in Telebugs helps you control how long [error reports][1] and
artifacts (like [source maps][2]) are kept. Automatic policies clean up old data
based on time or disk usage, keeping storage manageable and supporting
compliance needs.

Cleanup jobs run nightly at 2 AM server time. You can also trigger manual purges
immediately.

This chapter covers error and artifact retention policies, purge types, and
monitoring disk usage.

## Error Retention Policy

Error retention controls how long reports and their details (backtraces,
breadcrumbs, tags, notes, etc.) are stored.

Enable automatic cleanup to prevent unlimited growth.

### Enabling Error Retention

Go to **Settings** > **Data Retention**.

Toggle **Enable automatic error cleanup** and save. The UI shows when the next
cleanup will run.

### Time-Based Cleanup

Delete reports older than a set number of days.

Choose:

- **Full purge**: Removes everything (including notes and attachments).
  Historical details are lost.
- **Partial purge**: Keeps basic metadata for graphs and counts, but deletes
  heavy details like stack traces and contexts.

**Example:** A 90-day partial purge keeps stats for reports older than 90 days but
removes the full payloads.

### Disk-Based Cleanup

Triggers when the database file grows too large (full purge only, oldest reports
first).

Set limit as:

- Absolute size (e.g., 10 GB)
- Percentage of total disk (e.g., 35%)

Runs alongside time-based rules if both are enabled.

## Artifact Retention Policy

Artifacts (mainly source maps attached to releases) have separate retention
rules.

### Enabling Artifact Retention

In **Settings** > **Data Retention**, toggle **Enable automatic artifact
cleanup**.

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

The **Data Retention** section shows live stats:

- Total and free disk space
- Database size and percentage used
- Artifact size and count
- Total report count

Stats refresh automatically after cleanups.

Telebugs runs a nightly `VACUUM` job to reclaim unused space when there's enough
free disk (database size + 10% buffer).

**Important:** All automatic and manual purges are irreversible. Export critical
data if needed before cleanup.

For quick cleanup, use the **Danger Zone** in project settings to purge all
error data or note attachments manually.

[1]: /error-reports-00.md
[2]: /source-maps-00.md
