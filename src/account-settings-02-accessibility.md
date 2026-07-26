# Accessibility

The **Accessibility** settings let you control Telebugs' character-key
shortcuts for your account.

To open them, click your profile icon in the top-right corner, select **Account
Settings**, then select **Accessibility** from the sidebar.

## Character-Key Shortcuts

Character-key shortcuts are enabled by default. They provide fast navigation on
these list pages:

- **All Errors**
- The error list on an individual project page
- **All Reports**
- The report list within an error group

To disable or re-enable them:

1. Open **Account Settings → Accessibility**.
2. Clear or select **Enable character-key shortcuts**.
3. Click **Update accessibility**.

Disabling this setting turns off the printable `J`, `K`, `O`, `X`, and `?`
shortcuts. Native `Tab` and `Enter` behavior remains available. You can also
focus a list with `Tab` and use the arrow keys to move through it.

## Shortcut Reference

| Shortcut | Action |
| --- | --- |
| `J` or `ArrowDown` | Highlight and focus the next visible item. |
| `K` or `ArrowUp` | Highlight and focus the previous visible item. |
| `O` or `Enter` | Open the highlighted item's primary link. |
| `X` | Select or deselect the highlighted item on an error list. |
| `Escape` | Clear the list highlight. |
| `?` | Open the keyboard shortcut reference. |

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
browser's Back button or updating a list with search or filters can restore the
highlight if that item is still visible. On responsive pages, only the visible
desktop or mobile version of an item participates in navigation.

## When Shortcuts Are Paused

List shortcuts do not activate while you are:

- Typing in an input, text area, or editable region
- Using a select control
- Interacting with an open dialog or menu
- Composing text with an input method editor
- Holding `Shift`, `Command`, `Control`, or `Alt`

The `?` help shortcut remains available because typing it may require `Shift`
on your keyboard.
