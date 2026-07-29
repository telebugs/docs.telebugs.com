# All Errors

The **All Errors** view provides a global, cross-project overview of all error
groups in your Telebugs instance. It lists every grouped error (issue) that you
have access to, sorted by the most recently seen.

This is one of the main entry points to Telebugs and is especially useful when
managing multiple projects or when you want to see the overall health of your
entire system at a glance.

> **Note:** Only errors from projects you are a member of are shown.

## Key Features

### Filtering

You can narrow down the list using the filter controls at the top of the page
(all times are in UTC):

- **Project**: Select a specific project or leave it at **All projects** to see
  errors across every project you can access.
- **Date preset**: Choose **All time**, **Today**, **Last 7 days**, **Last 28
  days**, or **Last 91 days**.
- **Custom range**: Set a From time, a To time, or both. Custom boundaries are
  interpreted and displayed in UTC.
- **Clear filters**: Return to all projects and all available history.

On desktop, project and preset changes apply immediately. On a narrow screen,
Telebugs opens the filters in a sheet so you can stage several changes and
apply them together.

### Status Tabs

Segmented control to switch between:

- **unresolved** – Active errors that have not been resolved (default view).
- **resolved** – Errors that have been marked as resolved.
- **all** – Both unresolved and resolved errors.

### Sorting and Pagination

- Errors are sorted by **last seen** time (most recent first).
- Infinite-style cursor-based pagination with **Previous** / **Next** arrows.
- Loads 50 errors per page.

### Error List

The list displays error groups in either a responsive table (desktop) or compact
cards (mobile).

Each row/card shows:

- **Project name** – Link to the project's overview.
- **Error icon** – A generated bug illustration or the first screenshot/image
  from the error reports.
  - Badges overlay the icon if the error has an **owner**, is **muted/snoozed**,
    or is **resolved**.
  - Hovering, focusing, or activating the labelled status button reveals
    details about ownership, mute status, and resolution.
- **Error type and culprit** – e.g., `TypeError` in `app/controllers/users_controller.rb`.
- **Error message** – Truncated preview, clickable to open the full error group
  detail.
- **Reports count** – Number of individual error reports in the group, with a
  link to view all reports.
- **Seen times** –
  - "Last seen" (e.g., "5 minutes ago") – primary sort key.
  - "First seen" (e.g., "3 days old").
  - Hovering, focusing, or activating the timestamp button reveals exact UTC
    timestamps.

This dashboard is ideal for triaging new or recurring issues across your entire
deployment, spotting widespread problems, or monitoring overall error volume.

## Keyboard Navigation

Use `J` / `K` or the arrow keys to move through the visible errors, and use `O`
or `Enter` to open the highlighted error. Press `X` to add or remove the
highlighted error from the bulk selection, or `Escape` to clear the highlight.

Press `Command-K` or `Control-K` to open the command palette. It can change the
status, project, or date filter, clear active filters, and run applicable bulk
resolve, mute, or merge actions for selected errors.

When character shortcuts are enabled, the date presets are also available
directly from the keyboard. The command palette shows the bindings that apply
to the current page.

See [Accessibility](/account-settings-02-accessibility.md) for the complete
shortcut reference, custom assignments, favorites, and safety behavior.
