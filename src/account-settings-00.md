# Account Settings

Account settings let you update your profile, manage security, configure local
development, and control notifications.

Click your profile icon in the top-right and select **Account Settings**.

On desktop, the navigation is grouped into **Personal**, **Security**, and
**Developer** sections. On smaller screens, use the **Settings section**
selector. The available pages are **Profile**, **Appearance**,
**Accessibility**, **Notifications**, **Security**, **Local development**,
**API access**, and **Connected apps**.

<span id="profile"></span>
<h2 id="general">Profile</h2>

The **Profile** page contains only your profile picture and name.

### Profile Picture

Your profile picture shows next to your name in the dashboard and team views.

To upload or change it:

1. In the **Your profile picture** card, click the preview area (it shows your
   current picture or the default user icon).
2. Select a new image file from your device.
3. The preview updates immediately.
4. Click **Update profile picture**.

To remove it and revert to the default icon:

1. Hover over or focus the preview area. A trash icon appears when a custom
   picture is set.
2. Click the trash icon to clear the picture.
3. Click **Update profile picture** to confirm.

### Changing Your Name

Your name appears in team lists and notes.

To change it, enter your full name in the **Your name** card and click **Change
name**.

There are no restrictions on length or characters.

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

## Accessibility

Use **Account Settings → Accessibility** to configure keyboard access,
shortcuts, and command palette preferences. See
[Accessibility](account-settings-02-accessibility.md).

## Security Settings

Use **Account Settings → Security** for email, password, and device sign-in.

### Change Email Address

Enter your new email address and current password, then click **Change email**.

### Change Password

Enter your current password, new password, and confirmation, then click
**Change password**.

## Log In on Another Device

The **Log in on another device** card is on **Account Settings → Security**.
Copy or share the private sign-in link to sign in on another device.

The link expires after 4 hours. Do not share it with anyone else.

## Notification Preferences

Use **Account Settings → Notifications** to choose which projects send you
notifications. Changes save automatically.

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
