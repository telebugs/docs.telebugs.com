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

- **Project**: Select a specific project or leave as "All" to see errors across
  all your projects.
- **From / To**: Date-time range picker to show only errors whose first or last
  occurrence falls within the specified window. Defaults to the full range of
  available data.
- **Reset link**: Quickly clear all filters.

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
  - Hovering the icon reveals a popover with details about ownership, mute
    status, and resolution.
- **Error type and culprit** – e.g., `TypeError` in `app/controllers/users_controller.rb`.
- **Error message** – Truncated preview, clickable to open the full error group
  detail.
- **Reports count** – Number of individual error reports in the group, with a
  link to view all reports.
- **Seen times** –
  - "Last seen" (e.g., "5 minutes ago") – primary sort key.
  - "First seen" (e.g., "3 days old").
  - Hovering reveals exact UTC timestamps in a popover.

This dashboard is ideal for triaging new or recurring issues across your entire
deployment, spotting widespread problems, or monitoring overall error volume.
