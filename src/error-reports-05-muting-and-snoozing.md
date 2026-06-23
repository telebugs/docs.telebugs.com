# Muting and Snoozing

**Muting** silences notifications for a specific error group. Temporary
muting is also called **snoozing**. This is useful when:

- An error is known and low-priority.
- You're waiting on a third-party fix.
- The error is noisy but not urgent.
- You want notifications to resume only if the error keeps happening.

When an error group is muted, **no notifications** (email, push, or webhook)
will be sent for new reports in that group, regardless of your notification
rules.

### Types of Muting

Telebugs supports three mute types:

- **Time-based snooze** - Silence notifications for a fixed duration. The web
  UI offers these durations:

  - 1 hour
  - 4 hours
  - 8 hours
  - 1 day
  - 3 days

  After the time expires, notifications automatically resume.

- **Occurrence-based mute** - Silence notifications until the group receives a
  selected number of additional reports. The web UI offers:

  - Until it happens again
  - 10 more occurrences
  - 100 more occurrences
  - 1,000 more occurrences
  - 10,000 more occurrences
  - 100,000 more occurrences

  Occurrence-based muting counts from the group's current `reports_count`. For
  example, if a group currently has 17 reports and you mute it for 10 more
  occurrences, notifications resume when the group reaches 27 reports.

- **Permanent mute** ("Forever") - Silence notifications indefinitely until the
  group is manually unmuted.

### How Muting Works

- Muting applies to the **entire error group**.
- Muting only affects **notifications**. New reports are still recorded,
  grouped, and visible in dashboards.
- Muting does not resolve the error. Resolution and muting are separate triage
  states.
- Any team member with access to the project can mute or unmute.
- Choosing a new mute option replaces the previous mute condition for that
  group.
- When an error is muted or unmuted, Telebugs automatically adds a system note:
  - "Error muted by [User Name]."
  - "Error unmuted by [User Name]."
- A badge appears on the error icon in all views (**All Errors**, **All
  Reports**, project dashboards, group detail) showing:
  - Bell-snooze icon for time-based snoozes
  - Bell-slash icon for permanent and occurrence-based mutes
- Hovering the badge reveals who muted it and when notifications resume:
  - Time-based snoozes show the remaining time.
  - Occurrence-based mutes show how many more occurrences remain.
  - Permanent mutes show that they remain muted until manually unmuted.

When a time-based or occurrence-based mute expires, Telebugs clears the mute and
notifications resume automatically. For occurrence-based mutes, the report that
reaches the threshold can trigger notifications.

### How to Mute or Unmute an Error

Controls are available on the **individual error group detail page**.

#### On desktop / wider screens

The **Mute…** button appears in the header actions (next to Own it / Resolve).
The menu includes a few common choices from each category, such as **For 1
hour**, **For 1 day**, **Until it happens again**, **Until 10 more
occurrences**, and **Forever**.

Choose **More mute options…** to see the full list of time and occurrence
options.

#### On mobile / narrow screens

A prominent **Mute…** button is shown below the error header. Tapping it opens
a bottom sheet menu with the same common choices and **More mute options…**
for the full list.

#### Unmuting / Unsnoozing

If the error is currently muted:

- The button changes to **Unmute** for permanent and occurrence-based mutes, or
  **Unsnooze** for time-based snoozes.
- Clicking/tapping it immediately removes the mute and resumes notifications.

### API and MCP Support

Muting is also available through automation interfaces:

- The [REST API Groups endpoint](/rest-api-05-groups.md) can mute a single group
  forever or until a number of additional occurrences. REST bulk mute creates
  permanent mutes.
- [Telebugs MCP Error Groups](/telebugs-mcp-05-error-groups.md) can mute a
  single group forever, until an ISO8601 `snooze_until` timestamp, or until a
  number of additional `occurrences`. MCP bulk mute supports permanent and
  time-based snoozes.

### Important Notes

- Resolved errors can still be muted (useful for preventing notifications if
  they regress; see [Owning Errors][1] for related triage).
- If a muted error receives new reports after being resolved, it will
  automatically become unresolved (as with any error), but notifications remain
  suppressed while the mute condition is still active.
- You can find muted and unmuted groups with the `is:muted` and `is:unmuted`
  search filters.

Use muting responsibly to reduce noise while keeping full visibility into your
error stream.

[1]: /error-reports-04-owning-errors.md
