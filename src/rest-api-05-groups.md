# Groups

Groups represent aggregated errors. You can list, filter, resolve, and mute them
via the API.

## List Groups for a Project

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

This endpoint is commonly used to build internal dashboards or scripts that need
to count or iterate over issues per device, environment, or other tags.

## Filtering and Search

The recommended way to filter and search groups is with the `query` parameter.
It supports a rich search syntax that lets you combine status, severity, server/device
names, arbitrary tags, environments, and free-text search (including negation and OR)
in a single parameter.

**Common use case** — reading issues for a specific device/server:

```sh
curl "https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups?query=server_name:%22eagle-618d24%22" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

You can also combine it with status:

```sh
curl "https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups?query=is:unresolved+server_name:eagle-618d24" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

### Query Syntax

The `query` value can contain any combination of the following:

| Syntax                      | Meaning                                                       | Example                              |
| --------------------------- | ------------------------------------------------------------- | ------------------------------------ |
| `is:unresolved`             | Only unresolved groups                                        | `is:unresolved`                      |
| `is:resolved`               | Only resolved groups                                          | `is:resolved`                        |
| `is:muted`                  | Only muted groups                                             | `is:muted`                           |
| `is:unmuted`                | Only unmuted groups                                           | `is:unmuted`                         |
| `!is:resolved`              | Negated status (equivalent to `is:unresolved`)                | `!is:resolved`                       |
| `!is:unresolved`            | Negated status (equivalent to `is:resolved`)                  | `!is:unresolved`                     |
| `is:error`                  | Groups whose (max) severity is `error`                        | `is:error`                           |
| `is:warning`                | Groups whose (max) severity is `warning`                      | `is:warning`                         |
| `is:info` / `is:debug` / `is:fatal` | Other severity levels                                  | `is:info`                            |
| `!is:error`                 | Groups whose severity is *not* `error`                        | `!is:error`                          |
| `is:error,warning`          | Severity OR (comma-separated)                                 | `is:error,warning` or `is:error, warning` |
| `!is:error,warning`         | Negated severity OR                                           | `!is:error,warning`                  |
| `server_name:VALUE`         | Groups that have reports from this server/device              | `server_name:"eagle-618d24"`         |
| `tags.server_name:VALUE`    | Same as above (tag form)                                      | `tags.server_name:prod-box-7`        |
| `environment:VALUE`         | Filter by environment                                         | `environment:production`             |
| `tags.KEY:VALUE`            | Filter by any tag                                             | `tags.component:worker`              |
| Free text                   | Matches error type, message or culprit (FTS)                  | `TypeError` or `"payment failed"`    |

You can mix filters and free text:

- Unresolved errors from a specific device containing "timeout":
  `?query=is:unresolved server_name:eagle-618d24 timeout`
- Production errors with a particular tag:
  `?query=environment:production tags.region:eu-west PaymentError`
- All non-error, non-warning groups from a server:
  `?query=!is:error,warning server_name:foo`
- Negated status + free text:
  `?query=!is:resolved "payment failed"`

Negation (`!is:...`) is supported for both status and severity filters. Comma syntax provides OR semantics within a single `is:` or `!is:` clause (most useful for severities). Status negation is automatically inverted (e.g. `!is:resolved` behaves like `is:unresolved`). Last filter of a given type wins if duplicated.

### Other List Parameters

| Parameter | Description                                                                  | Example              |
| --------- | ---------------------------------------------------------------------------- | -------------------- |
| `status`  | Filter by status. When using `query`, prefer `is:unresolved` etc. inside it. | `?status=unresolved` |
| `resolved`| Simple status filter (true/false, resolved/unresolved, 1/0).                 | `?resolved=false`    |
| `since`   | Groups with `last_occurred_at` on or after this date                         | `?since=2026-05-01`  |
| `until`   | Groups with `last_occurred_at` on or before this date                        | `?until=2026-05-20`  |
| `limit`   | Number of groups to return (default 25, max 100)                             | `?limit=50`          |
| `cursor`  | Pagination cursor (use `next_cursor` from previous response)                 | `?cursor=12345`      |

Example for unresolved groups (using the simple `?resolved=` filter):

```sh
curl "https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups?resolved=false&limit=50" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

Example combining modern query syntax (with negation and severity OR) with time range and pagination:

```sh
curl "https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups?query=!is:resolved+is:error,warning+server_name:%22eagle-618d24%22&since=2026-05-01&limit=50" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

## Response Format

```json
{
  "groups": [
    {
      "id": 42,
      "project_id": 1,
      "error_type": "NoMethodError",
      "error_message": "undefined method `foo' for nil:NilClass",
      "culprit": "OrdersController#create",
      "fingerprint": "...",
      "severity": "error",
      "occurred_at": "2026-05-20T10:12:34Z",
      "first_occurred_at": "2026-05-20T10:12:34Z",
      "last_occurred_at": "2026-05-20T14:55:01Z",
      "reports_count": 17,
      "notes_count": 2,
      "resolved_at": null,
      "resolver_id": null,
      "muted_at": null,
      "muter_id": null,
      "muted_until": null,
      "muted_until_reports_count": null,
      "resolved": false,
      "muted": false,
      "created_at": "2026-05-20T10:12:34Z",
      "updated_at": "2026-05-20T14:55:01Z"
    }
  ],
  "next_cursor": 41,
  "has_more": true
}
```

See [Pagination](rest-api-02-pagination.md) for how to use `next_cursor` and `limit`.

The `severity` field on each group is the highest severity ever observed for reports in that group (`fatal`, `error`, `warning`, `info`, or `debug`).

The mute fields describe the group's current active mute:

- `muted` is `true` when notifications are currently suppressed.
- `muted_until` is set for time-based snoozes.
- `muted_until_reports_count` is set for occurrence-based mutes. It stores the
  total `reports_count` at which notifications resume, not the additional count
  originally requested.

To see per-occurrence details for a group (including `server_name`, `tags`, `environment`, user info, request context, etc.), use the [Reports](rest-api-06-reports.md) endpoints under the group.

## Resolve a Group

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/resolve \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Unresolve a Group

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/resolve \
  -X DELETE \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Mute a Group

Mute a group forever by omitting a request body:

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/mute \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Mute a group until a number of additional occurrences by passing a positive
`occurrences` value:

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/mute \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"occurrences": 10}'
```

If the group currently has `reports_count: 17`, the example above sets
`muted_until_reports_count` to `27`. Notifications resume when the group reaches
that total report count. Actions that only change state return `204 No Content`.

## Unmute a Group

Unmuting clears permanent, time-based, and occurrence-based mute conditions.

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/mute \
  -X DELETE \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Bulk Resolve

Resolve multiple groups in the same project. Groups that are already resolved are
skipped; the response reports how many groups were changed.

For bulk resolve, unresolve, mute, and unmute, the groups changed are the
`group_ids` in the request body.

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/bulk_resolve \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"group_ids": [123, 456, 789]}'
```

```json
{
  "processed": 3
}
```

## Bulk Unresolve

Re-open multiple resolved groups. Groups that are already unresolved are skipped.

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/bulk_resolve \
  -X DELETE \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"group_ids": [123, 456, 789]}'
```

```json
{
  "processed": 3
}
```

## Bulk Mute

Mute multiple groups in the same project. REST bulk mute creates permanent
mutes. Groups that are already muted are skipped.

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/bulk_mute \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"group_ids": [123, 456, 789]}'
```

```json
{
  "processed": 3
}
```

## Bulk Unmute

Unmute multiple groups. This clears permanent, time-based, and occurrence-based
mute conditions. Groups that are already unmuted are skipped.

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/bulk_mute \
  -X DELETE \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"group_ids": [123, 456, 789]}'
```

```json
{
  "processed": 3
}
```

## Bulk Merge

Merge multiple source groups into a target group. The target group is identified
by `GROUP_ID` in the URL; the request body lists the groups to merge into it.

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/groups/GROUP_ID/bulk_merge \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"group_ids": [456, 789]}'
```

```json
{
  "processed": 2,
  "merged_into_id": 123
}
```

The API rejects attempts to merge a group into itself or to merge groups that
have already been merged.
