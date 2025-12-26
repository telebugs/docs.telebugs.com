# Email

Emails go to your account email.

To configure:

1. Go to **Notification Configuration** > **Email**.
2. Fill the form and save.
3. Test with **Send test email**.
4. Disable with the toggle.

## Configuration Form

The **Email notifications configuration form** defines global settings that all projects inherit. Complete the fields as follows:

- **Provider:** Select your email provider from the dropdown. Telebugs supplies preset configurations for common providers (Gmail, Outlook, etc.). Choose **Custom SMTP** to enter your own server settings manually.
- **Outgoing (SMTP) server:** Enter the SMTP server address used to send emails (for example, `smtp.gmail.com` for Gmail). This field is required.
- **Port:** Specify the port number for the SMTP server. Typically `587` (TLS) or `465` (SSL). This field is required.
- **Username:** Enter the username for your SMTP server—usually your email address or the username provided by your email service. Leave blank if authentication is not required. Required if your provider requires login.
- **Password:** Enter the password for your SMTP account. Leave blank if authentication is not required. Required if your provider requires login.
- **Domain:** The HELO domain used by the SMTP server (for example, `example.com`). This field is required.
- **From address:** The email address that appears as the sender of notification emails. Commonly, a `no-reply` address. Optional.
- **Encryption:** Select the encryption method for the SMTP connection: **None**, **SSL**, or **TLS**. This field is required.
- **Authentication:** Specify if SMTP authentication is required: **None**, **Login**, or **Plain**. If you choose an option other than **None**, you must provide a username and password. This field is required.
