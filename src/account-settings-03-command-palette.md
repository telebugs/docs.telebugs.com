# Command Palette

The command palette gives you quick access to navigation, actions, projects,
and applications. Its settings page manages your favorite commands.

To open the settings, select your identity block in the account menu, then
choose **Command palette** in the settings sidebar. On a small screen, use the
**Settings section** selector.

## Opening and Using the Palette

Open the command palette with `Command` + `K` on macOS or `Control` + `K` on
other platforms. You can also select **Search** in the navigation bar. Its key
hint follows your customized command-palette binding.

Start typing to find:

- Projects and applications you can access
- Global destinations such as All Errors, All Reports, and Account Settings
- Navigation and error actions available on the current page
- Existing search, status, project, and date filters
- Applicable bulk actions when errors are selected

Use `ArrowUp` and `ArrowDown`, `Home`, or `End` to change the active result,
then press `Enter` to run it. `Command` + `Enter` or `Control` + `Enter` opens
a navigation result in a new tab; it never submits an action. Press `Escape`,
use the opening shortcut again, or select the close button to close the
palette.

Telebugs does not replace the normal `Command` + `K` or `Control` + `K`
behavior while you are editing a field. Use `Command` + `Option` + `K` on
macOS or `Control` + `Alt` + `K` on other platforms when you intentionally
want the palette from an editing field.

Palette actions use the same visible controls, permissions, confirmations, and
endpoints as pointer interaction. Project and application results are loaded
only from resources your account can access.

## Favorites and Recent Commands

When a favoritable command is active in the palette, use the star at the end
of its highlighted row. An outlined star adds the command to favorites; a
filled star removes it. The palette stays open and the command remains in
place while you manage it.

To review the full command catalogue, open **Account Settings → Command
palette**. **Find command** filters by command name or group; clearing the
search restores the complete list. Select the star beside a command to add or
remove it from favorites. Filtering does not change favorites, and saving a
visible command keeps your hidden favorites. **Clear all** removes every
favorite, including those hidden by the current search.

Changes save automatically. A green tick beside the page title confirms the
save and remains visible while you scroll. Failed saves show an error and a
**Retry** action. These changes keep your key bindings and the character-key
switch unchanged.

Favorites sync with your Telebugs account and appear first the next time the
palette opens with an empty search.

Commands you run from the palette appear in **Recent** suggestions on that
browser. Recent commands are deduplicated and limited to ten. They stay in the
browser's local storage and are never synced or sent to Telebugs. Project and
application results, raw keystrokes, and shortcuts used outside the palette
are not added to this history.

Favorites and recent entries never make a command appear on a page where it is
unavailable. Projects, applications, current-project results, and dynamic
project filters cannot be favorited.

## Customizing the Opening Shortcut

Choose **Keyboard shortcuts** in the settings sidebar, or **Customize
shortcuts** in the palette footer. The **Command palette** group includes
bindings for opening the palette outside and inside editing fields. See
[Customizing shortcuts](account-settings-02-accessibility.md#customizing-shortcuts).
