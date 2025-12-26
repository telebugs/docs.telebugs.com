# Push Notifications

Push notifications deliver real-time alerts to your desktop browser or mobile device.

Set up global push settings first. Projects can disable them individually, and
users can opt out per project in their profile.

Notifications go to devices where you have granted permission (browser prompt or
device settings).

You can receive alerts for:

- A new error occurring for the first time.
- An error reoccurring after being resolved.
- Error frequency exceeding a threshold (e.g., more than 10 reports in 5 minutes).

For the best mobile experience, install Telebugs as a Progressive Web App (PWA). See the PWA installation section below.

## Configuring Push Notifications

1. Click your profile in the top-right and select **Notification Configuration**.
2. Choose **Push** in the sidebar.
3. Fill the form and click **Save Configuration**.
   A green checkmark appears next to Push when configured.
4. Click **Send test push notification** to verify.
5. If prompted, allow notifications in your browser or device.
   A confirmation shows the test was sent – check your device.
6. To disable globally, toggle off **Enable push notifications**.
   The icon changes to a crossed-out bell.

Real errors will trigger push notifications based on project rules, including the error message, project name, and a direct link.

## Push Configuration Form

- **VAPID subject** (required): A contact URL or email for your instance, e.g., `https://telebugs.example.com` or `mailto:admin@example.com`.

## Installing Telebugs as a Progressive Web App (PWA)

Installing as a PWA gives a native-app feel and more reliable push notifications on mobile. It is optional but recommended.

### Benefits

- Faster loading.
- Push notifications even when the browser is closed.
- Full-screen, app-like experience.

### Android (Chrome)

- Open Telebugs in Chrome.
- Tap the three-dot menu > **Add to Home screen**.
  Or tap the automatic **Install** prompt at the bottom if it appears.
- Confirm **Add** or **Install**.

### iOS (Safari)

- Open Telebugs in Safari.
- Tap the Share icon (square with upward arrow).
- Scroll and select **Add to Home Screen**.
- Tap **Add**.

### Desktop (Chrome) – Optional

- Open Telebugs in Chrome.
- Click the + icon in the address bar or menu > **Install Telebugs**.
- Confirm **Install**.

**Note:** Steps may vary slightly by browser version. Keep your browser updated
and allow notifications when prompted.
