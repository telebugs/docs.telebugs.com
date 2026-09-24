# Project Settings

Access via three dots on card > **Settings**, or inside project > project name
dropdown > **Project Settings**.

## General Settings

Project settings use a sidebar on desktop and a section picker on smaller
screens. The project name stays visible so you can tell which project you’re
configuring. These settings apply to everyone with access to the project.

- **Project name**: Select the edit icon, enter a name, then choose **Save**.
  **Cancel** discards your draft. Renaming does not change the project token.
- **Reporting timezone**: Choose the timezone used for reporting days and charts.
  The selection saves automatically. Changing it rebuilds statistics in the
  background; large projects can take a while to finish.
- **Platform**: Choose the project icon and SDK setup instructions. This saves
  automatically and does not change existing reports.

### Source Code Linking

Select the edit icon beside **Repository** to set a GitHub, GitLab, or Bitbucket
repository URL and its default deployment branch. Choose **Save** to apply both
fields, or **Cancel** to discard changes. Leave the URL blank to turn off source
code linking.

Backtrace links open the corresponding source file. Private repositories work
when the viewer is signed in to the code host and has access; Telebugs does not
need repository credentials.

### Hosted Source Maps

Instance admins can open **Hosted source maps** in the project settings menu to
authorize exact public HTTPS asset origins. Telebugs makes no hosted-map
requests until an origin is listed.

Choose **Authorize origin…**, enter an origin, and choose **Authorize**. You can
authorize up to ten origins. Use an origin such as `https://assets.example.com`, without a path, query,
fragment, wildcard, IP address, or credentials. If a bundle points to a map on
a different CDN origin, authorize that exact origin separately.

Use the trash icon to remove an origin after confirming. Removing it prevents future use and purges its hosted-map cache. Existing
reports retain frames that were already remapped. See [Source Maps][3] for
setup, supported discovery methods, security behavior, limits, statuses, and
troubleshooting.

### Project Muting

Admins can mute every existing error in a project and automatically mute new
error groups for 1 hour, 4 hours, 8 hours, 1 day, 3 days, or forever. Reports
continue to be recorded, and muted groups remain in their normal **unresolved**
or **resolved** list with a mute-status badge. They do not send email, push, or
notification-webhook alerts.

To start muting from a project page, open the project-name menu, select **Mute
project**, and choose a duration.

You can open the same duration menu from the Command Palette: press
<kbd>Cmd</kbd>/<kbd>Ctrl</kbd>+<kbd>K</kbd> and choose **Mute project**.
This also works before the first error arrives. While muting is active, a
colored bell-slash icon appears beside the project name. Select it to open the
**Project muting** settings. The project menu shows **Manage muting**, and the
palette command changes to **Manage project muting** and opens the same
settings.

Use project muting before URL scans, load tests, or other planned noisy work.
In **General > Project muting**, choose **Mute project…**, select a duration,
and choose **Mute**. The active duration and **Stop muting new errors** control
appear in the same group.

Selecting **Stop muting new errors** stops future groups from inheriting the
project mute. Errors already muted by the setting stay muted until their
deadline or until you explicitly unmute them. This prevents scan-created errors
from flooding the active queue as soon as the project resumes.

## Token Settings

Tokens allow your app to send reports securely.

- **Project token**: Copy with the clipboard icon. Administrators can use the
  regenerate icon and confirm to replace it.
- **DSN**: Copy this full URL when configuring a Sentry SDK.

Regenerating immediately invalidates both the old token and its DSN. Update your
app configuration to keep sending reports. Anyone with either value can submit
reports to this project, but cannot read reports or access your account.

Store in env vars, not code. Test after regenerate with a sample error.

## Access Control

Control who sees the project.

Administrators can use the switch beside each person to grant or remove access.

Admins: full control; members: view/resolve only.

Changes save automatically. See [Team Management][1] for roles/invites.

Use for segmented teams, e.g., backend devs on backend projects.

## Notifications Settings

Enable alerts via preferred channels without overload.

- **Channels**: Toggle Email, Push, or Webhook for this project. Select a channel
  name to configure it. Webhook subscriptions retain their choices when the
  Webhook channel is off; their controls become available again when it is on.
- **Severity**: Enable **Only notify for fatal and error events** to keep
  lower-severity reports without sending alerts for them. The setting is off by
  default and applies to every notification channel in the project. Frequency
  thresholds count only fatal, error, and missing-level reports when enabled.
- **Rules**: Set notifications for new errors, reoccurrences, frequency thresholds,
  or every unresolved occurrence. Use the edit icon beside an enabled frequency
  rule to set the number of reports and interval in minutes, then choose **Save**.
- **Recipients**: Toggle personal notifications per user. Each person’s account
  notification settings still apply; project preferences remain stored when a
  person turns off notifications in their account.

Combine channels for redundancy. Test with simulated errors to avoid fatigue.

## Danger Zone

Irreversible actions; back up first.

- **Storage and reports**: Estimated disk usage, note attachments, report count,
  and the time of the last report. Use the refresh icon to recalculate disk usage.
- **Purge error details**: Remove report details, including backtraces and
  breadcrumbs, while retaining core report data for statistics.
- **Purge note attachments**: Clear files from notes (text remains).
- **Purge all errors**: Wipe all error data (project structure stays).
- **Delete project**: Remove the project, its reports, and its settings.

Every destructive action has a confirmation that explains what will be removed.

Use for cleanup, but export data if needed for audits (see [Instance Settings][2]).

[1]: /team-management-00.md
[2]: /instance-00.md
[3]: /release-01-source-maps.md#hosted-source-map-discovery
