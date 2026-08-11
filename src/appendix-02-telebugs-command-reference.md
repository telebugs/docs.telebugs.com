# `telebugs` command reference

Install and manage your Telebugs instance.

To run the `telebugs` command, connect to your server using SSH or your cloud
provider’s web-based terminal.

## Fresh-server recovery bootstrap

Install only the CLI on a fresh replacement server:

```bash
bash -c "$(curl -fsSL https://auth.telebugs.com/restore)"
```

The public bootstrap verifies a platform-specific SHA-256 checksum and installs
`/usr/local/bin/telebugs`. It does not run setup, create configuration, install
Docker, start Telebugs, receive a backup, or restore data.

Do **not** run `telebugs setup` on a replacement server. Copy the archive over,
run `telebugs data verify`, and then `sudo telebugs data restore`. Restore always
uses the licensed domain stored in the archive; it has no domain override.

## Usage

- `telebugs` — Displays the main menu with available commands.

## Manage passwords

- `password` — Manage passwords.

## Manage automatic updates

- `auto-update` — Manage automatic updates.

## Manage application data

- `data backup [filename]` — Stop a running instance, validate all persistent
  data, and create a complete verified backup. The default filename is a UTC
  timestamp. Existing files are never overwritten; plan a maintenance window
  when the stored data is large.
- `data verify <filename>` — Verify a backup manifest and creation timestamp,
  configuration checksum, and every archived file without changing Telebugs.
  - Format-2 backups verify their signed domain receipt offline.
  - Format-1 backups require online exact-domain authorization from
    `auth.telebugs.com`. Verification does not rewrite the archive or persist the
    replacement receipt; a successful restore does. Invalid format-2 receipts
    are never reissued.
- `data restore <filename>` — Verify and stage a backup, then restore it with the
  captured immutable application image. Existing storage and configuration are
  retained; a failed switch is rolled back automatically.
  - The manifest, recovery configuration, receipt, and any existing installation
    must agree on product, installation token, and exact licensed domain before
    Docker or storage is changed.
  - Fresh-host restore uses `/var/telebugs`, archived recovery secrets, archived
    registry identity, and the captured image digest. Registry access is still
    required if that exact image is not available locally.
  - A completed replacement restore is failed back by returning DNS to the
    retained previous server. If the replacement accepted activity that must be
    kept, create a fresh backup there and restore it onto the previous server
    before moving DNS. Telebugs does not merge two installations.
  - Restore sends only sanitized, best-effort lifecycle status with a fixed
    failure stage and rollback outcome. Telemetry failure never changes restore.
  - A captured image that predates `/ready` may fall back to `/up`; the CLI
    prints a warning instead of silently weakening the check.
  - `--yes` skips the replacement prompt. Use it only when automation has
    independently confirmed the target installation.

See [Backup and Restore](operations-01-backup-and-restore.md) before relying on
an archive.

## Manage versions (previews, pins, and rollbacks)

- `update` — Update Telebugs to the latest version (or a specific tag with `--tag` / `-t`).
  - Use `telebugs update --tag rest-api-preview-20250610-abc1234` to try a private preview build on your instance.
  - The previous running image is tagged locally as `:previous` for safety.
  - Updates do not automatically create a data backup. The command warns before
    changing the application image.
- `rollback` — Roll back to the image that was running before the last update (uses the local `:previous` tag).
  - Image rollback does not reverse database migrations or restore data.

## Additional commands

- `help` — Displays help information for the `telebugs` command.
- `setup` — Runs the initial setup process for a new Telebugs installation. Do
  not use it to prepare a replacement server for `data restore`.
- `start` — Start Telebugs.
- `stop` — Stop Telebugs.
- `status` — Checks the container, `/up`, `/ready`, local databases, storage,
  migrations, critical workers, queue latency, and notification failure warning.
  - `--json` prints the detailed local result for scripts.

## Flags

- `-h`, `--help` — Displays help information for the `telebugs` command.

Use `telebugs [command] --help` to see detailed help for a specific command.
