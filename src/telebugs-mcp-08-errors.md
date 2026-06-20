# MCP Errors

MCP uses [JSON-RPC 2.0](https://www.jsonrpc.org/specification) for communication. This means error handling works differently from the REST API.

There are two distinct kinds of errors:

| Type                 | When it happens                                            | How it's represented                                           | HTTP status         |
| -------------------- | ---------------------------------------------------------- | -------------------------------------------------------------- | ------------------- |
| **Transport errors** | Authentication, protocol, or rate limiting issues          | Top-level `error` object in JSON-RPC response                  | Usually `4xx`/`5xx` |
| **Tool errors**      | Tool execution failed (not found, validation, permissions) | `isError: true` inside a successful `200 OK` JSON-RPC response | `200 OK`            |

## Transport Errors (JSON-RPC level)

These occur before a tool is even invoked — usually due to authentication or protocol problems.

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32001,
    "message": "Authorization required"
  },
  "id": null
}
```

### Common Transport Error Codes

| Code     | Meaning                           |
| -------- | --------------------------------- |
| `-32001` | Missing or invalid authentication |
| `-32000` | Rate limit exceeded               |

## Tool Errors (`isError: true`)

When a tool fails (e.g. invalid ID, insufficient permissions, missing required parameter), the JSON-RPC request itself **succeeds** (HTTP 200), but the result contains `isError: true`.

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Group not found or access denied"
      }
    ],
    "isError": true
  }
}
```

**Important:** Always check `result.isError` to detect tool failures. Do **not** look for a `success` field or rely on HTTP status codes alone.

## How Tool Results Work

Tool outputs are returned as plain text inside the `content` array. The structure depends on the operation:

| Operation                            | Shape of `content[0].text` |
| ------------------------------------ | -------------------------- |
| List resources                       | JSON array of objects      |
| Get single resource                  | JSON object                |
| Write action (resolve, assign, etc.) | `{}` (empty object)        |
| Create note                          | `{ "id": 8 }`              |

Pagination metadata (`next_cursor`) is returned in `result._meta`, **not** inside the text payload.

### Examples of Successful Results

**List projects:**

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "[{\"id\":1,\"name\":\"Production\",\"platform\":\"Ruby\"}]"
      }
    ]
  }
}
```

**Get a single error group:**

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"id\":42,\"project_id\":1,\"error_type\":\"NoMethodError\",\"resolved\":false}"
      }
    ]
  }
}
```

**Paginated list (cursor in `_meta`):**

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "[{\"id\":42,\"error_type\":\"NoMethodError\"}]"
      }
    ],
    "_meta": {
      "next_cursor": 41
    }
  }
}
```

**Write action (e.g. resolve):**

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{}"
      }
    ]
  }
}
```

## Request Parameters

Tool arguments are passed as a flat object. For example:

```json
{
  "group_id": 42,
  "user_id": 7,
  "note": "Fixed in v1.4.2"
}
```

Do not wrap arguments in extra layers.

## Best Practices for Error Handling

- Check `result.isError === true` to detect tool failures.
- Read the error message from `result.content[0].text`.
- For transport errors, inspect the top-level `error` object.
- When building prompts for AI tools, instruct them to check `isError` before trusting the result.
