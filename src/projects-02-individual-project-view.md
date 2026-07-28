# Individual Project View

Click a project to open its dashboard for analyzing errors.

Key elements:

- Project picker dropdown: Switch projects or access settings.
- Releases link: View release history.
- Search bar: Find errors by message, type, or details (live updates).
- Date range selector: Filter by time (e.g., today, last week) with pager.
- Stats overview: Total reports, new vs. reoccurred.
- Interactive chart: Error volume over time; expand it for closer inspection.
  Open **View data table** for exact values and release links, or download the
  displayed data as CSV.
- Error list: Grouped unique errors with type, message, timestamp, and count. Click for details.
- Filters: All, resolved, unresolved; sort by last seen or count.

If no errors, dashboard shows SDK setup instructions. Refreshes automatically as reports arrive.

Use search and filters to triage high-volume unresolved errors. Chart helps spot deploy or traffic patterns.

## Chart Data and CSV Exports

The chart is the quickest way to spot spikes and changes over time. Select
**Expand chart** for more vertical detail.

Select **View data table** when you need exact values, keyboard navigation, or
a screen-reader-friendly alternative to the visual chart. The table follows
the selected date range and includes both periods when comparison is enabled.
Release links appear when a release marker falls within the displayed range.

With the table open, select **Download CSV** to export the same rows. The CSV
includes the selected comparison periods and release labels, making it useful
for spreadsheets, incident reviews, and sharing trend data outside Telebugs.

## Keyboard Navigation

Use `J` / `K` or the arrow keys to move through the visible errors, and use `O`
or `Enter` to open the highlighted error. Press `X` to add or remove the
highlighted error from the bulk selection, or `Escape` to clear the highlight.

Press `Command-K` or `Control-K` to search errors, change the status or date
filter, run applicable actions for selected errors, or navigate to another
project or application.

See [Accessibility](/account-settings-02-accessibility.md) for the complete
shortcut reference, custom assignments, favorites, and safety behavior.
