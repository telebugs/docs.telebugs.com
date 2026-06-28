# Disk Space Low

Telebugs shows this warning when free disk space is below the configured
threshold for the SQLite database filesystem.

This is the most serious ingest protection state. A full disk can make SQLite,
Solid Queue, and normal application writes unhealthy. Telebugs rejects new
errors with `429 Too Many Requests` before writing them to the ingest queue.

## What To Check

Open the profile menu, then go to **Instance** > **Ingest Protection**.

In the **Disk protection** card, check:

- **Free disk space**
- **Pause intake below**
- **SQLite maintenance needs**
- **SQLite maintenance status**
- **Limited by low disk space this minute**
- **Limited by low disk space last hour**

The disk check watches the filesystem that contains the SQLite database. If
another app, log file, backup, or service fills that same filesystem, Telebugs
sees the lower free space and can pause intake. If large files live on a
separate mount, monitor that mount separately.

**Pause intake below** is the configured hard floor. If free disk space is below
that number, Telebugs pauses incoming errors.

SQLite maintenance is shown separately. SQLite may need free disk space up to
twice the current database size to compact the database safely. If **SQLite
maintenance status** says more space is needed, Telebugs can still accept errors
as long as free disk space is above **Pause intake below**, but `VACUUM` may skip
compaction until there is more room.

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
space to run maintenance and reclaim unused SQLite pages safely. After freeing
space, click **Recheck disk space** in the **Disk protection** card if the page
still shows the old value.

## When It Clears

Disk protection clears when free disk space rises above **Pause intake below**.
Telebugs measures disk space periodically and also refreshes the cached
measurement after purge and database maintenance jobs. The **Recheck disk
space** button clears the cached measurement immediately.
