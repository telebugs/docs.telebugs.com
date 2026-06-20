# Apps

Apps are used to organize multiple projects (for example, a frontend and a
backend app).

> **Note:** Most App operations require admin access.

## List Apps

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/apps \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

## Create an App

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/apps \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name": "Web Platform",
    "project_ids": [123, 456]
  }'
```

Returns the created app with fields at the top level (`id`, `name`, `project_ids`, etc.).

## Update an App

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/apps/APP_ID \
  -X PATCH \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name": "Web Platform v2"
  }'
```

Returns the updated app with fields at the top level.

## Delete an App

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/apps/APP_ID \
  -X DELETE \
  -H "Authorization: Bearer YOUR_API_KEY"
```

> **Note:** Deleting an app will ungroup its projects but will not delete the projects themselves.
