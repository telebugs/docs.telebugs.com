# Connecting AI Tools

This guide covers connecting MCP-compatible AI tools — including Codex,
Cursor, Windsurf, and Claude — to your Telebugs instance.

## Codex

1. Open **Settings → MCP servers** in the ChatGPT desktop app.
2. Select **Add server**.
3. Enter a name, choose **Streamable HTTP**, and use your Telebugs URL:

```sh
https://your-telebugs-instance.com/mcp
```

4. Save the server and restart the app.
5. Select **Authenticate**, sign in to Telebugs, and approve the requested scopes.

Type `/mcp` in the composer to verify that Telebugs is connected. The desktop
app, Codex CLI, and Codex IDE extension share MCP configuration on the same
Codex host.

To configure Codex directly, add the server to `~/.codex/config.toml`:

```toml
[mcp_servers.telebugs]
url = "https://your-telebugs-instance.com/mcp"
```

Then run `codex mcp login telebugs` to authorize the connection. Use
`codex mcp list` or `/mcp` to verify it.

See the [Codex MCP documentation](https://learn.chatgpt.com/docs/extend/mcp)
for additional configuration options.

## Cursor

1. Open **Cursor Settings → MCP**.
2. Add a new MCP server with your Telebugs URL:

```json
{
  "mcpServers": {
    "telebugs": {
      "url": "https://your-telebugs-instance.com/mcp"
    }
  }
}
```

3. Cursor discovers OAuth metadata automatically and prompts you to sign in.
4. Approve the requested scopes on the Telebugs consent screen.
5. Once connected, Telebugs tools appear in Cursor's tool list.

To revoke access later, go to **Account Settings → Connected apps** in
Telebugs.

## Windsurf

Windsurf follows the same OAuth discovery flow. Add your Telebugs MCP endpoint
in Windsurf's MCP server configuration:

```json
{
  "mcpServers": {
    "telebugs": {
      "url": "https://your-telebugs-instance.com/mcp"
    }
  }
}
```

Sign in when prompted and approve the connection.

## Claude

Claude connects to Telebugs as a **remote MCP custom connector**. This works in
Claude on the web, Claude Desktop, and Cowork.

> **Note:** Unlike Cursor and Windsurf, Claude does not call your Telebugs
> instance from your computer. Connections originate from Anthropic's
> infrastructure, so your Telebugs instance must be reachable over the public
> internet. Private networks, VPN-only hosts, and `localhost` will not work.

### Pro and Max plans

1. Open **[Customize → Connectors](https://claude.ai/customize/connectors)** in
   Claude.
2. Click **+**, then **Add custom connector**.
3. Enter your Telebugs MCP URL:

```sh
https://your-telebugs-instance.com/mcp
```

4. Click **Add**, then **Connect** when prompted.
5. Sign in to Telebugs and approve the requested scopes on the consent screen.

### Team and Enterprise plans

An Owner must add the connector first under
**[Organization settings → Connectors](https://claude.ai/admin-settings/connectors)**.
Choose **Custom → Web** and enter the same MCP URL. Team members then connect
individually from **Customize → Connectors**.

### Using Telebugs in a conversation

Enable the Telebugs connector for a chat via the **+** button → **Connectors**.
Claude discovers OAuth metadata automatically — no manual client registration is
required on your side.

To revoke access, disconnect the connector in Claude or remove the app under
**Account Settings → Connected apps** in Telebugs.

## Other MCP Clients

Any MCP client supporting Streamable HTTP transport and OAuth 2.0 discovery can
connect to Telebugs. The server advertises:

- **Transport:** `streamable-http`
- **Protocol version:** `2025-06-18`
- **Discovery:** `/.well-known/mcp.json`

Supported redirect URI schemes for OAuth include `https://`, `http://localhost`,
and custom schemes (`cursor://`, `windsurf://`, `vscode://`).

## API Key Setup (Manual / Scripting)

If your client supports Bearer token authentication but not OAuth, use your REST
API key:

1. Copy your API key from **Account Settings → API access**.
2. Configure the client to send `Authorization: Bearer tlbgs_...` on MCP
   requests.

See [Authentication](telebugs-mcp-01-authentication.md) for details.

## Verifying the Connection

After connecting, ask your AI tool to list your Telebugs projects. It should call
`list_projects_tool` and return your accessible projects with stats. To assign
errors, it can call `list_project_users_tool` to discover team member IDs.

For an end-to-end investigation check, open an error in Telebugs, select **Copy
for LLMs**, and paste the prompt into the connected coding agent. Its first
Telebugs call should be `get_investigation_context_tool`.

If authentication fails, check:

- The Telebugs URL is correct and reachable
- Your account is active
- The connected app has not been revoked under **Connected apps**
