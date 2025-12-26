# Muting and Snoozing

**Muting** (also called "snoozing" for temporary periods) allows you to silence
notifications for a specific error group. This is useful when:

- An error is known and low-priority.
- You're waiting on a third-party fix.
- The error is noisy but not urgent.

When an error group is muted, **no notifications** (email, push, or webhook)
will be sent for new reports in that group, regardless of your notification
rules.

### Types of Muting

There are two forms:

- **Temporary Snooze** – Silence notifications for a fixed duration. Available
  durations:

  - 1 hour
  - 4 hours
  - 8 hours
  - 1 day
  - 3 days
  - After the time expires, notifications automatically resume.

- **Permanent Mute** ("Forever") – Silence notifications indefinitely until
  manually unmuted.

### How Muting Works

- Muting applies to the **entire error group**.
- Any team member with access to the project can mute or unmute.
- When an error is muted or unmuted, Telebugs automatically adds a system note:
  - "Error muted by [User Name]."
  - "Error unmuted by [User Name]."
- A badge appears on the error icon in all views (**All Errors**, **All
  Reports**, project dashboards, group detail) showing:
  - Bell-snooze icon for temporary snooze
  - Bell-slash icon for permanent mute
- Hovering the badge reveals a popover with who muted it and (for snoozes) when
  it will resume.

### How to Mute or Unmute an Error

Controls are available on the **individual error group detail page**.

#### On desktop / wider screens

The **Mute…** button appears in the header actions (next to Own it / Resolve).
Clicking it opens a dropdown with duration options, including **Forever**.

#### On mobile / narrow screens

A prominent **Mute…** button is shown below the error header.
Tapping it opens a bottom sheet menu with the same duration options.

#### Unmuting / Unsnoozing

If the error is currently muted:

- The button changes to **Unmute** (permanent mute) or **Unsnooze** (temporary).
- Clicking/tapping it immediately removes the mute and resumes notifications.

### Important Notes

- Muting only affects **notifications** — new reports are still recorded,
  grouped, and visible in dashboards.
- Resolved errors can still be muted (useful for preventing notifications if
  they regress).
- If a muted error receives new reports after being resolved, it will
  automatically become unresolved (as with any error), but notifications will
  remain suppressed until unmuted.

Use muting responsibly to reduce noise while keeping full visibility into your
error stream.
