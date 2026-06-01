# Problems

The Telebugs REST API uses [RFC 9457 Problem Details](https://www.rfc-editor.org/rfc/rfc9457.html) for all error responses.

Each problem is identified by a `type` URI. These URIs are dereferenceable and point directly to the human-readable documentation for that problem type (the pages in this section).

## Defined Problem Types

| Type URI (used in responses)                                      | Title             | Status Code             | Description |
|-------------------------------------------------------------------|-------------------|-------------------------|-------------|
| `https://docs.telebugs.com/rest-api/problems/unauthorized`        | Unauthorized      | 401 Unauthorized        | The request did not include valid authentication credentials. |
| `https://docs.telebugs.com/rest-api/problems/validation-error`    | Validation Failed | 422 Unprocessable Content | The submitted data failed validation. |

When no more specific problem type applies, the API uses `about:blank` as the type (per RFC 9457 §4.2.1). In this case the `title` will be the standard HTTP status phrase.

## Client Guidance

- Always examine the `type` field first for robust, forward-compatible error handling.
- The `detail` field and any extension members (such as `errors`) contain occurrence-specific information.
- All problem responses use `Content-Type: application/problem+json`.

Browse the individual problem pages below for causes, remedies, and full example responses.
