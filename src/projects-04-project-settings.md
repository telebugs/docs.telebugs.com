# Project Settings

Access via three dots on card > **Settings**, or inside project > project name
dropdown > **Project Settings**.

## General Settings

- **Name**: Update for clarity, e.g., "AwesomeApp Backend". Click **Rename**.
- **Timezone**: Set to match team or servers (affects dates in reports).
  Search/select, **Change timezone**. Use UTC for global teams.
- **Platform**: Choose for icon and tailored SDK guides. Save changes.

These make the dashboard more intuitive without affecting data.

### Hosted Source Maps

Instance admins can open **Hosted source maps** in the project settings menu to
authorize exact public HTTPS asset origins. Telebugs makes no hosted-map
requests until an origin is listed.

Enter an origin such as `https://assets.example.com`, without a path, query,
fragment, wildcard, IP address, or credentials. If a bundle points to a map on
a different CDN origin, authorize that exact origin separately.

Removing an origin prevents future use and purges its hosted-map cache. Existing
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
The active duration and stop control appear in **Project muting** settings.

Selecting **Stop muting new errors** stops future groups from inheriting the
project mute. Errors already muted by the setting stay muted until their
deadline or until you explicitly unmute them. This prevents scan-created errors
from flooding the active queue as soon as the project resumes.

## Token Settings

Tokens allow your app to send reports securely.

- **Project token**: View/copy/regenerate if compromised (invalidates old one).
- **DSN**: Full URL with token. Copy for SDK config.

Store in env vars, not code. Test after regenerate with a sample error.

## Access Control

Control who sees the project.

View team list and toggle checkboxes for access.

Admins: full control; members: view/resolve only.

Changes save automatically. See [Team Management][1] for roles/invites.

Use for segmented teams, e.g., backend devs on backend projects.

## Notifications Settings

Enable alerts via preferred channels without overload.

- **Channels**: Toggle Email, Push, Webhooks. Configure/test each.
- **Severity**: Enable **Only notify for fatal and error events** to keep
  lower-severity reports without sending alerts for them. The setting is off by
  default and applies to every notification channel in the project. Frequency
  thresholds count only fatal, error, and missing-level reports when enabled.
- **Rules**: Set for new errors, reoccurrences, frequency thresholds.
- **Recipients**: Toggle per user for targeted alerts, e.g., on-call.

Combine channels for redundancy. Test with simulated errors to avoid fatigue.

## Danger Zone

Irreversible actions; back up first.

- **Stats**: Disk space, report count.
- **Partial purge**: Remove details from old reports, keep stats.
- **Purge attachments**: Clear files from notes (text remains).
- **Full purge**: Wipe all error data (project structure stays).
- **Delete project**: Remove entirely; double-confirm.

Use for cleanup, but export data if needed for audits (see [Instance Settings][2]).

[1]: /team-management-00.md
[2]: /instance-00.md
[3]: /release-01-source-maps.md#hosted-source-map-discovery
