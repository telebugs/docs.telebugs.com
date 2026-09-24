# Account Settings

Account settings let you update your profile, manage security, configure local
development, and control notifications.

Click your profile icon in the top-right, then select the block containing your
name, email address, and role to open **Account**. On desktop, use the settings
sidebar to move between pages. Related pages are separated by whitespace. On
smaller screens, use the **Settings section** selector. The page title stays
visible as you scroll.

The available pages are **Account**, **Appearance**, **Notifications**,
**Keyboard shortcuts**, **Command palette**, **Local development**, **API access**,
and **Connected apps**.

<span id="account"></span>
<span id="profile"></span>
<h2 id="general">Account</h2>

The **Account** page brings your personal details and sign-in settings together:

- **Personal details:** photo, full name, and email address.
- **Sign-in:** password.
- **Log in on another device:** your private sign-in link.

Your name, email, and access-level badge appear in the settings sidebar and
account menu. Select this identity block to return to Account. There is no
separate Security menu item.

Account keeps the `/settings/profile` URL. Old `/settings/security` links redirect
to Account, and `/settings/sessions` links open its device sign-in section.

### Profile Picture

Your profile picture shows next to your name in the dashboard and team views.

To upload or change it, click your photo or **Choose photo**, then select a
JPEG, PNG, or WebP image. Hovering over or focusing the photo reveals **edit**.
The photo saves automatically after selection. Select **Remove photo** to
return to the default avatar.

### Changing Your Name

Under **Account → Personal details**, select the edit icon beside **Full name**.
Enter your name in the dialog, then select **Save**. The updated name appears in
team lists, notes, the settings sidebar, and the account menu. A green tick beside
the name confirms that it was saved.

Select **Cancel** or press **Escape** to discard your changes. If saving fails,
the dialog keeps your entered name and shows an error; select **Save** to retry.

Photo changes still save automatically. If a photo save fails, use **Retry** beside
the error. The help icon below the Account cards opens this manual page.

<h3 id="security-settings">Email and Password</h3>

Email and password changes open in dialogs and require your current password
and explicit submission. A green tick beside the changed setting confirms that
it was saved.

<span id="email-address"></span>

#### Change Email Address

Under **Account → Personal details**, select the edit icon beside **Email address**.
Enter your new email address and current password, then
select **Save**. Your updated email also appears in the settings sidebar
and account menu.

#### Change Password

Under **Account → Sign-in**, the **Password** row shows a fixed eight-dot mask,
unrelated to your password’s length. Select the edit icon beside it. Enter your current password, new password,
and confirmation, then select **Change password** in the dialog.

If the change succeeds, the dialog closes and a green tick appears beside the
action. If it fails, the dialog shows an error so you can try again. Password
fields are cleared after a submission or when you close the dialog.

### Log In on Another Device

The **Log in on another device** card is on **Account**.
Use the copy icon beside **Sign-in link** to copy the private link. A tick
confirms it was copied. The share icon is available when your browser supports
sharing. You can also select and copy the link directly from the field.

The link expires after 4 hours. Do not share it with anyone else.

## Local Development

Use **Account Settings → Local development** to configure editor links and
local source paths.

### Preferred Local Editor

In the **Editor** card, choose an application from **Open files with**. Choose
**None** to disable editor links. Your selection saves
immediately. A green tick confirms the save; if it fails, use **Retry**.

### Local Source Code Paths (per project)

Set each project's source folder on your computer to open files from error
backtraces in your preferred editor. Editor and path preferences belong to
your account.

Configured projects appear as compact rows, grouped by application, with the
project name and its saved path:

1. Select the edit icon beside a project.
2. Enter its full local source path in the dialog and select **Save path**.
3. A green tick confirms the save. **Cancel** leaves the saved path unchanged.

Use the trash icon beside a path to remove its mapping after confirmation.

To configure another project, select **Add project path…** below the list. In
the dialog, search by project or application name, choose a project, and enter
its **Local source path**. **Add** becomes available when both fields
are filled in. Adding closes the dialog and places the path in its application
group. Projects that already have a mapping are omitted from the picker.

**Cancel** or Escape discards the draft. If adding fails, the dialog keeps your
selection and path so you can retry. The same dialog is used on desktop and
mobile.

When more than ten paths are configured, **Filter configured projects** searches
project and application names. The help icon below the settings opens this
reference.

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

## Notification Preferences

Open **Account Settings → Notifications** to manage your project email and push
notifications.

Use **Allow notifications** to turn them off or back on for your account. Turning
it off keeps your individual project choices. The project switches are dimmed
while notifications are off; turning them back on restores the same choices.
This also applies to projects you join later. It does not change another team
member’s preferences, shared webhook deliveries, or account security emails.

Use the project switches to choose which projects you receive notifications
from. The list shows active projects you belong to. Select a project name to open it.

Changes save automatically. A green tick beside the changed switch confirms
the save. If a change cannot be saved, **Not saved** and **Retry** appear beside
that switch. The displayed choice has not taken effect until it is saved; select
**Retry** to try again. Project switches are unavailable while the master switch
saves, and remain unavailable while **Allow notifications** is off.

Turning notifications back on allows future notifications from your selected
projects. Notifications skipped while they were off are not replayed.

The help icon below the project list opens this reference.

<h2 id="api">API Access</h2>

Open **Account Settings → API access** to copy or regenerate your personal API
key and manage project webhooks.

### Your API Key

Your API key authenticates requests to the Telebugs REST API. Treat it like a
password and do not commit it to source control.

Use the copy icon beside the key. A green tick confirms it was copied. You can
also select and copy the key directly from the field. If the browser cannot copy
the key, an error appears below it and the key is selected for manual copying.

### Regenerating Your API Key

If your API key is compromised or needs rotation, select the refresh icon
(**Regenerate API key**) beside the copy icon, then confirm. The confirmation
explains that the current key will stop working immediately. Cancel to keep
your existing key.

After confirmation, the new key appears selected so you can copy it immediately.
A green tick beside the refresh icon confirms the change. Copy the new key and
update any integrations or scripts using the old one. The copy icon always
copies the key currently displayed.

### Using the API

The **REST API documentation** link opens the
[API getting-started guide](/rest-api-00-getting-started.md), with authentication
instructions and links to available endpoints.

### Project Webhooks

The **Webhooks** list shows active projects you belong to and the number of
webhook endpoints configured for each. Select a project to open its webhook
settings. See [Webhooks](/rest-api-08-webhooks.md) for setup and delivery details.

The help icon below the list opens this account-settings reference.

<span id="connected-apps"></span>
<h2 id="connected-mcp-apps">Connected Apps</h2>

AI coding tools can connect to Telebugs through the
[Model Context Protocol (MCP)](/telebugs-mcp-00-getting-started.md). Open
**Account Settings → Connected apps** to set up a connection or review apps
you have authorized.

### Connect an App

Copy the **MCP server URL** using the copy icon. A green tick confirms it was
copied. If copying fails, an error appears below the field and the URL is selected
for manual copying. Add the URL to your AI tool, then sign in and approve its
requested access. The **App setup instructions** link opens the
[connecting guide](/telebugs-mcp-02-connecting.md).

Read access lets an app investigate errors. Write access lets it record findings
and update error status. Your AI tool refreshes its authorized session
automatically.

### Review Authorized Apps

The **Authorized apps** card shows each app's name, icon, and granted access.
Permissions reflect your current authorizations, including sessions with an
expired access token that can still refresh. Select an app's name or disclosure
arrow to see its client ID, which helps distinguish connections with the same
name.

Use the trash icon beside an app to **revoke access**, then confirm. The app is
removed from the list and a green tick confirms the change. This revokes all of
your active or refreshable sessions for that connection without affecting other
users. Cancel to keep the connection. You can reconnect the app later.

Apps using your API key are not listed here. Manage that key under
**Account Settings → API access**. The help icon below the app list opens this
reference.

The page retains the `/settings/mcp` application URL for compatibility. MCP
remains the protocol name used in setup instructions and technical references.
