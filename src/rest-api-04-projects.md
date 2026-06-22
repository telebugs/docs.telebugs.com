# Projects

You can manage projects through the API.

## List Projects

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

Response includes `next_cursor` and `has_more` for pagination.

### Filtering Projects

Use `name` to check for an exact project name. This is the recommended way to
test whether a project already exists before creating it.

```sh
curl "https://your-telebugs-instance.com/api/telebugs/v1/projects?name=Production" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

The filter only returns projects your API key can access and can be combined
with `limit` and `cursor`.

## Create a Project

When you create a project, the response includes the `token` so you can start sending errors immediately.

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name": "Production",
    "platform": "Ruby",
    "timezone": "UTC"
  }'
```

Response (`201 Created`) — fields at the top level, including the project `token`:

```json
{
  "id": 1,
  "name": "Production",
  "platform": "Ruby",
  "timezone": "UTC",
  "token": "tlbgs_...",
  "groups_count": 0,
  "reports_count": 0,
  "created_at": "2026-05-20T10:00:00Z",
  "updated_at": "2026-05-20T10:00:00Z"
}
```

## Get a Single Project

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

Returns the project object with fields at the top level (same shape as create).

## Update a Project

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID \
  -X PATCH \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name": "Production v2",
    "timezone": "Europe/Berlin"
  }'
```

Returns the updated project object with fields at the top level.

## Delete a Project

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID \
  -X DELETE \
  -H "Authorization: Bearer YOUR_API_KEY"
```
