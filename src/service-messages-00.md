# Service Messages

Service Messages guide admins through important maintenance tasks (like database
optimization or post-update cleanup) directly in the dashboard. No command-line
access is required.

Pending messages show as a red badge on your profile picture in the top-right
corner (visible only to admins). Once all messages are addressed, the badge
disappears for everyone.

## Accessing Service Messages

1. Click your profile picture in the top-right.
2. Look for the **Service Messages** entry in the dropdown (highlighted with the
   red badge if pending).

The index page lists all messages in a simple table with titles and statuses.
Click a title for details.

## Message Statuses

Each message has one of these statuses:

- **Needs action** (gray): Requires admin input.
- **In progress** (orange): Background job running.
- **Completed** (green): Finished successfully.
- **Failed** (red): Something went wrong.

## Viewing a Message

The detail page shows:

- **Title** and **Description** (what the task does and why it matters)
- **Status** with color tag
- **First read by** (admin and timestamp)
- **Started by** and **Started at**
- **Completed at** (if finished)
- **Error message** (if failed)

If the status is **Needs action** or **Failed**, a **Run Action** button appears
at the bottom.

Clicking **Run Action** automatically marks the message as read and clears your
badge (the badge is shared across all admins).

## Running an Action

Only admins can start actions, and only when the status allows it.

After clicking **Run Action**:

- Status changes to **In progress**.
- The task runs asynchronously in the background.
- A notice warns it may take time (e.g., up to an hour for large datasets).

Refresh the page to see updates. When finished, the status becomes **Completed**
or **Failed**, with timestamps and any error details.

**Quick tip:** Address service messages promptly after upgrades to keep your instance running smoothly.
