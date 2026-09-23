<span id="accessibility"></span>
# Keyboard Shortcuts

The **Keyboard shortcuts** settings let you control Telebugs' keyboard access
and customize key bindings for your account.

To open them, click your profile icon in the top-right, select your identity
block, then select **Keyboard shortcuts** from the settings sidebar. On a
small screen, use the **Settings section** selector.

Favorite commands have their own [Command palette](account-settings-03-command-palette.md)
settings page. Existing `/settings/accessibility` links open Keyboard shortcuts.

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

1. Open **Account Settings → Keyboard shortcuts**.
2. Turn **Character-key shortcuts** off or on.

The change saves automatically. A green tick beside the page title confirms
the save and stays visible as you scroll. A failed save shows an error and a
**Retry** action.

Disabling this setting turns off the printable `J`, `K`, `O`, `X`, `P`, `N`,
`U`, `R`, `M`, `A`, and `?` shortcuts, together with the `G` navigation
sequences. Native `Tab` and `Enter` behavior remains available. You can also
focus a list with `Tab` and use the arrow keys to move through it.

Modifier-based shortcuts remain available when character-key shortcuts are
disabled. This includes the default `Command` + `K` or `Control` + `K`
command-palette shortcut and any character command that you remap to a
modifier chord.

## Default Shortcut Reference

| Context | Default shortcut | Action |
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
| Outside editing fields | `Command` + `K` or `Control` + `K` | Open the command palette. |
| Inside editing fields | `Command` + `Option` + `K` or `Control` + `Alt` + `K` | Open the command palette without replacing the field's native shortcut. |
| Supported pages | `?` | Open the shortcuts available on the current page. |

Keys joined by a plus sign are pressed together. Keys separated by **then**
are pressed in order.

You can open the shortcut reference by pressing `?` when character-key
shortcuts are enabled. It is always available by selecting **Search** in the
navigation bar and choosing **Keyboard shortcuts** from the command palette.
The Search control displays the current command-palette shortcut, and
**Keyboard shortcuts** appears in the initial suggestions so you do not need
to search for it.

## Customizing Shortcuts

Open **Account Settings → Keyboard shortcuts**. Use **Find shortcut** to search
command names, groups, or the displayed key bindings. Clearing the search
restores the complete list. Filtering does not change any assignments.

Each command shows its current assignment:

1. Select the labelled edit button beside the command.
2. Press the new key, chord, or two-key sequence.

The edit button remains in place while the current key changes to **Press
keys…**. The assignment saves automatically after you finish recording, and
Telebugs shows a green tick beside the title without reloading the page.
Press `Escape` or move focus away to cancel without changing the assignment.

Direct commands accept one printable key or a portable chord containing
`Command` on macOS or `Control` on other platforms. A chord can also include
`Option`/`Alt` or `Shift`. Navigation sequences contain exactly two printable
keys without modifiers. Telebugs uses the character produced by your keyboard
layout rather than the physical key position.

Telebugs does not allow `Tab`, the arrow keys, `Enter`, or `Escape` to be
remapped. These native alternatives remain available even if you clear the
corresponding character shortcut. Browser and operating-system shortcuts such
as `Command` + `L` or `Control` + `L`, reload, closing a tab, and restoring a
tab are also reserved.

Each direct assignment and complete sequence must be unique. A sequence's
first key cannot also be assigned as a direct character shortcut. If a new
assignment conflicts with another command, Telebugs names the conflicting
command and keeps the existing assignments unchanged.

Use the labelled clear icon to leave one command unassigned, or the reset icon
to restore that command's default. **Restore defaults** resets every assignment
after confirmation, including assignments hidden by a search, and keeps your
favorite commands. Conflicts are checked against every assignment, including
filtered-out rows. These changes also save automatically.

## Command Palette

The palette searches commands, projects, and applications. Open it with
**Search** in the header, `Command` + `K` on macOS, or `Control` + `K` on other
platforms. See [Command palette](account-settings-03-command-palette.md) for
navigation, keyboard behavior, and preferences.

The bindings for opening the palette remain on the **Keyboard shortcuts**
settings page with the other key bindings.

### Favorites and Recent Commands

Manage favorites on **Account Settings → Command palette** or with the star
beside an active command in the palette. See
[Favorites and recent commands](account-settings-03-command-palette.md#favorites-and-recent-commands).

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
- Holding an unsupported modifier combination

The layout-generated `Shift` needed to type a printable character is allowed.
Unassigned modifier combinations are left to the browser and operating
system. Held keys do not repeatedly open pages, show help, or submit actions.
List movement may repeat so you can move through a list efficiently.
