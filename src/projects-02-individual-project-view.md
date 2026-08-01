# Individual Project View

Click a project to open its dashboard for analyzing errors.

Key elements:

- Project picker: Search the projects you can access, switch to a matching
  project, or open the current project's settings. Press `Enter` when the
  search leaves one match.
- Releases link: View release history.
- Search bar: Find errors by message, type, or details (live updates).
- Date range selector: Filter by time (e.g., today, last week) with pager, and
  compare supported ranges with the immediately preceding period.
- Stats overview: Total reports, new vs. reoccurred.
- Interactive chart: Error volume over time; expand it for closer inspection.
  Open **View data table** for exact values and release links, or download the
  displayed data as CSV.
- Error list: Grouped unique errors with type, message, timestamp, and count. Click for details.
- Filters: unresolved and resolved; sort by last seen or count. Muted errors
  remain in the appropriate list and display a mute-status badge.

If no errors, dashboard shows SDK setup instructions. Refreshes automatically as reports arrive.

Use search and filters to triage high-volume unresolved errors. Chart helps spot deploy or traffic patterns.

## Previous-Period Comparisons

Open the date menu and select **Compare with previous period** to add the
immediately preceding range to the dashboard. For example, **Last 28 days**
compares with the 28 days before it. The date button shows **vs. prev.** while
comparison is active, and totals display the direction and size of the change.

Telebugs aligns the two periods point by point, including partial current
hours, so an in-progress period is not compared with a complete one. Release
markers remain attached to the current period. Select the comparison item
again, press `X`, or use the command palette to turn comparison off.

Comparison is available for bounded ranges. **All time** has no equally sized
preceding period, so its comparison control is hidden. Changing to **All time**
also clears an active comparison.

## Chart Data and CSV Exports

The chart is the quickest way to spot spikes and changes over time. Select
**Expand chart** for more vertical detail.

Select **View data table** when you need exact values, keyboard navigation, or
a screen-reader-friendly alternative to the visual chart. The table follows
the selected date range and includes both periods when comparison is enabled.
Release links appear when a release marker falls within the displayed range.

With the table open, select **Download CSV** to export the same rows. The CSV
contains the displayed timestamps, current values, previous-period values when
enabled, and release labels. It uses the same filters as the chart, making it
useful for spreadsheets, incident reviews, and sharing trend data outside
Telebugs.

## Keyboard Navigation

Use `J` / `K` or the arrow keys to move through the visible errors, and use `O`
or `Enter` to open the highlighted error. Press `X` to add or remove the
highlighted error from the bulk selection, or `Escape` to clear the highlight.

Press `Command-K` or `Control-K` to search errors, change the status or date
filter, run applicable actions for selected errors, or navigate to another
project or application.

See [Accessibility](/account-settings-02-accessibility.md) for the complete
shortcut reference, custom assignments, favorites, and safety behavior.
