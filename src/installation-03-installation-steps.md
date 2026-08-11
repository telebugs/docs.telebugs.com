# Installation Steps

The whole process takes less than 5 minutes. Here is how to get started.

1. **Choose a server.** Pick a machine to host Telebugs (cloud or local). I
   recommend DigitalOcean (see the [DigitalOcean setup guide][3]) or Hetzner
   (see the [Hetzner setup guide][4]).

2. **Point your domain.** Update your DNS records so your domain points directly
   to your server IP. Do not use proxying. Telebugs handles TLS itself.

   ![Cloudflare DNS configuration example][1]

3. **Connect to your server.** Use SSH or your provider console.

4. **Run the installation command.** Copy the command from your purchase email
   and paste it into the server terminal. Installation can take up to 5 minutes.

   Your personal command will look similar to this:

   ```bash
   bash -c "$(curl -fsSL https://auth.telebugs.com/install/a12b-c34d-e56f-g78h)"
   ```

   **Important:** Keep your install command private. Do not share it or post it
   online. It is tied to your account and license. The purchase token is included
   in your email.

When you run this command, it will automatically install Docker on your server
(assuming you’re using Linux, which is standard for most cloud environments). It
will then download the latest version of the Telebugs app as a Docker container.
During setup, you’ll be prompted to enter your domain name so we can generate a
TLS certificate for you.

![Successful Telebugs installation][2]

That is it. Visit `https://YOUR-DOMAIN` in your browser to create the first
user. After that, you can invite your team.

Telebugs updates itself automatically every night at 1 AM (server local time).
You can disable updates or run other admin tasks (backups, password resets,
etc.) with the [telebugs command][5]. Connect to your server and run `telebugs`
to see all options.

After first launch, run `telebugs status` on the server. Before sending
production errors, create an off-server [backup and restore plan][6] and decide
whether your external monitoring should check [`/ready`][7].

> 💡 Want multiple Telebugs installations? You need a separate license for each domain.

## Replacing or Recovering an Existing Server

Do not follow the normal installation steps or run `telebugs setup` on a
replacement server. Install only the recovery CLI:

```bash
bash -c "$(curl -fsSL https://auth.telebugs.com/restore)"
```

Then copy your backup, run `telebugs data verify`, and follow the
[backup and restore runbook][6]. Restore uses the exact licensed domain captured
in the archive. The runbook covers format-1 authorization, format-2 offline
receipts, Docker and registry requirements, local checks, direct DNS cutover,
ports 80/443, TLS, and rollback.

[1]: assets/images/installation-03-installation-steps/01.webp
[2]: assets/images/installation-03-installation-steps/02.webp
[3]: /appendix-04-installing-on-digital-ocean.md
[4]: /appendix-05-installing-on-hetzner.md
[5]: /appendix-02-telebugs-command-reference.md
[6]: /operations-01-backup-and-restore.md
[7]: /operations-02-health-and-status.md
