# MCP Pagination

Several list tools in Telebugs MCP use cursor-based pagination:

- `list_error_groups_tool`
- `list_reports_tool`
- `list_project_users_tool`

This approach is efficient for large result sets and avoids the problems of offset-based pagination, such as skipped or duplicate results when data changes between pages.

## How It Works

Paginated Telebugs tools include pagination fields in the response:

```json
{
  "groups": [
    { "id": 42, "error_type": "NoMethodError" }
  ],
  "next_cursor": 8472,
  "has_more": true
}
```

To fetch the next page, pass the `next_cursor` value back to the same tool as `cursor`:

```json
{
  "cursor": 8472
}
```

Use `has_more` as the reliable signal. When `has_more` is `false`, you have reached the end of the results and `next_cursor` is `null`.

## Page Size

Control how many results are returned per request using the `limit` parameter.

| Tool                      | Default | Maximum | Recommended for most cases |
| ------------------------- | ------- | ------- | -------------------------- |
| `list_error_groups_tool`  | 25      | 100     | 25-50                      |
| `list_reports_tool`       | 25      | 100     | 25-50                      |
| `list_project_users_tool` | 25      | 100     | 25                         |

Values above the maximum are automatically capped.

## Example: Paginating Error Groups

Here is a typical pagination flow:

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
  "groups": [
    { "id": 42, "error_type": "NoMethodError" }
  ],
  "next_cursor": 3921,
  "has_more": true
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
  "groups": [
    { "id": 41, "error_type": "ArgumentError" }
  ],
  "next_cursor": null,
  "has_more": false
}
```

`has_more: false` means you are done, even if the returned page happens to contain exactly `limit` items.

## Best Practices

- **Use the cursor exactly as returned** - Do not modify or guess cursor values.
- **Stop when `has_more` is `false`** - This is the reliable way to know you have reached the end.
- **Filter first, then paginate** - Use `query`, `status`, `severity`, `since`, or `project_id` to reduce the total number of results before paging.
- **Do not infer availability from page size** - A full page can still be the last page.
- **Do not over-fetch** - For AI tools, it is usually better to fetch smaller pages (25-50) and let the model decide if it needs more data.

> **Tip:** If you are building prompts for AI tools, encourage them to use filters before falling back to pagination. This leads to faster, more relevant results.
