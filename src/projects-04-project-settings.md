# Project Settings

Access via three dots on card > **Settings**, or inside project > project name
dropdown > **Project Settings**.

## General Settings

- **Name**: Update for clarity, e.g., "AwesomeApp Backend". Click **Rename**.
- **Timezone**: Set to match team or servers (affects dates in reports).
  Search/select, **Change timezone**. Use UTC for global teams.
- **Platform**: Choose for icon and tailored SDK guides. Save changes.

These make the dashboard more intuitive without affecting data.

## Token Settings

Tokens allow your app to send reports securely.

- **Project token**: View/copy/regenerate if compromised (invalidates old one).
- **DSN**: Full URL with token. Copy for SDK config.

Store in env vars, not code. Test after regenerate with a sample error.

## Access Control

Control who sees the project.

View team list and toggle checkboxes for access.

Admins: full control; members: view/resolve only.

Changes save automatically. See Team Management for roles/invites.

Use for segmented teams, e.g., backend devs on backend projects.

## Notifications Settings

Enable alerts via preferred channels without overload.

- **Channels**: Toggle Email, Push, Webhooks. Configure/test each.
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

Use for cleanup, but export data if needed for audits.
