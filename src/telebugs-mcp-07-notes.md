# Notes

Notes let you and your team add context to error groups. They are useful for tracking investigation status, recording decisions, and maintaining team knowledge about specific issues.

MCP supports listing, adding, and deleting notes on error groups.

## List Notes

**Tool:** `list_notes_tool`

Retrieve notes attached to a specific error group.

### Parameters

| Parameter  | Type    | Required | Default      |
| ---------- | ------- | -------- | ------------ |
| `group_id` | integer | Yes      | —            |
| `limit`    | integer | No       | 50 (max 100) |

### Example Response

```json
[
  {
    "id": 7,
    "content": "Investigating — looks like a race condition in checkout.",
    "created_at": "2026-05-20T15:30:00Z",
    "automated": false,
    "user": {
      "id": 1,
      "name": "Kyrylo",
      "email_address": "kyrylo@example.com"
    }
  },
  {
    "id": 12,
    "content": "Auto-resolved: No reports in the last 30 days.",
    "created_at": "2026-06-10T08:15:00Z",
    "automated": true,
    "user": null
  }
]
```

Notes created by users have `automated: false` and include user information. System-generated notes have `automated: true`.

## Add Note

**Tool:** `add_note_tool`
**Scope required:** `telebugs.write`

Add a note to an error group.

### Parameters

| Parameter  | Type    | Required |
| ---------- | ------- | -------- |
| `group_id` | integer | Yes      |
| `note`     | string  | Yes      |

### Example Response

```json
{
  "id": 8
}
```

## Delete Note

**Tool:** `delete_note_tool`
**Scope required:** `telebugs.write`

Remove a note from an error group.

### Parameters

| Parameter | Type    | Required |
| --------- | ------- | -------- |
| `note_id` | integer | Yes      |

Returns an empty response on success.

## Common Use Cases

- Record investigation progress ("Investigating — suspected memory leak")
- Document root cause and fix ("Fixed by PR #847 in v1.4.2")
- Add context for teammates ("This only happens on weekends")
- Let AI tools leave notes when they take automated actions

## Error Responses

See [Errors](telebugs-mcp-08-errors.md) for general handling.

Common errors for this resource:

| Message                            | Cause                                          |
| ---------------------------------- | ---------------------------------------------- |
| `Group not found or access denied` | Invalid `group_id` or insufficient permissions |
| `Note cannot be blank`             | Empty `note` content provided                  |
| `Note not found`                   | Invalid `note_id` on delete                    |
