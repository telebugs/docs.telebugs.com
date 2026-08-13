# Reports

Reports are individual error occurrences. You can list and retrieve reports
under a specific group. Reports expose per-occurrence details such as
`server_name` (useful when combined with group filtering by `server_name`),
`environment`, `tags`, `contexts`, user info, request data, and more.

## List Reports under a Group

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/reports \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

### Filtering

You can filter reports using these parameters:

| Parameter | Description                  | Example             |
| --------- | ---------------------------- | ------------------- |
| `since`   | Reports that occurred after  | `?since=2026-05-01` |
| `until`   | Reports that occurred before | `?until=2026-05-20` |

Example:

```sh
curl "https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/reports?since=2026-05-01&limit=50" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Reports support cursor-based pagination using `cursor` and `limit` (for size) and return `next_cursor` + `has_more`. See the [Pagination](rest-api-02-pagination.md) guide.

### Response Format (List)

Each item in the list includes core fields plus occurrence-specific data:

```json
{
  "reports": [
    {
      "id": 123,
      "group_id": 42,
      "project_id": 1,
      "event_id": "69b345eb156342a496e5880afee01452",
      "error_type": "NoMethodError",
      "error_message": "undefined method `foo' for nil:NilClass",
      "culprit": "OrdersController#create",
      "occurred_at": "2026-05-20T14:55:01Z",
      "platform": "ruby",
      "severity": "error",
      "handled": true,
      "server_name": "eagle-618d24",
      "environment": "production",
      "release_version": "1.2.3",
      "sourcemap_status": "resolved",
      "sourcemap_failure_code": null,
      "sourcemap_attempted_at": "2026-05-20T14:55:02Z",
      "created_at": "2026-05-20T14:55:01Z",
      "tags": [
        { "key": "component", "value": "api" },
        { "key": "host", "value": "eagle-618d24" }
      ]
    }
  ],
  "next_cursor": 122,
  "has_more": true
}
```

## Get a Single Report

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/reports/REPORT_ID \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

### Response Format (Single Report)

The single report response includes all list fields plus additional context:

```json
{
  "id": 123,
  "group_id": 42,
  "project_id": 1,
  "event_id": "69b345eb156342a496e5880afee01452",
  "error_type": "NoMethodError",
  "error_message": "undefined method `foo' for nil:NilClass",
  "culprit": "OrdersController#create",
  "occurred_at": "2026-05-20T14:55:01Z",
  "platform": "ruby",
  "severity": "error",
  "handled": true,
  "server_name": "eagle-618d24",
  "environment": "production",
  "release_version": "1.2.3",
  "custom_fingerprint": null,
  "transaction_source": null,
  "sourcemap_status": "resolved",
  "sourcemap_failure_code": null,
  "sourcemap_attempted_at": "2026-05-20T14:55:02Z",
  "created_at": "2026-05-20T14:55:01Z",
  "updated_at": "2026-05-20T14:55:01Z",
  "tags": [
    { "key": "component", "value": "api" }
  ],
  "contexts": [
    { "name": "runtime", "data": { "version": "3.2" } }
  ],
  "user": {
    "user_id": "u123",
    "username": "alice",
    "email": "alice@example.com",
    "ip_address": "203.0.113.42",
    "geo_city": "Berlin",
    "geo_region": "BE",
    "geo_country_code": "DE",
    "data": {}
  },
  "request": {
    "url": "https://example.com/orders",
    "method": "POST",
    "query_string": "",
    "data": { "foo": "bar" },
    "cookies": {},
    "headers": { "User-Agent": "..." },
    "env": {}
  },
  "sdk": {
    "name": "rails",
    "version": "7.1"
  },
  "extras": [
    { "key": "custom", "value": "data" }
  ],
  "dependencies": [
    { "name": "rails", "version": "7.1" }
  ],
  "release": {
    "id": 7,
    "version": "1.2.3"
  }
}
```

`event_id` is `null` on legacy reports received before occurrence identity was
stored. Source map status is one of `unprocessed`, `queued`, `fetching`,
`resolved`, `not_found`, `failed`, or `blocked`. Failure code and attempt time are
`null` until applicable.

## Get a Report by Event ID

Use the project-scoped occurrence ID when an SDK or ingestion response gives you
an event ID but not a Telebugs report ID:

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/reports/EVENT_ID \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

This returns the same detailed representation as the group-nested report route.
Dashless and standard hyphenated event IDs are accepted case-insensitively and
normalized to 32 lowercase hexadecimal characters. Invalid, missing,
inaccessible, and wrong-project IDs return `404 Not Found`.

## Retry Source Map Processing

An admin API key can retry source map processing for one report:

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/reports/REPORT_ID/sourcemap_retry \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

A queued or already-running attempt returns `202 Accepted`; an already resolved
report returns `200 OK`:

```json
{
  "result": "queued",
  "report_id": 123,
  "sourcemap_status": "queued",
  "sourcemap_failure_code": null,
  "sourcemap_attempted_at": null
}
```

Failures use `application/problem+json` and include the same public diagnostic
fields:

| Status | Meaning |
| --- | --- |
| `409 Conflict` | No uploaded release map or authorized hosted origin is available |
| `422 Unprocessable Content` | The report is not a JavaScript report |
| `503 Service Unavailable` | Work could not be queued; retry shortly |

The internal processing token is never returned.
