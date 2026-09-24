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

Choose **Add webhook** to enter an endpoint URL, an optional signing secret,
and the events to send. Choose **Add** to create it or **Cancel** to discard the
form. The **Enabled** switch controls whether the webhook receives events.

Use a webhook’s edit icon to change its details, then choose **Save**. Existing
event selections are preserved. Clearing all events leaves the endpoint
configured without sending any events. Use the trash icon to delete a webhook;
the confirmation also warns that its delivery history will be deleted.

## Events

You can subscribe to events such as:

- `group.created`
- `group.resolved`
- `group.unresolved`
- `group.muted`
- `group.unmuted`

## Delivery History

Select a webhook’s URL to view its recent delivery attempts, including success
status, UTC timestamps, HTTP response codes, and any recorded error messages.
Use the pagination controls to move through older attempts. This helps with debugging integrations.

## Managing via the REST API

API Webhooks can also be managed programmatically. See the
[Webhooks](/rest-api-08-webhooks.md) and [Webhook
Deliveries](/rest-api-09-webhook-deliveries.md) sections in the REST API
documentation.
