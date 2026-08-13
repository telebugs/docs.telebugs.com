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

## Automatic Regression Context

When a new report automatically reopens a resolved group, a
`group.unresolved` API webhook includes `reason: "new_report"` plus correlation
details captured before the resolution is cleared:

```json
{
  "event": "group.unresolved",
  "reason": "new_report",
  "group_id": 42,
  "project_id": 1,
  "report_id": 123,
  "event_id": "69b345eb156342a496e5880afee01452",
  "release_version": "server-2026-08-12",
  "report_occurred_at": "2026-08-12T09:00:00.000000Z",
  "report_received_at": "2026-08-12T10:00:00.000000Z",
  "previous_resolved_at": "2026-08-12T08:00:00.000000Z",
  "previous_resolver_id": 3,
  "previous_resolver_name": "Sunshine"
}
```

`event_id`, release, and resolver fields are `null` when unavailable.
