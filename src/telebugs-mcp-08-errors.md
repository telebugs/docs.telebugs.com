# MCP Errors

Most people use Telebugs MCP through an AI client, so they rarely need to handle raw protocol responses. If you are troubleshooting a connection or building a custom client, there are two kinds of errors to know about.

| Type                 | When it happens                                            | How it appears                                               | HTTP status         |
| -------------------- | ---------------------------------------------------------- | ------------------------------------------------------------ | ------------------- |
| **Transport errors** | Authentication, protocol, or rate limiting issues          | Top-level JSON-RPC `error` object                            | Usually `4xx`/`5xx` |
| **Tool errors**      | Tool execution failed, such as not found or no permission  | `isError: true` inside an otherwise successful MCP response  | `200 OK`            |

## Transport Errors

Transport errors happen before a tool is invoked, usually because authentication failed or the request is not valid MCP.

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

## Tool Errors

Tool errors happen after authentication succeeds. The MCP request itself succeeds, but the tool result is marked with `isError: true`.

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

Always check `result.isError` before trusting a tool result. Do not rely on HTTP status alone.

## Reading Successful Results

The resource pages in this guide show the JSON payloads returned by each tool. Depending on the MCP client, those payloads may be exposed as text, structured data, or both.

Common patterns:

| Operation                            | What to expect                                      |
| ------------------------------------ | --------------------------------------------------- |
| List projects                        | A `projects` array                                  |
| List error groups                    | A `groups` array plus `has_more` and `next_cursor`  |
| List reports                         | A `reports` array plus `has_more` and `next_cursor` |
| Get one group or report              | One JSON object                                     |
| Resolve, mute, assign, or add notes  | A small confirmation object or success message      |

For paginated tools, use `has_more` as the stop signal. When `has_more` is `false`, `next_cursor` is `null`.

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

## Best Practices

- Check `result.isError === true` to detect tool failures.
- Read the error message from `result.content[0].text`.
- For transport errors, inspect the top-level `error` object.
- When paginating, stop when `has_more` is `false`.
