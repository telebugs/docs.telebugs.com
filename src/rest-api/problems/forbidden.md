# Forbidden

## Forbidden

**Problem type**

`forbidden`

**Type URI**

`https://docs.telebugs.com/rest-api/problems/forbidden.html`

**Status code**

`403 Forbidden`

## Reasons

The server understood the request but refuses to authorize it.

This problem occurs when:

1. The authenticated user does not have the required privileges (e.g. admin role).
2. The user does not have access to the requested resource (e.g. a project or app they are not a member of).

## Remedy

- Use an API key belonging to a user with the necessary role or membership.
- For admin-only operations, ensure the key is for an admin user (see Account Settings → Team).

## Example Problem Document

```http
HTTP/1.1 403 Forbidden
Content-Type: application/problem+json

{
  "type": "https://docs.telebugs.com/rest-api/problems/forbidden.html",
  "title": "Forbidden",
  "status": 403,
  "detail": "Admin access required"
}
```

The `detail` value explains the specific reason.
