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

This makes per-report data such as `server_name` (and the tags used for group-level filtering) directly reachable via the API.
