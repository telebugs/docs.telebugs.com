# Account Settings

Account settings let you update your profile, manage security, and control
notifications.

Click your profile icon in the top-right and select **Account Settings**.

The page includes a sidebar navigation with sections such as **General**,
**Security**, **Sessions**, and **Notifications**.

## General

The General section contains settings for your profile, name, and local
development preferences.

### Profile Picture

Your profile picture shows next to your name in the dashboard and team views.

To upload or change it:

1. In the **Your profile picture** card, click the preview area (shows your
   current picture or the default user icon).
2. Select a new image file from your device.
3. The preview updates immediately.
4. Click **Update profile picture**.

To remove it and revert to the default icon:

1. Hover over (or click) the preview area – a trash icon overlay will appear if
   a custom picture is set.
2. Click the trash icon to clear the picture.
3. Click **Update profile picture** to confirm.

### Changing Your Name

Your name appears in team lists and notes.

To change it:

1. In the **Your name** card, enter your new full name in the text field.
2. Click **Change name**.

There are no restrictions on length or characters.

### Preferred Local Editor

Choose your preferred text editor for "Open in Editor" links in error
backtraces. This allows you to quickly open source files locally from Telebugs.

To set it:

1. In the **Preferred local editor** card, select your editor from the **Local
   editor** dropdown.
   - Options include **None (disable local open)** and supported editors (e.g.,
     VS Code, RubyMine, etc.).
2. Click **Update editor preference**.

### Local Source Code Paths (per project)

Configure the local path to each project's source code on your machine. This
enables "Open in Editor" links for errors from production/deployed environments
when a preferred editor is selected.

To configure paths:

1. In the **Local source code paths (per project)** card, find your projects listed.
2. For each project, enter the full local filesystem path to its source code in
   the text field.
   - A placeholder example is provided (e.g., `/Users/username/projects/project-name`).
3. Click **Update local paths** at the bottom of the card.

If you are not a member of any projects yet, a message "You are not a member of
any projects yet." will be shown instead of the form.

## Security Settings

Go to the **Security** tab for email and password.

### Change Email Address

Enter your new email and current password, then click **Change email**.

Verify the new email via the confirmation link sent to it.

### Change Password

Enter your current password, new password, and confirmation.

Click **Change password**.

## Log In on Another Device

Generate a sign-in link for quick access on new devices.

Go to the **Sessions** tab, then copy the link from **Log in on another
device**.

The link expires after 4 hours. Do not share it.

## Notification Preferences

Control which projects send you email notifications.

Go to the **Notifications** tab, then toggle checkboxes for each project.

Changes save automatically.

# API

The **API access** section in Account Settings contains your personal API key.

## Your API Key

Your API key is used to authenticate requests to the Telebugs REST API.

You can find your current API key on this page. Use this key when making
authenticated requests to the API.

## Regenerating Your API Key

If your API key is compromised or you need to rotate it, click **Regenerate**.

After regenerating:

- Copy the new key immediately.
- Update any integrations or scripts that use the old key.
- The previous key will stop working.

## Using the API

For documentation on available endpoints and how to use the API, see the [REST
API](/rest-api-00-getting-started.md) section.

## Connected MCP Apps

AI coding tools can connect to Telebugs via the
[Model Context Protocol (MCP)](/telebugs-mcp-00-getting-started.md). After
authorizing a tool, you can review and revoke its access from **Account
Settings → Connected MCP apps**.
