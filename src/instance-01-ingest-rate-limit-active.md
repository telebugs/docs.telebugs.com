# Rate Limit Active

Telebugs shows this warning when the accepted-errors-per-minute limit has been
reached.

This usually means Telebugs is doing exactly what you asked it to do: accepting
up to the configured limit, then returning `429 Too Many Requests` with a
`Retry-After` header for the rest. Rejected errors are not written to the ingest
queue and do not create background jobs.

## What To Check

Open **Settings** > **Instance** > **Ingest Protection**.

Check:

- **Accepted errors this minute**
- **Rate-limited errors this minute**
- **Limited by rate limit last hour**
- **Queued errors**

If queued errors stay low, the instance is healthy and the rate limit is simply
protecting Telebugs during a noisy burst.

## What To Do

First, find the app or deploy that is sending the burst. A rate limit protects
Telebugs, but it does not fix the underlying error storm.

If the burst is expected and the server has headroom, raise **Accepted errors
per minute**. Do this carefully. A higher front-door limit lets more work enter
SQLite and the background queue.

If queued errors also start climbing, do not keep raising the rate limit. Lower
the accepted-errors-per-minute setting, give the server more CPU or faster disk,
or reduce the noisy source.

For low-end VPSes, the default `3,000` accepted errors per minute is a good
starting point. For larger servers, benchmark your own instance and set the
limit near the sustained processing rate you are comfortable with.

## When It Clears

Rate limiting clears automatically when incoming traffic drops below the
configured limit in a later minute bucket.
