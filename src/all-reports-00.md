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

- **Project**: Select a specific project or leave it at **All projects** to see
  reports across every project you can access.
- **Date preset**: Choose **All time**, **Today**, **Last 7 days**, **Last 28
  days**, or **Last 91 days**.
- **Custom range**: Set a From time, a To time, or both. Custom boundaries are
  interpreted and displayed in UTC.
- **Clear filters**: Return to all projects and all available history.

On desktop, project and preset changes apply immediately. On a narrow screen,
Telebugs opens the filters in a sheet so you can stage several changes and
apply them together.

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
  - Hovering, focusing, or activating the labelled status button reveals
    detailed ownership, mute/snooze, and resolution information.
- **Occurred at** – Relative time (e.g., "5 minutes ago").
  - Hovering, focusing, or activating the timestamp button reveals the exact
    UTC timestamp.

This dashboard complements the **All Errors** view by letting you drill into the
raw stream of incoming reports, making it ideal for monitoring live traffic or
troubleshooting issues that may not yet be grouped effectively.

## Keyboard Navigation

Use `J` / `K` or the arrow keys to move through the visible reports, and use
`O` or `Enter` to open the highlighted report. Press `Escape` to clear the
highlight.

Press `Command-K` or `Control-K` to open the command palette and change the
project or date filter, clear active filters, or navigate elsewhere.

When character shortcuts are enabled, the date presets are also available
directly from the keyboard. The command palette shows the bindings that apply
to the current page.

See [Accessibility](/account-settings-02-accessibility.md) for the complete
shortcut reference, custom assignments, favorites, and safety behavior.
