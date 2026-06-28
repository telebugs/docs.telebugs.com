# Validation Error

## Validation Failed

**Problem type**

`validation-error`

**Type URI**

`https://docs.telebugs.com/rest-api/problems/validation-error.html`

**Status code**

`422 Unprocessable Content`

## Reasons

The server understood the request but could not process it because the payload failed validation.

This typically happens on `POST`, `PATCH`, or other mutating requests when one or more fields are:

- Missing or empty when required
- Of the wrong type or format
- Violating uniqueness or other domain constraints

## Remedy

Read the `errors` extension in the response. It is a map of attribute names to arrays of validation messages.

Fix the invalid fields and resubmit the request.

## Example Problem Document

```http
HTTP/1.1 422 Unprocessable Content
Content-Type: application/problem+json

{
  "type": "https://docs.telebugs.com/rest-api/problems/validation-error.html",
  "title": "Validation Failed",
  "status": 422,
  "detail": "The request could not be processed due to validation errors.",
  "errors": {
    "name": ["can't be blank"],
    "url": ["is invalid"],
    "platform": ["is not included in the list"]
  }
}
```

The `errors` object mirrors the structure returned by Active Model / Rails validations.
