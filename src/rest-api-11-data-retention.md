# Data Retention

Data retention policies let you control how long error reports and release artifacts (such as debug symbols and minidumps) are kept. This is primarily for compliance and data minimization requirements.

The policies are global to the instance (not per-project).

All endpoints require an admin user's API key.

In the Telebugs UI, these settings live under the profile menu > **Instance**.

## Get Ingest Protection Policy

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/data_retention/ingest_protection \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

## Update Ingest Protection Policy

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/data_retention/ingest_protection \
  -X PATCH \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "enabled": true,
    "global_rate_limit_per_minute": 3000,
    "backlog_protection_enabled": true,
    "max_pending_ingest_payloads": 10000,
    "disk_protection_enabled": true,
    "minimum_free_disk_space_mb": 2048
  }'
```

## Get Error Retention Policy

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/data_retention/errors \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

## Update Error Retention Policy

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/data_retention/errors \
  -X PATCH \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "enabled": true,
    "time_based_enabled": true,
    "retention_period_days": 30,
    "time_purge_type": "partial",
    "disk_based_enabled": false
  }'
```

## Get Artifact Retention Policy

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/data_retention/artifacts \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

## Update Artifact Retention Policy

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/data_retention/artifacts \
  -X PATCH \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "enabled": true,
    "time_based_enabled": true,
    "retention_period_days": 90,
    "disk_based_enabled": true,
    "disk_limit_type": "percentage",
    "disk_limit_value": 20,
    "purge_on_new_release": true,
    "max_releases_kept": 10
  }'
```

## Hosted Source Map Processing

Read or update the instance-wide hosted source map emergency switch with an
admin API key:

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/data_retention/hosted_sourcemaps \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/data_retention/hosted_sourcemaps \
  -X PATCH \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"enabled": false}'
```

Both responses use this shape:

```json
{"enabled":false}
```

Disabling this switch prevents hosted network fetching. Uploaded release maps
continue to work.

## Response Format (Ingest Protection)

For ingest protection, `enabled` controls the accepted-errors-per-minute limit.
Backlog and disk protection have their own separate switches. The
`minimum_free_disk_space_mb` value is the hard free-space floor for disk
protection. Telebugs pauses intake when the filesystem that contains the SQLite
database falls below that value.

The pending-byte and recent-activity fields are read-only status values:

- `pending_ingest_bytes`: decoded bytes currently waiting for processing.
- `max_pending_ingest_bytes`: fixed 512 MiB queued-byte ceiling.
- `recent_rejections`: bounded-ingest rejections in the last hour.
- `recent_truncations`: accepted events shortened in the last hour.

They appear in the response and cannot be changed by `PATCH`.

```json
{
  "enabled": true,
  "global_rate_limit_per_minute": 3000,
  "backlog_protection_enabled": true,
  "max_pending_ingest_payloads": 10000,
  "pending_ingest_bytes": 245760,
  "max_pending_ingest_bytes": 536870912,
  "recent_rejections": 2,
  "recent_truncations": 7,
  "disk_protection_enabled": true,
  "minimum_free_disk_space_mb": 2048
}
```

## Response Format (Error Retention)

```json
{
  "enabled": true,
  "time_based_enabled": true,
  "retention_period_days": 30,
  "time_purge_type": "partial",
  "disk_based_enabled": false,
  "disk_limit_type": "absolute",
  "disk_limit_value": 35
}
```

## Response Format (Artifact Retention)

```json
{
  "enabled": true,
  "time_based_enabled": true,
  "retention_period_days": 90,
  "disk_based_enabled": true,
  "disk_limit_type": "percentage",
  "disk_limit_value": 20,
  "purge_on_new_release": true,
  "max_releases_kept": 10
}
```

See the [Instance Settings](instance-00.md) chapter for details on the meaning of each setting (ingest protection, time-based vs disk-based cleanup, full vs partial purge, etc.).
