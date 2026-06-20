# Webhooks

You can manage webhooks programmatically through the API.

## List Webhooks for a Project

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/webhooks \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

## Create a Webhook

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/webhooks \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "url": "https://example.com/webhook",
    "events": ["group.resolved", "group.muted"],
    "enabled": true
  }'
```

Returns the created webhook with fields at the top level (`id`, `url`, `events`, `enabled`, `secret`).

## Update a Webhook

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/webhooks/WEBHOOK_ID \
  -X PATCH \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "enabled": false
  }'
```

Returns the updated webhook with fields at the top level.

## Delete a Webhook

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/webhooks/WEBHOOK_ID \
  -X DELETE \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Send a Test Webhook

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/webhooks/WEBHOOK_ID/test \
  -X POST \
  -H "Authorization: Bearer YOUR_API_KEY"
```
