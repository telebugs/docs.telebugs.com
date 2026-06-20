# MCP Pagination

Several list tools in Telebugs MCP use **cursor-based pagination**:

- `list_error_groups_tool`
- `list_project_users_tool`
- `list_notes_tool`

This approach is efficient for large result sets and avoids the problems of offset-based pagination (skipped or duplicate results when data changes between pages).

## How It Works

When a list tool has more results available, the response includes a `next_cursor` value inside `_meta`:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "[{...}, {...}, {...}]"
      }
    ],
    "_meta": {
      "next_cursor": 8472
    }
  }
}
```

To fetch the next page, pass the `cursor` value back to the **same tool**:

```json
{
  "cursor": 8472
}
```

When no `next_cursor` is present in `_meta`, you have reached the end of the results.

## Page Size

Control how many results are returned per request using the `limit` parameter.

| Tool                      | Default | Maximum | Recommended for most cases |
| ------------------------- | ------- | ------- | -------------------------- |
| `list_error_groups_tool`  | 25      | 100     | 25–50                      |
| `list_notes_tool`         | 50      | 100     | 50                         |
| `list_project_users_tool` | 25      | 100     | 25                         |

Values above the maximum are automatically capped.

## Example: Paginating Error Groups

Here's a typical pagination flow:

**First request** (no cursor):

```json
{
  "project_id": 1,
  "status": "unresolved",
  "limit": 25
}
```

**First response** (has more results):

```json
{
  "_meta": {
    "next_cursor": 3921
  },
  "content": [
    {
      "type": "text",
      "text": "[{group1}, {group2}, ..., {group25}]"
    }
  ]
}
```

**Second request** (pass the cursor):

```json
{
  "project_id": 1,
  "status": "unresolved",
  "limit": 25,
  "cursor": 3921
}
```

**Second response** (no more results):

```json
{
  "content": [
    {
      "type": "text",
      "text": "[{group26}, {group27}]"
    }
  ]
}
```

No `next_cursor` means you're done.

## Best Practices

- **Use the cursor exactly as returned** — Do not modify or guess cursor values.
- **Stop when `next_cursor` is missing** — This is the only reliable way to know you've reached the end.
- **Filter first, then paginate** — Use `query`, `status`, `since`, or `project_id` to reduce the total number of results before paging.
- **Don't over-fetch** — For AI tools, it's usually better to fetch smaller pages (25–50) and let the model decide if it needs more data.
- **Combine with filters aggressively** — For example, use `since` + `status:unresolved` to avoid paging through years of historical data.

> **Tip:** If you're building prompts for AI tools, encourage them to use filters (`query`, `status`, `since`) before falling back to pagination. This leads to faster, more relevant results.
