# Projects

Projects are the starting point for most Telebugs MCP workflows. Use them to discover which Telebugs projects your account can access, then pass the project ID to group, report, and user tools.

`list_projects_tool` is often the first tool an AI calls after connecting. `list_project_users_tool` is useful when assigning an error group to a teammate.

## List Projects

**Tool:** `list_projects_tool`
**Scope required:** `telebugs.read`

Returns all active projects you have access to. No parameters are required.

### Example Response

```json
{
  "projects": [
    {
      "id": 1,
      "name": "Production",
      "platform": "Ruby",
      "timezone": "UTC",
      "web_url": "https://telebugs.example.com/projects/1",
      "source_repository_url": "https://github.com/example/payments",
      "source_default_branch": "main",
      "groups_count": 42,
      "reports_count": 1287,
      "muted": false,
      "muted_at": null,
      "muted_until": null
    },
    {
      "id": 2,
      "name": "Staging",
      "platform": "Ruby",
      "timezone": "UTC",
      "web_url": "https://telebugs.example.com/projects/2",
      "source_repository_url": null,
      "source_default_branch": "main",
      "groups_count": 17,
      "reports_count": 312
    }
  ]
}
```

Use the project `id` as `project_id` when calling tools such as `list_error_groups_tool` or `list_project_users_tool`.

`source_repository_url` never includes embedded URL credentials, query
parameters, or fragments. Configure repository metadata under
**Project Settings → Source repository** to enable source links in
`get_investigation_context_tool`.

## Agent-Assisted Project Setup

Open a new project's installation page and use the primary agent setup action:
**Copy setup for agent** when OAuth-connected with `telebugs.read` access, or
**Set up with agent** when Telebugs needs to explain the connection first.
Paste the identifier-only prompt into a repository-aware coding agent connected
to Telebugs MCP. The agent inspects the repository, installs the appropriate
official Sentry SDK, keeps the DSN in an environment variable, sends one marked
test exception, and asks Telebugs to verify receipt.

If no read-authorized OAuth MCP client is visible, the dashboard first explains
how to connect one. Users who configured MCP manually or with an API key can
use the **Already connected?** action. The manual **Copy DSN** path remains
available and does not require MCP.

The copied prompt never contains a DSN, account credential, MCP token, or
production event content.

### Get Project Setup

**Tool:** `get_project_setup_tool`<br>
**Scope required:** `telebugs.read`<br>
**Behavior:** read-only and non-destructive; each call creates a new marker

| Parameter    | Type    | Required | Description                         |
| ------------ | ------- | -------- | ----------------------------------- |
| `project_id` | integer | Yes      | Existing authorized Telebugs project |

The response is the authoritative setup contract for the agent. It contains:

- Project ID, name, platform, and canonical Telebugs URL
- Project DSN and the recommended `SENTRY_DSN` environment-variable name
- The official Sentry SDK instructions URL for the project's platform
- Confirmed supported and unsupported capability IDs
- A unique verification marker and the arguments for
  `verify_ingestion_tool`

The DSN is a project ingestion credential. Agents must place it in the returned
environment variable and must not commit it to source control. The tool never
returns account API keys, OAuth access tokens, refresh tokens, or MCP
credentials.

Example response, with the DSN shortened for display:

```json
{
  "project_id": 13,
  "name": "Storefront",
  "platform": "Ruby",
  "web_url": "https://telebugs.example.com/projects/13",
  "dsn": "https://project-token@telebugs.example.com/api/v1/sentry_errors/13",
  "dsn_environment_variable": "SENTRY_DSN",
  "sdk_capabilities": {
    "supported": [
      { "id": "error_reporting" },
      { "id": "event_tags" }
    ],
    "unsupported": [
      { "id": "tracing" },
      { "id": "profiling" }
    ]
  },
  "verification_marker": "telebugs-setup-0123456789abcdef0123456789abcdef"
}
```

Agents must configure only the capabilities returned as supported. They must
not infer support from the broader Sentry product or enable tracing and
profiling.

### Verify Ingestion

**Tool:** `verify_ingestion_tool`<br>
**Scope required:** `telebugs.read`<br>
**Behavior:** read-only, idempotent, and non-destructive

| Parameter             | Type    | Required | Description                         |
| --------------------- | ------- | -------- | ----------------------------------- |
| `project_id`          | integer | Yes      | Project returned by the setup tool  |
| `verification_marker` | string  | Yes      | Exact marker returned by that call  |

The agent attaches the exact marker to its safe test exception message or the
`telebugs.verification_marker` string tag, flushes the SDK transport when
needed, and calls this tool. Telebugs searches only that authorized project and
only reports ingested during the bounded 30-minute window.

A successful result contains the matching report and event identity:

```json
{
  "received": true,
  "report_id": 304578,
  "event_id": "34de0458a4ea42159547f7a4df273941",
  "received_at": "2026-08-15T13:24:06Z",
  "web_url": "https://telebugs.example.com/errors/193/reports/304578"
}
```

When no match is found, `received` is `false`, report fields are `null`, and
`next_action` tells the agent to send the exact marked event, flush the SDK,
and retry within the verification window. The tool is intentionally not a
general-purpose event search.

## Mute Project

**Tool:** `mute_project_tool`
**Scope required:** `telebugs.write`
**Admin required:** Yes

Mutes every current error group and automatically mutes new groups. Omit
`snooze_until` to mute forever, or pass a future ISO8601 datetime for a
temporary mute. Reports continue to be recorded.

| Parameter       | Type    | Required | Description                              |
| --------------- | ------- | -------- | ---------------------------------------- |
| `project_id`    | integer | Yes      | Project to mute                          |
| `snooze_until`  | string  | No       | Future ISO8601 automatic-expiration time |

```json
{
  "project_id": 1,
  "snooze_until": "2026-08-01T18:00:00Z"
}
```

## Stop Automatically Muting New Errors

**Tool:** `unmute_project_tool`
**Scope required:** `telebugs.write`
**Admin required:** Yes

Pass `project_id` to stop future groups from inheriting the project mute.
Existing groups remain muted until their deadline or until explicitly unmuted.

## List Project Users

**Tool:** `list_project_users_tool`
**Scope required:** `telebugs.read`

Returns active users who have access to a specific project. Use this to discover valid `user_id` values before assigning error groups.

### Parameters

| Parameter    | Type    | Required | Default      |
| ------------ | ------- | -------- | ------------ |
| `project_id` | integer | Yes      | -            |
| `limit`      | integer | No       | 25 (max 100) |
| `cursor`     | integer | No       | -            |

### Example Response

```json
{
  "users": [
    {
      "id": 3,
      "name": "Sunshine",
      "email_address": "sunshine@example.com"
    },
    {
      "id": 7,
      "name": "Kyrylo",
      "email_address": "kyrylo@example.com"
    }
  ],
  "next_cursor": null,
  "has_more": false
}
```

If more results are available, `has_more` will be `true` and `next_cursor` will contain the cursor for the next request. See [Pagination](telebugs-mcp-03-pagination.md).

### Common Use Case

Before calling `assign_error_group_tool`, first call `list_project_users_tool` with the relevant `project_id` to get valid user IDs.

## Error Responses

See [Errors](telebugs-mcp-08-errors.md) for general error handling.

Common error for this resource:

```json
{
  "content": [
    {
      "type": "text",
      "text": "Project not found or access denied"
    }
  ],
  "isError": true
}
```
