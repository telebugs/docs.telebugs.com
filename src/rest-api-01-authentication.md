# Authentication

All requests to the Telebugs REST API must be authenticated using an API key.

## Getting Your API Key

1. Go to **Account Settings** in Telebugs.
2. Find the **API access** section.
3. Copy your personal API key.

> **Note:** Your API key gives full access to everything you have access to. Keep it secure.

## Authenticating Requests

Include your API key in the `Authorization` header using the `Bearer` scheme:

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

## Example

```
curl https://your-telebugs-instance.com/api/telebugs/v1/groups \
  -H "Authorization: Bearer tlbgs_xxxxxxxxxxxxxxxx" \
  -H "Accept: application/json"
```

## Notes

- API keys are tied to your user account.
- There is currently no support for project-scoped or read-only tokens.
- Treat your API key like a password.
