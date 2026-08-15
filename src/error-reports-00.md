# Error Reports

Telebugs collects rich error reports using compatible Sentry SDKs. Each report
contains stack traces, request data, breadcrumbs, tags, and more to help you
diagnose problems quickly.

Similar errors are automatically grouped into issues to reduce noise.

Teams can add notes (with attachments) to discuss and track resolution (see
[Notes and Collaboration][1]).

## Investigating with a Coding Agent

If your coding agent is connected to Telebugs MCP, open an error group or an
individual report and select **Copy for LLMs**. Paste the copied prompt into the
agent while it has the corresponding repository open.

The clipboard prompt contains stable Telebugs identifiers and generic workflow
instructions only. It does not include error messages, backtraces, request
data, user data, notes, secrets, or other production payloads. The action only
copies text; it does not start an agent or edit code.

The agent uses its authorized Telebugs MCP connection to retrieve the error
context, inspect the repository, and propose a fix without editing first. See
[Agent Investigations][2] for the complete workflow and security model.

## Keyboard Navigation

When viewing the reports within an error group, use `J` / `K` or the arrow keys
to move through the visible reports. Use `O` or `Enter` to open the highlighted
report, or press `Escape` to clear the highlight.

On an individual report, use `P` / `N` for the previous or next occurrence and
`U` to return to the originating list. `R`, `M`, and `A` provide the current
resolve, mute, and self-claim actions on every error-group tab.

Press `Command-K` or `Control-K` to open the command palette. On the Reports
tab it can open message search and date filters. On an individual report it
includes available occurrence navigation and error actions.

The Reports chart includes **View data table**, which exposes exact time-series
values and release links in a keyboard-accessible format. With the table open,
select **Download CSV** to export the selected range. Comparison exports include
both periods.

See [Accessibility](/account-settings-02-accessibility.md) for the complete
shortcut reference, custom assignments, favorites, and safety behavior.

See the following sections for details.

[1]: /error-reports-03-notes-and-collaboration.md
[2]: /telebugs-mcp-09-agent-investigations.md
