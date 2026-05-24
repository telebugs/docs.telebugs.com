# Pagination

Most list endpoints in the Telebugs API use **cursor-based pagination**.

This approach is efficient and works well even with large datasets.

## How Pagination Works

List endpoints return two important fields:

- `next_cursor` — The ID you should use to fetch the next page
- `has_more` — A boolean indicating whether more results are available

### Example Response

````json
{
  "projects": [...],
  "next_cursor": 12345,
  "has_more": true
}

## Fetching the Next Page

To get the next page, pass the `next_cursor` value as the `cursor` parameter:

```sh
curl "https://your-telebugs-instance.com/api/telebugs/v1/projects?cursor=12345" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
````

## Controlling Page Size

You can control how many items are returned using the `limit` parameter:

```
curl "https://your-telebugs-instance.com/api/telebugs/v1/groups?limit=50" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Limits

- Default limit: `25`
- Maximum limit: `100`

If you request a higher value, it will be capped at `100`.

## Best Practices

- Always check `has_more` before making another request.
- Use `next_cursor` exactly as returned — do not modify it.
