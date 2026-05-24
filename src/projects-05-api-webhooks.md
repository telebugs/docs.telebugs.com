# API Webhooks

API Webhooks allow you to receive structured HTTP callbacks when events happen
in a project, such as when a group is resolved or muted.

This is separate from the notification webhooks used for Slack, Discord, and Teams.

## Managing API Webhooks

API Webhooks are configured per project.

To manage them:

1. Go to the project.
2. Open **Project Settings**.
3. Go to the **API Webhooks** section.

From here you can create, edit, enable, disable, and delete webhooks. You can
also send test events and view delivery history.

## Events

You can subscribe to events such as:

- `group.created`
- `group.resolved`
- `group.unresolved`
- `group.muted`
- `group.unmuted`

## Delivery History

Each webhook shows its recent deliveries, including success status, HTTP
response codes, and error messages. This helps with debugging integrations.

## Managing via the REST API

API Webhooks can also be managed programmatically. See the
[Webhooks](/rest-api-08-webhooks.md) and [Webhook
Deliveries](/rest-api-09-webhook-deliveries.md) sections in the REST API
documentation.
