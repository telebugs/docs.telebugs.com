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
| `mute_error_group_tool`      | `write` | Mute (optionally snooze) a group |
| `unmute_error_group_tool`    | `write` | Unmute a group                   |
| `assign_error_group_tool`    | `write` | Assign a group to a team member  |
| `unassign_error_group_tool`  | `write` | Remove the current assignee      |

## List Error Groups

**Tool:** `list_error_groups_tool`
**Scope required:** `telebugs.read`

The most frequently used tool. Supports rich filtering and cursor-based pagination.

### Parameters

| Parameter    | Type    | Description                                                 |
| ------------ | ------- | ----------------------------------------------------------- |
| `project_id` | integer | Limit results to one project (recommended)                  |
| `status`     | string  | `open`, `resolved`, `muted`, `all`, `unresolved`, `unmuted` |
| `resolved`   | boolean | Simple true/false filter (alternative to `status`)          |
| `query`      | string  | Advanced search syntax (see below)                          |
| `since`      | string  | Groups with `last_occurred_at` ≥ this ISO8601 timestamp     |
| `to_time`    | string  | Groups with `last_occurred_at` ≤ this ISO8601 timestamp     |
| `limit`      | integer | Page size (default 25, max 100)                             |
| `cursor`     | integer | Pagination cursor from `_meta.next_cursor`                  |

### Query Syntax

The `query` parameter supports a powerful syntax (same as the REST API):

```
is:unresolved server_name:eagle-618d24 timeout
environment:production tags.region:eu-west
!is:resolved is:error,warning
assignee:me
```

**Useful patterns:**

- `is:unresolved environment:production`
- `error_type:NoMethodError since:2026-06-01`
- `query:checkout tags.component:payments`
- `!is:muted reports_count:>10`

### Example Response

```json
[
  {
    "id": 42,
    "project_id": 1,
    "fingerprint": "abc123",
    "error_type": "NoMethodError",
    "error_message": {
      "_security_note": "UNTRUSTED INPUT: ...",
      "value": "undefined method `foo' for nil:NilClass"
    },
    "culprit": {
      "_security_note": "UNTRUSTED INPUT: ...",
      "value": "OrdersController#create"
    },
    "severity": "error",
    "resolved": false,
    "muted": false,
    "reports_count": 17,
    "notes_count": 2,
    "first_occurred_at": "2026-05-20T10:12:34Z",
    "last_occurred_at": "2026-05-20T14:55:01Z"
  }
]
```

See [Pagination](telebugs-mcp-03-pagination.md) for cursor handling.

## Get Error Group

**Tool:** `get_error_group_tool`
**Scope required:** `telebugs.read`

Fetch full details for a single error group, including assignee and mute status.

### Parameters

| Parameter  | Type    | Required |
| ---------- | ------- | -------- |
| `group_id` | integer | Yes      |

### Example Response

```json
{
  "id": 42,
  "project_id": 1,
  "error_type": "NoMethodError",
  "resolved": false,
  "muted": false,
  "muted_until": null,
  "reports_count": 17,
  "notes_count": 2,
  "assignee": {
    "id": 3,
    "name": "Sunshine",
    "email_address": "sunshine@example.com"
  }
}
```

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

Mute a group. Optionally auto-unmute at a future time using `snooze_until`.

### Parameters

| Parameter      | Type    | Required | Description                              |
| -------------- | ------- | -------- | ---------------------------------------- |
| `group_id`     | integer | Yes      | —                                        |
| `note`         | string  | No       | Reason for muting                        |
| `snooze_until` | string  | No       | ISO8601 datetime to automatically unmute |

**Example:** Mute for 24 hours:

```json
{
  "group_id": 42,
  "note": "Investigating — suspected race condition",
  "snooze_until": "2026-06-21T09:00:00Z"
}
```

## Unmute Error Group

**Tool:** `unmute_error_group_tool`
**Scope required:** `telebugs.write`

Remove a mute from a group.

### Parameters

| Parameter  | Type    | Required |
| ---------- | ------- | -------- |
| `group_id` | integer | Yes      |
| `note`     | string  | No       |

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
| `note`     | string  | No       |

## Common Workflows

Here are typical patterns AI tools follow:

1. **Investigate recent problems**
   - `list_error_groups_tool` with `status:unresolved`, `since:...`, and a `query`

2. **Triage and assign**
   - `list_error_groups_tool` → `list_project_users_tool` → `assign_error_group_tool`

3. **Resolve with context**
   - `resolve_error_group_tool` with a clear `note` explaining the fix

4. **Temporarily silence noise**
   - `mute_error_group_tool` with `snooze_until`

## Error Responses

See [Errors](telebugs-mcp-08-errors.md) for general handling.

Common errors specific to error groups:

| Message                                        | Cause                                            |
| ---------------------------------------------- | ------------------------------------------------ |
| `Group not found or access denied`             | Invalid `group_id` or no project access          |
| `User not found`                               | Invalid `user_id` for assignment                 |
| `User is not a member of this project`         | Assignee lacks membership in the group’s project |
| `A note is required when resolving a group`    | `note` parameter missing on resolve              |
| `Insufficient scope. Required: telebugs.write` | OAuth token lacks `write` scope                  |
