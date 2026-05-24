# Webhook Deliveries

You can inspect webhook delivery attempts through the API.

## List Deliveries for a Webhook

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/webhooks/WEBHOOK_ID/deliveries \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```

## Filtering

| Parameter | Description              | Example                 |
| --------- | ------------------------ | ----------------------- |
| `event`   | Filter by event type     | `?event=group.resolved` |
| `success` | Filter by success status | `?success=true`         |

Example:

```sh
curl "https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/webhooks/WEBHOOK_ID/deliveries?event=group.resolved&success=false" \
  -H "Authorization: Bearer YOUR_API_KEY"
```

Deliveries support cursor-based pagination.

## Get a Single Delivery

```sh
curl https://your-telebugs-instance.com/api/telebugs/v1/projects/PROJECT_ID/webhooks/WEBHOOK_ID/deliveries/DELIVERY_ID \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Accept: application/json"
```
