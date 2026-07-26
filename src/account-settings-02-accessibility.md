# Accessibility

The **Accessibility** settings let you control Telebugs' character-key
shortcuts for your account.

To open them, click your profile icon in the top-right corner, select **Account
Settings**, then select **Accessibility** from the sidebar.

## Character-Key Shortcuts

Character-key shortcuts are enabled by default. They provide fast navigation
and error-group actions on these pages:

- **All Errors**
- The error list on an individual project page
- **All Reports**
- The report list within an error group
- Individual report pages
- The **Details**, **Reports**, and **Notes** tabs of an error group

To disable or re-enable them:

1. Open **Account Settings → Accessibility**.
2. Clear or select **Enable character-key shortcuts**.
3. Click **Update accessibility**.

Disabling this setting turns off the printable `J`, `K`, `O`, `X`, `P`, `N`,
`U`, `R`, `M`, `A`, and `?` shortcuts. Native `Tab` and `Enter` behavior
remains available. You can also focus a list with `Tab` and use the arrow keys
to move through it.

## Shortcut Reference

| Context | Shortcut | Action |
| --- | --- | --- |
| Error and report lists | `J` or `ArrowDown` | Highlight and focus the next visible item. |
| Error and report lists | `K` or `ArrowUp` | Highlight and focus the previous visible item. |
| Error and report lists | `O` or `Enter` | Open the highlighted item's primary link. |
| Error lists | `X` | Select or deselect the highlighted error. |
| Error and report lists | `Escape` | Clear the list highlight. |
| Individual report | `P` | Open the previous occurrence in the active ordering. |
| Individual report | `N` | Open the next occurrence in the active ordering. |
| Individual report | `U` | Return to the originating list. |
| Any error-group tab | `R` | Resolve or unresolve the error. |
| Any error-group tab | `M` | Open mute choices, or immediately unmute or unsnooze the error. |
| Any error-group tab | `A` | Claim or unclaim the error for yourself. |
| Supported pages | `?` | Open the shortcuts available on the current page. |

You can open the shortcut reference by pressing `?` when character-key
shortcuts are enabled. It is always available by opening the account menu and
selecting **Keyboard shortcuts**.

## How List Navigation Works

The list highlight is a cursor, not a selection. Moving with `J`, `K`, or the
arrow keys does not select an error or change any data. Use `X` separately when
you want to add or remove an error from the bulk selection.

Forward movement starts at the first visible item. Backward movement starts at
the last visible item. Navigation stops at the first or last item on the
current page and does not automatically change pages.

Telebugs remembers the highlighted item when possible. Returning with the
browser's Back button, using `U` from an individual report, or updating a list
with search or filters can restore the highlight if that item is still visible.
On responsive pages, only the visible desktop or mobile version of an item
participates in navigation.

## Navigating Occurrences

On an individual report page, use `P` and `N` to move through occurrences of
the same error. Navigation stops at the first or last occurrence and never
wraps.

When you open a report from a filtered error-group Reports list, `P` and `N`
follow that list's date range, search, and ascending or descending order across
the complete filtered result, not only the current page. The counter and
visible previous and next controls use the same ordering. Direct links and
reports opened from other lists use all occurrences in chronological order.

Use `U` to return to the originating list. For a report opened in the same tab,
Telebugs restores the exact list URL, filters, pagination, scroll position, and
keyboard cursor when one was visible. A report opened with the pointer returns
without adding a row highlight.

For a direct, shared, or new-tab report, `U` falls back to the error group's
Reports list. It preserves a valid occurrence filter when available; otherwise,
it opens the day containing the current occurrence.

## Error-Group Actions

The `R`, `M`, and `A` shortcuts work on the **Details**, **Reports**, and
**Notes** tabs:

- `R` uses the current **Resolve** or **Unresolve** action.
- `M` opens the existing mute choices when the error is unmuted. Muting still
  requires you to choose a duration or occurrence threshold. When the error is
  muted or snoozed, `M` immediately uses **Unmute** or **Unsnooze**.
- `A` uses **Own it** or **Unclaim** for your account. It is unavailable when
  another person owns the error because Telebugs does not currently support
  reassignment.

These actions use the same visible controls as pointer and touch interaction.
They are ignored while an earlier action is still being processed.

## When Shortcuts Are Paused

Shortcuts do not activate while you are:

- Typing in an input, text area, or editable region
- Using a select control
- Interacting with an open dialog or menu
- Composing text with an input method editor
- Holding `Command`, `Control`, or `Alt`, or using another modifier chord

The layout-generated `Shift` needed to type `?` is allowed; other modified
character commands are left to the browser and operating system. Held keys do
not repeatedly open pages, show help, or submit actions. `J`, `K`, and arrow
movement may repeat so you can move through a list efficiently.
