# MCP Authentication

Telebugs supports two authentication methods for the MCP server:

- **OAuth 2.0 with PKCE** — Recommended for AI coding tools (Cursor, Claude, Windsurf, etc.)
- **API keys** — Recommended for scripts, automation, and manual testing

## Quick Comparison

| Aspect                 | OAuth 2.0 (Recommended)                | API Key                                   |
| ---------------------- | -------------------------------------- | ----------------------------------------- |
| **Best for**           | AI coding tools (Cursor, Claude, etc.) | Scripts, CI, custom integrations          |
| **Security model**     | Per-app tokens with scopes             | Full access (no scopes)                   |
| **Revocation**         | Per-app (via Connected MCP apps)       | Requires rotating the API key             |
| **User consent**       | Explicit approval screen               | None                                      |
| **Token rotation**     | Refresh tokens rotate automatically    | N/A                                       |
| **Recommended for AI** | Yes                                    | Only if your client doesn't support OAuth |

> **Recommendation:** Use **OAuth 2.0** for any AI coding tool. It gives you fine-grained control and lets you revoke access to a specific app without affecting anything else.

## OAuth 2.0 (Recommended)

MCP clients discover OAuth metadata automatically:

```sh
curl https://your-telebugs-instance.com/.well-known/oauth-authorization-server
```

Telebugs implements standard OAuth 2.0 with PKCE, including dynamic client registration, authorization, token, and revocation endpoints.

### Scopes

| Scope            | Access                                              |
| ---------------- | --------------------------------------------------- |
| `telebugs.read`  | List and fetch projects, groups, reports, and notes |
| `telebugs.write` | Resolve, mute, assign, and manage notes             |

If no scopes are requested during authorization, both `telebugs.read` and `telebugs.write` are granted by default.

### OAuth Flow

1. The MCP client initiates authorization using PKCE.
2. You sign in to Telebugs and approve the requested scopes.
3. Telebugs returns a short-lived authorization code.
4. The client exchanges the code for an access token + refresh token.
5. The client uses the access token for requests to `/mcp`.

**Important details:**

- Authorization codes expire after **60 seconds** and are single-use.
- Refresh tokens **rotate on every use** (improves security).
- Access tokens are valid for **12 hours**.

### Token Lifetimes

| Token              | Lifetime   | Notes                        |
| ------------------ | ---------- | ---------------------------- |
| Access token       | 12 hours   | Used for actual MCP requests |
| Refresh token      | 90 days    | Automatically rotates on use |
| Authorization code | 60 seconds | Single-use, very short-lived |

These lifetimes are fixed. To revoke access earlier, use one of the methods below.

### Revoking Access

You have two ways to revoke a connected MCP client:

1. **From the UI (recommended)**
   Go to **Account Settings → Connected MCP apps** and revoke the specific app.

2. **Programmatically**
   Call the revocation endpoint:

   ```sh
   curl https://your-telebugs-instance.com/oauth/revoke \
     -X POST \
     -d "token=YOUR_ACCESS_OR_REFRESH_TOKEN"
   ```

   The revocation endpoint always returns `200 OK`.

## API Key Authentication

You can authenticate MCP requests using your existing REST API key. This is useful for scripts or when your client doesn't support OAuth.

### Setup

1. Go to **Account Settings → API**.
2. Copy your API key (it starts with `tlbgs_`).
3. Send it as a Bearer token when calling `/mcp`:

   ```sh
   curl https://your-telebugs-instance.com/mcp \
     -X POST \
     -H "Authorization: Bearer tlbgs_YOUR_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc":"2.0","method":"tools/list","id":1}'
   ```

### Characteristics

- API keys grant **full read and write access** with no scope restrictions.
- Treat them like passwords — never commit them to version control.
- There is no per-app revocation. If you need to revoke access, you must rotate the API key.

> **Note:** For AI coding tools, prefer OAuth 2.0. It allows you to revoke access to a specific editor or agent without rotating your main API key and affecting other integrations.

## Which Method Should I Use?

| Your Use Case                        | Recommended Method | Reason                                |
| ------------------------------------ | ------------------ | ------------------------------------- |
| Using Cursor, Claude, Windsurf, etc. | **OAuth 2.0**      | Per-app revocation + explicit consent |
| Writing a custom script or bot       | API Key            | Simpler for non-interactive use       |
| CI/CD pipeline                       | API Key            | No browser interaction needed         |
| Want maximum security + auditability | **OAuth 2.0**      | Scoped + revocable per client         |
