# Webhooks

Send POST to services like Slack or Discord.

To configure:

1. Go to **Notification Configuration** > **Webhooks**.
2. Click **Create Configuration**.
3. Fill form and save.
4. Test with **Test**.
5. Edit by clicking the name.

## Add Webhook Form

- **URL**: Public endpoint.
- **Name**: Optional.
- **Template**: Slack, Discord, Custom.
- **Body**: JSON with placeholders.

## Placeholders

| Placeholder         | Description                                                                | Example                                                            |
| ------------------- | -------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| `{{project_name}}`  | The name of the project where the error occurred.                          | `Backend`, `example.com`                                           |
| `{{trigger}}`       | The event that caused the notification or error alert.                     | `"error"`, `"reoccurrence"`, `"error frequency exceeded"`          |
| `{{subject}}`       | A short description of the error or affected part of the code.             | `NoMethodError in ScoresController#create`, `Error in Thread.java` |
| `{{culprit}}`       | The specific method, function, or code location responsible for the error. | `ScoresController#create`                                          |
| `{{location}}`      | The file or line number where the error originated.                        | `app/controllers/scores_controller.rb:42`                          |
| `{{error_type}}`    | The class or type of the error.                                            | `NoMethodError`, `Error`, `Exception`                              |
| `{{error_message}}` | The detailed message associated with the error.                            | `undefined method '+' for nil`, `division by zero`                 |
| `{{project_url}}`   | A link to the project’s dashboard in Telebugs.                             | `https://telebugs.example.com/projects/7`                          |
| `{{view_url}}`      | A link to view the specific error instance in Telebugs.                    | `https://telebugs.example.com/errors/107`                          |

## Slack Setup

In Slack: **Channel** > **Integrations** > **Incoming Webhooks** > **Add to Slack** > **Copy URL**.

In Telebugs: Use **Slack** template, paste URL.

Example payload:

```json
{
  "username": "Telebugs",
  "text": "{{project_name}}: {{trigger}} - {{error_type}}: {{error_message}}",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*{{trigger}}* from <{{project_url}}|{{project_name}}>\n\n*{{error_type}}{{culprit}}*\n{{error_message}}\n\n*Location*\n{{location}}"
      }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "View"
          },
          "url": "{{view_url}}"
        }
      ]
    }
  ]
}
```

## Discord Setup

In Discord: **Server Settings** > **Integrations** > **Create Webhook** > **Copy UR**L.

In Telebugs: Use **Discord** template, paste URL.

Example payload:

```json
{
  "content": "**{{trigger}}** from [{{project_name}}]({{project_url}})\n[View error]({{view_url}})",
  "embeds": [
    {
      "color": 16711680,
      "fields": [
        {
          "name": "{{error_type}}{{culprit}}",
          "value": "{{error_message}}"
        },
        {
          "name": "Location",
          "value": "{{location}}"
        }
      ]
    }
  ]
}
```

## Microsoft Teams Setup

Microsoft Teams supports rich notifications via **Incoming Webhooks** using
Adaptive Cards.

### Create Webhook in Teams

1. In Microsoft Teams, go to the channel where you want notifications.
2. Click **More options** (•••) next to the channel name.
3. Select **Manage channel** > **Edit**.
4. Search for **Incoming Webhook** and select **Add** (or **Configure** if already added).
5. Enter a name (e.g., "Telebugs") and optionally upload an image.
6. Click **Create**.
7. Copy the generated webhook URL and click **Done**.

In Telebugs: Use **Teams** template, paste URL.

Example payload:

```json
{
  "type": "message",
  "attachments": [
    {
      "contentType": "application/vnd.microsoft.card.adaptive",
      "content": {
        "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
        "type": "AdaptiveCard",
        "version": "1.4",
        "body": [
          {
            "type": "TextBlock",
            "text": "**{{trigger}}** from [{{project_name}}]({{project_url}})",
            "wrap": true,
            "size": "Medium",
            "weight": "Bolder"
          },
          {
            "type": "TextBlock",
            "text": "**{{error_type}}{{culprit}}**",
            "wrap": true,
            "spacing": "Small"
          },
          {
            "type": "TextBlock",
            "text": "{{error_message}}",
            "wrap": true,
            "spacing": "None"
          },
          {
            "type": "TextBlock",
            "text": "**Location**",
            "wrap": true,
            "spacing": "Medium"
          },
          {
            "type": "TextBlock",
            "text": "{{location}}",
            "wrap": true,
            "spacing": "None"
          }
        ],
        "actions": [
          {
            "type": "Action.OpenUrl",
            "title": "View Error",
            "url": "{{view_url}}"
          }
        ]
      }
    }
  ]
}
```

This payload creates a formatted card with bold trigger/project, error details,
location, and a **View Error** button.

## Custom Webhooks

Use Custom template. Build your JSON with placeholders.

Example:

```json
{
  "project_name": "{{project_name}}",
  "trigger": "{{trigger}}",
  "subject": "{{subject}}",
  "culprit": "{{culprit}}",
  "location": "{{location}}",
  "error_type": "{{error_type}}",
  "error_message": "{{error_message}}",
  "view_url": "{{view_url}}"
}
```
