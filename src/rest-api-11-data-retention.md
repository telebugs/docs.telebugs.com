# Data Retention

Data retention policies let you control how long error reports and release artifacts (such as debug symbols and minidumps) are kept. This is primarily for compliance and data minimization requirements.

The policies are global to the instance (not per-project).

All endpoints require an admin user's API key.

In the Telebugs UI, these settings live under **Settings** > **Instance**.

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
    "global_rate_limit_per_minute": 3000
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

## Response Format (Ingest Protection)

```json
{
  "enabled": true,
  "global_rate_limit_per_minute": 3000
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
