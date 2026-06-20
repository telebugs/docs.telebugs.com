# Getting Started with the REST API

Telebugs exposes a REST API that lets you manage projects, groups, reports,
apps, webhooks, and users programmatically.

The API is designed to be simple, pragmatic, and easy to use from scripts,
internal tools, or other services.

## Getting Your API Key

1. Go to **Account Settings**.
2. Open the **API access** section.
3. Copy your API key.

You'll need this key to authenticate all requests.

## Base URL

All API requests are made to:

```sh
https://your-telebugs-instance.com/api/telebugs/v1
```

## Content Type

The API accepts and returns JSON:

```sh
Content-Type: application/json
Accept: application/json
```

## Request and Response Conventions

Telebugs uses flat JSON — no nested resource wrappers like `{ "project": { ... } }`.

### Request bodies

Pass attributes at the top level of the JSON body:

```json
{
  "name": "Production",
  "platform": "Ruby",
  "timezone": "UTC"
}
```

Unrecognized keys (including legacy wrapper keys such as `project`) are ignored.

### List responses

Collections use a plural key plus pagination metadata:

```json
{
  "projects": [ { "id": 1, "name": "Production", ... } ],
  "next_cursor": 42,
  "has_more": true
}
```

### Single-resource responses

`GET`, `POST`, and `PATCH` on a single resource return its fields at the top level —
not wrapped under a singular key:

```json
{
  "id": 1,
  "name": "Production",
  "platform": "Ruby",
  "timezone": "UTC"
}
```

Nested objects inside a resource (for example `user` or `request` on a report) are
part of the resource shape, not a wrapper around it.

### Write responses

Actions that only change state (resolve, mute, delete, etc.) return `204 No Content`
with an empty body. Validation and authorization failures return
[RFC 9457 problem details](rest-api-03-errors.md).

## Your First Request

Here's a simple example that lists your projects:

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```
