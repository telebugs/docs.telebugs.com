# Projects

You can manage projects through the API.

## List Projects

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

Response includes `next_cursor` and `has_more` for pagination.

## Create a Project

When you create a project, the response includes the `token` so you can start sending errors immediately.

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "project": {
      "name": "Production",
      "platform": "Ruby",
      "timezone": "UTC"
    }
  }'
```

## Get a Single Project

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

## Update a Project

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID \
  -X PATCH \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "project": {
      "name": "Production v2",
      "timezone": "Europe/Berlin"
    }
  }'
```

## Delete a Project

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID \
  -X DELETE \
  -H "Authorization: Bearer YOUR_API_KEY"
```
