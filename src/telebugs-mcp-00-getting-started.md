# Getting Started with Telebugs MCP

Telebugs exposes a [Model Context Protocol](https://modelcontextprotocol.io/) (MCP)
server that lets AI coding tools **read your error data and take action** on your
behalf — directly inside your editor.

Instead of copying stack traces into ChatGPT or Claude, your AI can now:

- Inspect full error reports with backtraces and context
- Search and filter error groups using the same powerful query syntax as the REST API
- Resolve, mute, assign, and annotate issues
- Add notes and manage your error workflow

The MCP integration mirrors the [REST API](rest-api-00-getting-started.md): the
same projects, groups, reports, and notes are available, scoped to your account
and project memberships.

## Quickstart

Get value in under two minutes:

1. **Connect your editor**
   Follow the step-by-step instructions in [Connecting AI Tools](telebugs-mcp-02-connecting.md)
   for Cursor, Windsurf, or Claude.

2. **Try a prompt**
   Once connected, ask your AI something like:

   > "List my Telebugs projects and show the open error groups in Production with the most reports this week."

   Or:

   > "Find the top 5 unresolved error groups in production and summarize what's happening."

3. **Take action**
   You can then say:

   > "Resolve group 42 with the note: 'Fixed by PR #847 — deployed in v1.4.2'"

   Or ask it to assign an issue to a teammate, add context, or investigate a specific report.

## What You Can Do

Connected AI tools can:

- List your projects and error groups
- Search and filter errors with the same query syntax as the REST API
- Fetch full error reports with backtraces, breadcrumbs, and request context
- List project members to find the right assignee
- Resolve, mute, assign, and annotate error groups
- Create, list, and delete notes on error groups

## MCP Endpoint

Your Telebugs instance serves MCP at:

```sh
https://your-telebugs-instance.com/mcp
```

## Discovery

MCP clients can discover the server automatically:

```sh
curl https://your-telebugs-instance.com/.well-known/mcp.json
```

Example response:

```json
{
  "mcp_endpoint": "https://your-telebugs-instance.com/mcp",
  "authorization_servers": ["https://your-telebugs-instance.com"],
  "protocol_version": "2025-06-18",
  "transport": "streamable-http"
}
```

## Authentication

MCP supports two authentication methods:

1. **OAuth 2.0** (recommended for AI tools like Cursor and Claude) — see
   [Authentication](telebugs-mcp-01-authentication.md)
2. **API key** — use your existing REST API key as a Bearer token (useful for scripts)

For step-by-step setup in your editor, see
[Connecting AI Tools](telebugs-mcp-02-connecting.md).

## Managing Connected Apps

After authorizing an MCP client, you can review and revoke access from
**Account Settings → Connected MCP apps**.

## Available Tools

Telebugs MCP exposes 14 tools grouped by resource:

| Resource                                        | Capabilities                                                |
| ----------------------------------------------- | ----------------------------------------------------------- |
| [Projects](telebugs-mcp-04-projects.md)         | List projects and members                                   |
| [Error Groups](telebugs-mcp-05-error-groups.md) | Search, inspect, resolve, mute, assign, and annotate groups |
| [Reports](telebugs-mcp-06-reports.md)           | Fetch full error reports                                    |
| [Notes](telebugs-mcp-07-notes.md)               | List, add, and delete notes                                 |

## Security Notes

- Access is limited to projects you belong to.
- OAuth uses `telebugs.read` and `telebugs.write` scopes.
- Report data is wrapped with security warnings (`_security_note`) to help protect
  against prompt injection from untrusted application data. See
  [Reports](telebugs-mcp-06-reports.md) for details.

## Next Steps

- Read the [Authentication](telebugs-mcp-01-authentication.md) guide to understand OAuth vs API keys
- Follow [Connecting AI Tools](telebugs-mcp-02-connecting.md) for your specific editor
- Explore the available tools in the [Error Groups](telebugs-mcp-05-error-groups.md) reference
