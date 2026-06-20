# Projects

These tools let you discover the projects you have access to and the users within them.

`list_projects_tool` is often the first tool an AI calls after connecting.
`list_project_users_tool` is primarily used to find valid `user_id` values when assigning error groups.

## List Projects

**Tool:** `list_projects_tool`

Returns all projects you have access to. No parameters are required.

### Example Response

```json
[
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
```

Use the `id` as `project_id` when calling other tools (e.g. `list_error_groups_tool`, `list_project_users_tool`).

## List Project Users

**Tool:** `list_project_users_tool`

Returns users who have access to a specific project. Use this to discover valid `user_id` values for assigning error groups.

### Parameters

| Parameter    | Type    | Required | Default      |
| ------------ | ------- | -------- | ------------ |
| `project_id` | integer | Yes      | —            |
| `limit`      | integer | No       | 25 (max 100) |
| `cursor`     | integer | No       | —            |

### Example Response

```json
[
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
]
```

If more results are available, `_meta.next_cursor` will be included in the response (see [Pagination](telebugs-mcp-03-pagination.md)).

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
