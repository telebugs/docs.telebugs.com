# Errors

The Telebugs API uses conventional HTTP status codes to indicate success or
failure.

## Error Response Format

Errors are always returned under the `errors` key as an array (for simple
errors) or an object (for validation errors).

### Simple Errors

```json
{
  "errors": ["Resource not found"]
}
```

### Validation Errors

```json
{
  "errors": {
    "name": ["can't be blank"],
    "url": ["is invalid"]
  }
}
```

### Common Status Codes

| Status | Meaning              | Typical `errors` message             |
| ------ | -------------------- | ------------------------------------ |
| 401    | Unauthorized         | `Missing API key`, `Invalid API key` |
| 404    | Not Found            | `Resource not found`                 |
| 422    | Unprocessable Entity | Validation errors object             |

# Example: Unauthorized

```json
curl https://your-telebugs-instance.com/api/telebugs/v1/projects \
  -H "Accept: application/json"

# Response (401)
{
  "errors": ["Missing API key"]
}
```

## Best Practice

Always check the HTTP status code. A non-2xx response means the request failed. The `errors` field will contain more details.
