# All Reports

The **All Reports** view provides a global, cross-project list of every
individual error report received by your Telebugs instance. Unlike the **All
Errors** view (which shows grouped issues), this page displays raw, ungrouped
reports in chronological order.

This view is particularly useful for:

- Investigating very recent errors in real time.
- Auditing exact occurrences without grouping logic interference.
- Debugging timing-specific issues or spotting patterns in rapid bursts of
  reports.

> **Note:** Only reports from projects you are a member of are shown.

## Key Features

### Filtering

Filter controls at the top of the page (all times are in UTC):

- **Project**: Select a specific project or leave as "All" to see reports across
  all your projects.
- **From / To**: Date-time range picker to restrict reports to those that
  occurred within the specified window. Defaults to the full range of available
  data.
- **Reset link**: Quickly clear all filters.

### Sorting and Pagination

- Reports are sorted by **occurred at** time (most recent first).
- Cursor-based pagination with **Previous** / **Next** arrows.
- Loads 50 reports per page.

### Report List

The list displays individual reports in either a responsive table (desktop) or
compact cards (mobile).

Each row/card shows:

- **Project name** – Link to the project's overview.
- **Report summary** – Clickable link showing the report **subject** (bold)
  followed by a truncated **error message**. Clicking opens the full individual
  report detail.
- **Status** – Icons indicating the current state of the associated error group:
  - Owner (user icon or profile picture)
  - Muted or snoozed (bell icons)
  - Resolved (check icon)
  - Hovering the icons reveals a popover with detailed ownership, mute/snooze, and resolution information.
- **Occurred at** – Relative time (e.g., "5 minutes ago").
  - Hovering reveals the exact UTC timestamp in a popover.

This dashboard complements the **All Errors** view by letting you drill into the
raw stream of incoming reports, making it ideal for monitoring live traffic or
troubleshooting issues that may not yet be grouped effectively.
