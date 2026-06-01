# Unauthorized

## Unauthorized

**Problem type**

`unauthorized`

**Type URI**

`https://docs.telebugs.com/rest-api/problems/unauthorized`

**Status code**

`401 Unauthorized`

## Reasons

The server rejected the request because it could not authenticate the caller.

This problem occurs when:

1. The `Authorization` header is completely missing.
2. The header does not use the `Bearer` authentication scheme.
3. The provided API key is invalid, revoked, or malformed.

## Remedy

Supply a valid API key using the Bearer scheme:

```
Authorization: Bearer tlbgs_xxxxxxxxxxxxxxxxxxxxxxxx
```

Obtain or regenerate the key from **Account Settings → API** in the Telebugs interface.

## Example Problem Document

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/problem+json

{
  "type": "https://docs.telebugs.com/rest-api/problems/unauthorized",
  "title": "Unauthorized",
  "status": 401,
  "detail": "Invalid API key"
}
```

The `detail` value may vary (`"Missing API key"`, `"Invalid API key"`, etc.) while the `type` remains stable.
