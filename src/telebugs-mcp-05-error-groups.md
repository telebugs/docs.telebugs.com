# Error Groups

Error groups represent **deduplicated errors**. They are the core unit you interact with in Telebugs — not individual reports.

MCP gives AI tools powerful capabilities to list, inspect, filter, and manage error groups directly.

## Available Tools

| Tool                         | Scope   | Purpose                          |
| ---------------------------- | ------- | -------------------------------- |
| `list_error_groups_tool`     | `read`  | Search and filter error groups   |
| `get_error_group_tool`       | `read`  | Fetch details for a single group |
| `resolve_error_group_tool`   | `write` | Mark a group as resolved         |
| `unresolve_error_group_tool` | `write` | Re-open a resolved group         |
| `mute_error_group_tool`      | `write` | Mute a group forever, until a time, or until more occurrences |
| `unmute_error_group_tool`    | `write` | Unmute a group                   |
| `bulk_resolve_error_groups_tool` | `write` | Resolve multiple groups      |
| `bulk_mute_error_groups_tool`    | `write` | Mute multiple groups         |
| `bulk_merge_error_groups_tool`   | `write` | Merge multiple groups        |
| `assign_error_group_tool`    | `write` | Assign a group to a team member  |
| `unassign_error_group_tool`  | `write` | Remove the current assignee      |

## List Error Groups

**Tool:** `list_error_groups_tool`
**Scope required:** `telebugs.read`

The most frequently used tool. Supports rich filtering and cursor-based pagination.

By default, low-severity telemetry groups are excluded: `list_error_groups_tool` returns `fatal`, `error`, and `warning` severities unless you ask for another severity. Use `severity: "all"` to include everything, or pass `severity: "info"`, `"debug"`, or `"sample_level"` when you specifically want low-severity telemetry.

### Parameters

| Parameter    | Type    | Description                                                 |
| ------------ | ------- | ----------------------------------------------------------- |
| `project_id` | integer | Limit results to one project (recommended)                  |
| `status`     | string  | `open`, `resolved`, `muted`, `all`, `unresolved`, `unmuted` |
| `resolved`   | boolean | Simple true/false filter (alternative to `status`)          |
| `query`      | string  | Advanced search syntax (see below)                          |
| `since`      | string  | Groups with `last_occurred_at` >= this ISO8601 timestamp    |
| `to_time`    | string  | Groups with `last_occurred_at` <= this ISO8601 timestamp    |
| `limit`      | integer | Page size (default 25, max 100)                             |
| `cursor`     | integer | Pagination cursor from `next_cursor`                        |
| `severity`   | string  | `all`, `fatal`, `error`, `warning`, `info`, `debug`, `sample_level` |
| `verbose`    | boolean | Use the verbose untrusted-data response format           |

If `query` already contains a severity token, such as `is:info` or `severity:debug`, that query filter takes precedence over the default actionable-severity filter.

### Query Syntax

The `query` parameter supports a powerful syntax (same as the REST API):

```
is:unresolved server_name:eagle-618d24 timeout
environment:production tags.region:eu-west
!is:resolved is:error,warning
severity:info assignee:me
```

**Useful patterns:**

- `is:unresolved environment:production`
- `error_type:NoMethodError since:2026-06-01`
- `severity:info Burn-in starting`
- `query:checkout tags.component:payments`
- `!is:muted reports_count:>10`

### Example Response

```json
{
  "_security_note": "UNTRUSTED INPUT: This value came from the errored application...",
  "groups": [
    {
      "id": 42,
      "project_id": 1,
      "fingerprint": "abc123",
      "error_type": "NoMethodError",
      "error_message": "undefined method `foo' for nil:NilClass",
      "culprit": "OrdersController#create",
      "severity": "error",
      "resolved": false,
      "muted": false,
      "muted_until": null,
      "muted_until_reports_count": null,
      "reports_count": 17,
      "notes_count": 2,
      "first_occurred_at": "2026-05-20T10:12:34Z",
      "last_occurred_at": "2026-05-20T14:55:01Z",
      "untrusted": true,
      "untrusted_fields": ["error_message", "culprit"]
    }
  ],
  "next_cursor": null,
  "has_more": false
}
```

See [Pagination](telebugs-mcp-03-pagination.md) for cursor handling.

## Get Error Group

**Tool:** `get_error_group_tool`
**Scope required:** `telebugs.read`

Fetch full details for a single error group, including assignee, mute status, and recent report IDs.

### Parameters

| Parameter  | Type    | Required | Description                                       |
| ---------- | ------- | -------- | ------------------------------------------------- |
| `group_id` | integer | Yes      | Error group ID                                    |
| `verbose`  | boolean | No       | Use the verbose untrusted-data response format |

### Example Response

```json
{
  "_security_note": "UNTRUSTED INPUT: This value came from the errored application...",
  "id": 42,
  "project_id": 1,
  "fingerprint": "abc123",
  "error_type": "NoMethodError",
  "error_message": "undefined method `foo' for nil:NilClass",
  "culprit": "OrdersController#create",
  "severity": "error",
  "resolved": false,
  "muted": false,
  "muted_until": null,
  "muted_until_reports_count": null,
  "reports_count": 17,
  "recent_report_ids": [123, 122, 121],
  "notes_count": 2,
  "first_occurred_at": "2026-05-20T10:12:34Z",
  "last_occurred_at": "2026-05-20T14:55:01Z",
  "assignee": {
    "id": 3,
    "name": "Sunshine",
    "email_address": "sunshine@example.com"
  },
  "untrusted": true,
  "untrusted_fields": ["error_message", "culprit"]
}
```

Use `recent_report_ids` as a quick way to fetch individual occurrences with [`get_report_tool`](telebugs-mcp-06-reports.md). For complete pagination through a group's reports, use [`list_reports_tool`](telebugs-mcp-06-reports.md). Group IDs and report IDs are separate IDs; do not pass a `group_id` to `get_report_tool`.

## Resolve Error Group

**Tool:** `resolve_error_group_tool`
**Scope required:** `telebugs.write`

Mark an error group as resolved. **A note is required.**

### Parameters

| Parameter  | Type    | Required |
| ---------- | ------- | -------- |
| `group_id` | integer | Yes      |
| `note`     | string  | Yes      |

**Example note:** `"Fixed in deploy v1.4.2 (PR #847)"`

## Unresolve Error Group

**Tool:** `unresolve_error_group_tool`
**Scope required:** `telebugs.write`

Re-open a previously resolved group.

### Parameters

| Parameter  | Type    | Required |
| ---------- | ------- | -------- |
| `group_id` | integer | Yes      |
| `note`     | string  | No       |

## Mute Error Group

**Tool:** `mute_error_group_tool`
**Scope required:** `telebugs.write`

Mute a group forever, until a specific time, or until a number of additional
occurrences.

Omit both `snooze_until` and `occurrences` to mute forever. Use `snooze_until`
for a time-based snooze, or `occurrences` to resume notifications after the
next N reports in the group. Pass one condition at a time; if both are supplied,
Telebugs applies the occurrence-based mute.

### Parameters

| Parameter      | Type    | Required | Description                              |
| -------------- | ------- | -------- | ---------------------------------------- |
| `group_id`     | integer | Yes      | Error group to mute                      |
| `note`         | string  | No       | Reason for muting                        |
| `snooze_until` | string  | No       | ISO8601 datetime to automatically unmute |
| `occurrences`  | integer | No       | Additional occurrences before notifications resume |

**Example:** Mute for 24 hours:

```json
{
  "group_id": 42,
  "note": "Investigating - suspected race condition",
  "snooze_until": "2026-06-21T09:00:00Z"
}
```

**Example:** Mute until 10 more occurrences:

```json
{
  "group_id": 42,
  "note": "Noisy upstream timeout",
  "occurrences": 10
}
```

If the group currently has `reports_count: 17`, the occurrence example above
sets `muted_until_reports_count` to `27`.

### Example Response

```json
{
  "muted": true,
  "muted_until": null,
  "muted_until_reports_count": 27
}
```

## Unmute Error Group

**Tool:** `unmute_error_group_tool`
**Scope required:** `telebugs.write`

Remove a mute from a group. This clears permanent, time-based, and
occurrence-based mute conditions.

### Parameters

| Parameter  | Type    | Required |
| ---------- | ------- | -------- |
| `group_id` | integer | Yes      |

## Bulk Resolve Error Groups

**Tool:** `bulk_resolve_error_groups_tool`
**Scope required:** `telebugs.write`

Resolve multiple error groups at once. A note is required and is added to each
processed group. Groups that are already resolved are skipped.

### Parameters

| Parameter   | Type             | Required | Description                    |
| ----------- | ---------------- | -------- | ------------------------------ |
| `group_ids` | array of integer | Yes      | Error groups to resolve        |
| `note`      | string           | Yes      | Context added to each resolved group |

### Example

```json
{
  "group_ids": [42, 43, 44],
  "note": "Fixed by deploy 2026.06.22"
}
```

### Example Response

```json
{
  "success": true,
  "processed": 3,
  "group_ids": [42, 43, 44]
}
```

## Bulk Mute Error Groups

**Tool:** `bulk_mute_error_groups_tool`
**Scope required:** `telebugs.write`

Mute multiple error groups at once. Groups that are already muted are skipped.
Optionally provide `snooze_until` to automatically unmute them later. Bulk MCP
mute does not support occurrence-based thresholds; use `mute_error_group_tool`
for that.

### Parameters

| Parameter      | Type             | Required | Description                              |
| -------------- | ---------------- | -------- | ---------------------------------------- |
| `group_ids`    | array of integer | Yes      | Error groups to mute                     |
| `note`         | string           | No       | Reason for muting                        |
| `snooze_until` | string           | No       | ISO8601 datetime to automatically unmute |

### Example

```json
{
  "group_ids": [42, 43, 44],
  "note": "Known noisy downstream timeout",
  "snooze_until": "2026-06-23T09:00:00Z"
}
```

### Example Response

```json
{
  "success": true,
  "processed": 3,
  "group_ids": [42, 43, 44]
}
```

## Bulk Merge Error Groups

**Tool:** `bulk_merge_error_groups_tool`
**Scope required:** `telebugs.write`

Merge multiple source groups into one target group. Use this when several groups
represent the same underlying error and should share one history going forward.

### Parameters

| Parameter         | Type             | Required | Description                       |
| ----------------- | ---------------- | -------- | --------------------------------- |
| `target_group_id` | integer          | Yes      | Group that receives merged groups |
| `group_ids`       | array of integer | Yes      | Source groups to merge            |

### Example

```json
{
  "target_group_id": 42,
  "group_ids": [43, 44]
}
```

### Example Response

```json
{
  "success": true,
  "processed": 2,
  "merged_into_id": 42
}
```

The tool rejects attempts to merge the target group into itself or to merge
groups that have already been merged.

## Assign Error Group

**Tool:** `assign_error_group_tool`
**Scope required:** `telebugs.write`

Assign an error group to a team member.

> **Important:** The assignee must be a member of the group's project. Use [`list_project_users_tool`](telebugs-mcp-04-projects.md) first to discover valid `user_id` values.

### Parameters

| Parameter  | Type    | Required |
| ---------- | ------- | -------- |
| `group_id` | integer | Yes      |
| `user_id`  | integer | Yes      |
| `note`     | string  | No       |

## Unassign Error Group

**Tool:** `unassign_error_group_tool`
**Scope required:** `telebugs.write`

Remove the current assignee from a group.

### Parameters

| Parameter  | Type    | Required |
| ---------- | ------- | -------- |
| `group_id` | integer | Yes      |

## Common Workflows

Here are typical patterns AI tools follow:

1. **Investigate recent problems**
   - `list_error_groups_tool` with `status:unresolved`, `since:...`, and a `query`

2. **Triage and assign**
   - `list_error_groups_tool` → `list_project_users_tool` → `assign_error_group_tool`

3. **Resolve with context**
   - `resolve_error_group_tool` with a clear `note` explaining the fix
   - `bulk_resolve_error_groups_tool` when the same fix closed several groups

4. **Temporarily silence noise**
   - `mute_error_group_tool` with `snooze_until` for time-based snoozes
   - `mute_error_group_tool` with `occurrences` to resume after the next N reports
   - `bulk_mute_error_groups_tool` when several groups share the same noisy cause

5. **Merge duplicate groups**
   - `bulk_merge_error_groups_tool` with a target group and duplicate group IDs

## Error Responses

See [Errors](telebugs-mcp-08-errors.md) for general handling.

Common errors specific to error groups:

| Message                                        | Cause                                            |
| ---------------------------------------------- | ------------------------------------------------ |
| `Group not found or access denied`             | Invalid `group_id` or no project access          |
| `User not found`                               | Invalid `user_id` for assignment                 |
| `User is not a member of this project`         | Assignee lacks membership in the group’s project |
| `A note is required when resolving a group`    | `note` parameter missing on resolve              |
| `A note is required when resolving groups`     | `note` parameter missing on bulk resolve         |
| `Cannot merge an error into itself.`           | `target_group_id` included in `group_ids`        |
| `Cannot merge already merged errors.`          | A source group has already been merged           |
| `Insufficient scope. Required: telebugs.write` | OAuth token lacks `write` scope                  |
