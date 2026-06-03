# Getting Started with the REST API

Telebugs exposes a REST API that lets you manage projects, groups, reports,
apps, webhooks, and users programmatically.

The API is designed to be simple, pragmatic, and easy to use from scripts,
internal tools, or other services.

## Getting Your API Key

1. Go to **Account Settings**.
2. Open the **API** section.
3. Copy your API key.

You'll need this key to authenticate all requests.

## Base URL

All API requests are made to:

```sh
https://your-telebugs-instance.com/api/telebugs/v1
```

## Content Type

The API accepts and returns JSON:

```sh
Content-Type: application/json
Accept: application/json
```

## Your First Request

Here's a simple example that lists your projects:

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```
