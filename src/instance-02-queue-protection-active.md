# Queue Protection Active

Telebugs shows this warning when too many incoming errors are waiting to be
processed.

This means Telebugs is accepting errors faster than its background workers can
finish them. New errors are temporarily rejected with `429 Too Many Requests`
before they are written to the ingest queue. This protects SQLite and Solid
Queue from an unbounded backlog.

## What To Check

Open the profile menu, then go to **Instance** > **Ingest Protection**.

In the **Queue protection** card, check:

- **Queued errors**
- **Queued payload bytes**
- **Fixed queued-byte ceiling**
- **Limited by queued errors this minute**
- **Limited by queued errors last hour**
- **Reports processed during load**, if you are benchmarking with `bin/load`

Then open the **Jobs** dashboard from the warning banner or go to `/jobs`.

In the Jobs dashboard, look for:

- Failed jobs
- Jobs that are retrying repeatedly
- A queue that is not draining
- Slow or stuck ingest jobs

## What To Do

If jobs are failing, fix the failing job first. Raising the queued-errors limit
will only give Telebugs more work it cannot currently process.

If jobs are running but the queue is growing, lower **Accepted errors per
minute** in the **Rate limit** card so Telebugs accepts work at a rate the
server can sustain.

If this is normal traffic and not an error storm, the instance may need more
CPU, faster disk, or a bigger server.

Only raise **Maximum queued errors** in the **Queue protection** card when you
are comfortable with a longer drain time. A large queue can be useful for short
bursts, but it can also leave Telebugs working through old errors long after the
incident has passed.

The 512 MiB queued-byte ceiling is fixed and remains active even if you disable
the configurable queued-error count check. If bytes reach that ceiling with a
relatively small error count, unusually large events are filling the queue.
Wait for the queue to drain and investigate slow or failing ingest jobs rather
than trying to tune around the boundary.

## When It Clears

Queue protection clears when pending ingest payloads are below **Maximum queued
errors** and pending bytes are below the fixed queued-byte ceiling. If traffic
has calmed down and workers are healthy, this should happen as the queue drains.
