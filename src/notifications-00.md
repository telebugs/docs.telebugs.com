# Notifications

Telebugs supports email, push notifications, and webhooks for real-time alerts
on errors.

Configure global settings in your profile > **Notification Configuration**.

Conditions for alerts (apply to all channels):

- Severity is allowed by the project's notification settings.
- New error occurs.
- Error reoccurs after resolution.
- Frequency exceeds threshold (e.g., >10 in 5 minutes).

By default, projects send notifications for every event level. Admins can enable
**Only notify for fatal and error events** in a project's notification settings.
Warning, info, debug, and sample-level events are still stored and searchable,
but they do not send email, push, or notification-webhook alerts. Reports
without a level are treated as errors. Lower-severity events also do not count
toward frequency thresholds while this setting is enabled.

Projects can disable channels individually (see [Project Settings][1]). Users
can opt out per project in their profile.

See sub-sections for setup.

[1]: /projects-04-project-settings.md
