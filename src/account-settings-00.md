# Account Settings

Account settings let you update your profile, manage security, configure local
development, and control notifications.

Click your profile icon in the top-right, then select the block containing your
name, email address, and role to open **Profile**. On desktop, use the settings
sidebar to move between pages. Related pages are separated by whitespace. On
smaller screens, use the **Settings section** selector. The page title stays
visible as you scroll.

The available pages are **Profile**, **Appearance**, **Keyboard shortcuts**,
**Command palette**, **Notifications**, **Security**, **Local development**,
**API access**, and **Connected apps**.

<span id="profile"></span>
<h2 id="general">Profile</h2>

The **Profile** page contains your photo and full name. Your name, email, and
access-level badge appear in the settings sidebar and account menu.

### Profile Picture

Your profile picture shows next to your name in the dashboard and team views.

To upload or change it, click your photo or **Choose photo**, then select a
JPEG, PNG, or WebP image. Hovering over or focusing the photo reveals **edit**.
The photo saves automatically after selection. Select **Remove photo** to
return to the default avatar.

### Changing Your Name

Edit **Full name** to change the name shown in team lists and notes. Changes
save automatically after you pause typing or leave the field. A green tick
beside the input confirms that the name was saved.

Photo and name changes save automatically. If a save fails, the page shows an
error and a **Retry** action. The help icon below the card opens the relevant
manual page.

## Local Development

Use **Account Settings → Local development** to configure editor links and
local source paths.

### Preferred Local Editor

Choose the editor used by **Open in Editor** links in error backtraces.

1. In the **Preferred local editor** card, select an editor from the **Local
   editor** menu.
2. Select **None (disable local open)** to disable editor links.
3. Click **Update editor preference**.

### Local Source Code Paths (per project)

Configure the local path to each project's source code on your machine. This
lets Telebugs open source files from production error backtraces in your
preferred editor.

Configured projects appear as independently editable rows:

1. Enter or update the full local filesystem path for a configured project.
2. Click **Save path**.
3. Use **Remove path** to remove a mapping explicitly.

To configure another project, click **Add project path**, select an active
project, enter its local source path, and save it. Projects that already have a
mapping are not offered in the picker.

## Appearance

Use **Account Settings → Appearance** to choose the color scheme, text size,
and related display preferences. See [Appearance](account-settings-01-appearance.md).

<span id="accessibility"></span>
## Keyboard Shortcuts

Use **Account Settings → Keyboard shortcuts** to enable or disable
character-key shortcuts and customize key bindings. Use **Find shortcut** to
filter the grouped list. See [Keyboard shortcuts](account-settings-02-accessibility.md).

## Command Palette

Use **Account Settings → Command palette** to review and manage favorite
commands. Use **Find command** to filter the catalogue. These preferences have
their own page in the sidebar. See [Command palette](account-settings-03-command-palette.md).

## Security Settings

Use **Account Settings → Security** to manage your sign-in details and get a
private link for signing in on another device. Email and password changes open
in dialogs and require explicit submission. A green tick beside the changed
setting confirms that it was saved. The help icon below the cards opens this
reference.

<span id="email-address"></span>

### Change Email Address

On **Account Settings → Security**, select the edit icon beside **Email address**. Enter your new email address and account password, then
select **Change email**. Your updated email also appears in the settings sidebar
and account menu.

### Change Password

Select **Change password** in the **Password** row. Enter your current password,
new password, and confirmation, then select **Change password** in the dialog.

If the change succeeds, the dialog closes and a green tick appears beside the
action. If it fails, the dialog shows an error so you can try again. Password
fields are cleared after a submission or when you close the dialog.

## Log In on Another Device

The **Log in on another device** card is on **Account Settings → Security**.
Use the copy icon beside **Sign-in link** to copy the private link. A tick
confirms it was copied. The share icon is available when your browser supports
sharing. You can also select and copy the link directly from the field.

The link expires after 4 hours. Do not share it with anyone else.

## Notification Preferences

Use **Account Settings → Notifications** to choose which projects send you
notifications. The list shows active projects you belong to, with a switch for
each project. These switches control your own notification preferences. Select
a project name to open that project.

Changes save automatically. A green tick beside the changed switch confirms
the save. If a change cannot be saved, **Not saved** and **Retry** appear beside
that switch. Select **Retry** to save your chosen value again.

The help icon below the project list opens this reference.

<h2 id="api">API Access</h2>

The **API access** page contains your personal API key and links to the REST API
documentation.

### Your API Key

Your API key authenticates requests to the Telebugs REST API. Treat it like a
password and do not commit it to source control.

### Regenerating Your API Key

If your API key is compromised or needs rotation, click **Regenerate**.

After regenerating:

- Copy the new key immediately.
- Update integrations and scripts that use the old key.
- The previous key stops working.

### Using the API

See the [REST API](/rest-api-00-getting-started.md) documentation for available
endpoints and examples.

<span id="connected-apps"></span>
<h2 id="connected-mcp-apps">Connected Apps</h2>

AI coding tools can connect to Telebugs through the
[Model Context Protocol (MCP)](/telebugs-mcp-00-getting-started.md). After
authorizing a tool, review or revoke its access from **Account Settings →
Connected apps**.

The page retains the `/settings/mcp` application URL for compatibility. MCP
remains the protocol name used in setup instructions and technical references.
