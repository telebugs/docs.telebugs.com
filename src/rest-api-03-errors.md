# Errors

The Telebugs REST API conveys error information using [Problem Details for HTTP APIs (RFC 9457)](https://www.rfc-editor.org/rfc/rfc9457.html).

All error responses are served with the `application/problem+json` content type and follow a consistent, machine-readable structure.

## Problem Details Structure

A problem details response always contains:

- `type` — A URI that identifies the specific problem type. These URIs are stable and can be used by clients for programmatic handling or to retrieve documentation.
- `title` — A short, human-readable summary of the problem type. This value is consistent across occurrences of the same problem type.
- `status` — The HTTP status code for this occurrence of the problem.

Optional members include:

- `detail` — A human-readable explanation specific to this particular occurrence of the problem.
- Additional extension members defined by the problem type (for example, `errors` for validation failures).

Example response:

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

## Using Problem Types

Instead of parsing free-form error messages, clients should inspect the `type` member to determine the nature of the error. See the [full catalog of problem types](rest-api/problems/index.md) for the currently defined types and their semantics.

When the `type` is `about:blank` (the default when no specific type is indicated), the problem has no additional semantics beyond the HTTP status code itself.

## Common HTTP Status Codes

| Status | Meaning               | Typical Problem Type                                                      |
| ------ | --------------------- | ------------------------------------------------------------------------- |
| 401    | Unauthorized          | [unauthorized](rest-api/problems/unauthorized.md)                         |
| 404    | Not Found             | `about:blank` (generic)                                                   |
| 422    | Unprocessable Content | [validation-error](rest-api/problems/validation-error.md)                 |

## Best Practice

- Always inspect the HTTP status code first.
- For machine clients, key off the `type` URI rather than string matching on `title` or `detail`.
- For validation errors, examine the `errors` extension for field-specific messages.
- Include `Accept: application/problem+json` (or `Accept: application/json, application/problem+json`) to signal preference for this format.

This structure makes error handling robust and allows the API to evolve by adding new problem types without breaking existing clients.
