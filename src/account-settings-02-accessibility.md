# Accessibility

The **Accessibility** settings let you control Telebugs' character-key
shortcuts for your account.

To open them, click your profile icon in the top-right corner, select **Account
Settings**, then select **Accessibility** from the sidebar.

## General Keyboard Access

Press `Tab` after a page loads to reveal **Skip to main content**. Activating it
moves focus past the repeated navigation and into the page content.

Telebugs shows a visible focus indicator on links, buttons, fields, switches,
menus, and other interactive controls. Dialogs and mobile sheets move focus to
a useful control when they open, close with `Escape`, keep focus inside while
open, and return focus to the control that opened them.

Status and timestamp details that appear on pointer hover are also available
by focusing or activating their labelled buttons. Press `Escape` to close an
open detail popover.

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
`U`, `R`, `M`, `A`, and `?` shortcuts, together with the `G` navigation
sequences. Native `Tab` and `Enter` behavior remains available. You can also
focus a list with `Tab` and use the arrow keys to move through it.

The modifier-based `Command-K` or `Control-K` command palette remains available
when character-key shortcuts are disabled.

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
| Authenticated pages | `G`, then `P` | Go to Projects. |
| Authenticated pages | `G`, then `E` | Go to All Errors. |
| Authenticated pages | `G`, then `R` | Go to All Reports. |
| Authenticated pages | `G`, then `S` | Go to Account Settings. |
| Outside editing fields | `Command-K` or `Control-K` | Open the command palette. |
| Inside editing fields | `Command-Option-K` or `Control-Alt-K` | Open the command palette without replacing the field's native shortcut. |
| Supported pages | `?` | Open the shortcuts available on the current page. |

You can open the shortcut reference by pressing `?` when character-key
shortcuts are enabled. It is always available by opening the account menu and
selecting **Keyboard shortcuts**.

## Command Palette

Open the command palette with `Command-K` on macOS or `Control-K` on other
platforms. You can also open the account menu and select **Command palette**.

Start typing to find:

- Projects and applications you can access
- Global destinations such as All Errors, All Reports, and Account Settings
- Navigation and error actions available on the current page
- Existing search, status, project, and date filters
- Applicable bulk actions when errors are selected

Use `ArrowUp` and `ArrowDown`, `Home`, or `End` to change the active result,
then press `Enter` to run it. `Command-Enter` or `Control-Enter` opens a
navigation result in a new tab; it never submits an action. Press `Escape`, use
the opening shortcut again, or select the close button to close the palette.

Telebugs does not replace the normal `Command-K` or `Control-K` behavior while
you are editing a field. Use `Command-Option-K` on macOS or `Control-Alt-K` on
other platforms when you intentionally want the palette from an editing
field.

Palette actions use the same visible controls, permissions, confirmations, and
endpoints as pointer interaction. Project and application results are loaded
only from resources your account can access.

## Global Navigation Sequences

Press `G`, then `P`, `E`, `R`, or `S` to navigate globally. A small **Go to**
reference appears after `G` and lists the valid second keys. The sequence
cancels after three seconds, when you press `Escape`, or when you press an
unrecognized second key. It never falls through and activates another
single-key command.

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

The same actions appear in the command palette when they are available. When
errors are selected on an error list, the palette also exposes applicable
resolve, unresolve, mute, unmute, and merge actions with the selected count.
Merge retains its existing confirmation.

## Charts and Data Tables

Charts include a **View chart data** control. Open it to read the chart as a
table with time labels, current values, comparison values when present, and
links to applicable releases. This table is the nonvisual and keyboard
alternative to inspecting points on the canvas.

Small decorative trend charts are skipped by screen readers when the same
change is already written next to them.

## Notes and File Attachments

The note attachment control works with a file picker as well as drag and drop.
After you choose files, Telebugs announces the updated file count. Each queued
file has a labelled removal button, and removing a file returns focus to the
next file, the previous file, or the attachment control.

Upload progress, successful note creation, and validation failures are exposed
as status or alert messages without moving focus unexpectedly.

## Display Preferences

Telebugs respects the operating system's reduced-motion preference and keeps
controls and focus indicators distinguishable in forced-colors modes. Browser
zoom and text-size controls can be used without changing the keyboard
shortcuts described here.

## When Shortcuts Are Paused

Shortcuts do not activate while you are:

- Typing in an input, text area, or editable region
- Using a select control
- Interacting with an open dialog or menu
- Composing text with an input method editor
- Holding a modifier for a shortcut other than the documented command-palette
  chords

The layout-generated `Shift` needed to type `?` is allowed; other modified
character commands are left to the browser and operating system. Held keys do
not repeatedly open pages, show help, or submit actions. `J`, `K`, and arrow
movement may repeat so you can move through a list efficiently.
