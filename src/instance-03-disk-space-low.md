# Disk Space Low

Telebugs shows this warning when free disk space is below the safe threshold for
the SQLite database filesystem.

This is the most serious ingest protection state. A full disk can make SQLite,
Solid Queue, and normal application writes unhealthy. Telebugs rejects new
errors with `429 Too Many Requests` before writing them to the ingest queue.

## What To Check

Open **Settings** > **Instance** > **Ingest Protection**.

Check:

- **Free disk space**
- **Pause intake below**
- **Limited by disk pressure last hour**

The disk check watches the filesystem that contains the SQLite database. If
another app, log file, backup, or service fills that same filesystem, Telebugs
sees the lower free space and can pause intake. If large files live on a
separate mount, monitor that mount separately.

SQLite may need free disk space up to twice the current database size to compact
the database safely. Because of that, **Pause intake below** can be higher than
the configured **Minimum free disk space** value.

## What To Do

Free disk space first.

Good options:

- Delete or move old logs and backups on the same filesystem.
- Enable or tighten error retention.
- Enable or tighten artifact retention.
- Increase the server disk size.
- Move unrelated services or backups off the Telebugs database filesystem.

Do not simply lower the disk threshold to make the warning disappear. That can
put SQLite and the job queue closer to a hard full-disk failure.

If the database has recently had a large purge, Telebugs may need enough free
space to run maintenance and reclaim unused SQLite pages safely.

## When It Clears

Disk protection clears when free disk space rises above the effective threshold.
That threshold is the higher of your configured minimum and SQLite's current
compaction safety requirement.
