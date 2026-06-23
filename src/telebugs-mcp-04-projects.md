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
      "groups_count": 42,
      "reports_count": 1287
    },
    {
      "id": 2,
      "name": "Staging",
      "platform": "Ruby",
      "timezone": "UTC",
      "groups_count": 17,
      "reports_count": 312
    }
  ]
}
```

Use the project `id` as `project_id` when calling tools such as `list_error_groups_tool` or `list_project_users_tool`.

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
