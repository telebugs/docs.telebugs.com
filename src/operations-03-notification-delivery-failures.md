# Notification Delivery Failures

Telebugs sends each email recipient, push subscription, and webhook subscription
as an independent background job. One broken destination does not block the
other recipients or make `/ready` fail.

Temporary delivery failures are attempted up to 10 times with increasing delays.
For HTTP delivery, `408`, `425`, `429`, and `5xx` responses are temporary.
Telebugs respects `Retry-After` up to one hour. Network timeouts, temporary SMTP
failures, and temporary push-service failures are retried too.

Delivery is at least once. A destination can accept a request before its
response is lost, so a retry can occasionally deliver the same notification
twice. Destinations should tolerate duplicates.

The queue database is included in Telebugs backups. Pending or retrying
deliveries resume after a restore and can therefore repeat an older
notification. Isolate outbound delivery on restore-drill hosts until their
destinations have been replaced with safe test endpoints.

Redirects, other HTTP `4xx` responses, TLS or invalid-URL errors, SMTP
authentication or fatal responses, invalid configuration, and exhausted retries
are permanent failures. Expired or invalid push subscriptions are removed
instead of retried.

## Admin Warning

Admins see a warning banner when one or more jobs in the notification queue have
permanently failed. The banner shows the count and age of the oldest failure and
links to the existing jobs page. It does not include recipient addresses,
webhook URLs, payloads, or remote response bodies.

The warning stays visible while any permanently failed notification jobs remain.
To clear it, fix the destination and retry the job, or discard the job if the
notification no longer needs to be delivered. A retried job clears the warning
after it succeeds. If it fails again, or another delivery fails permanently, the
warning remains. After the last failed job is retried successfully or discarded,
the warning can take up to 30 seconds and a page reload to disappear.

`telebugs status` shows the same condition as an advisory warning. It does not
turn the instance unready because ingestion and unrelated destinations can
continue safely.

Do not alert on an individual retry. Treat a permanent failure as operator work:
create a normal-priority ticket by default, and page only when the failed channel
is itself part of a critical incident path. External checks can inspect the
`warnings` array from `telebugs status --json`; Telebugs does not send a second
alert about the first alert failing.

## What to Do

1. Open **Review failed jobs** from the banner.
2. Identify the channel and the normalized failure class.
3. Check the corresponding configuration without copying secrets into tickets
   or chat:
   - email credentials, sender policy, DNS, and SMTP reachability;
   - webhook authentication, URL allowlists, and the destination's status;
   - push VAPID configuration and outbound HTTPS access.
4. Fix the destination.
5. Choose what should happen to the failed job:
   - **Retry** it after the destination is fixed. The warning clears after the
     delivery succeeds.
   - **Discard** it if the notification no longer needs to be delivered. This
     removes the failed job without sending it.

If notification delivery keeps failing, the warning stays visible. Do not
discard recurring failures just to hide it; fix or disable the broken
destination first.

Telebugs does not email an admin about failed email delivery because that can
fail recursively. It also does not call a second external alerting provider.
Operators who need paging should run their existing monitoring or scheduled
checks alongside `telebugs status` and their own end-to-end notification test.

At the default production `info` log level, Telebugs' operational delivery logs
use IDs, HTTP status codes, and normalized error classes rather than notification
payloads, recipient addresses, webhook URLs, remote response bodies, or secrets.
Do not enable framework debug logging routinely: debug output can include email
content and other application data. Host administrators are still responsible
for restricting and rotating Docker logs.
