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
  "muted": false,
  "muted_at": null,
  "muted_until": null,
  "muter_id": null,
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

## Mute a Project

Project muting requires an admin API key. It mutes all current error groups and
automatically mutes new groups. Reports continue to be recorded.

Omit `snooze_until` to mute forever:

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/mute \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY"
```

To mute temporarily, pass a future ISO8601 timestamp:

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/mute \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"snooze_until": "2026-08-01T18:00:00Z"}'
```

A successful request returns `204 No Content`. Project responses expose
`muted`, `muted_at`, `muted_until`, and `muter_id`.

## Stop Automatically Muting New Errors

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/mute \
  -X DELETE \
  -H "Authorization: Bearer YOUR_API_KEY"
```

This stops future groups from inheriting the project mute. Existing groups
remain muted until their deadline or until explicitly unmuted.

## Notification Severity Setting

An admin API key can read or update whether a project sends notifications only
for `error` and `fatal` reports:

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/notification_settings \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/notification_settings \
  -X PATCH \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"error_and_fatal_notifications_only": true}'
```

Both responses use this shape:

```json
{"error_and_fatal_notifications_only":true}
```

## Hosted Source Map Origins

Hosted source map origins are project-scoped and require an admin API key. List
the exact public HTTPS origins authorized for a project:

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/hosted_sourcemap_origins \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

Authorize an origin:

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/hosted_sourcemap_origins \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"origin":"https://assets.example.com"}'
```

Origins are canonicalized and must be exact public HTTPS origins without a path,
query, fragment, credentials, wildcard, or IP address. Each project can authorize
up to ten origins. A successful create returns `201 Created` with the origin:

```json
{
  "id": 7,
  "origin": "https://assets.example.com",
  "created_at": "2026-08-13T10:00:00Z",
  "updated_at": "2026-08-13T10:00:00Z"
}
```

Remove an origin with `DELETE`. This also purges hosted maps cached through the
origin:

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/hosted_sourcemap_origins/ORIGIN_ID \
  -X DELETE \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Delete a Project

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID \
  -X DELETE \
  -H "Authorization: Bearer YOUR_API_KEY"
```
