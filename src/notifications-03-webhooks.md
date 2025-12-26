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
  "attachments": [
    {
      "fallback": "{{project_name}}: {{trigger}} - {{error_type}}: {{error_message}}",
      "pretext": "*{{trigger}}* from <{{project_url}}|{{project_name}}>",
      "color": "#D00000",
      "fields": [
        {
          "title": "{{error_type}}{{culprit}}",
          "value": "{{error_message}}",
          "short": false
        },
        {
          "title": "Location",
          "value": "{{location}}",
          "short": false
        }
      ],
      "actions": [
        {
          "type": "button",
          "text": "View",
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
