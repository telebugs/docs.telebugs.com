# `telebugs` command reference

Install and manage your Telebugs instance.

To run the `telebugs` command, connect to your server using SSH or your cloud
provider’s web-based terminal.

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
- `data restore <filename>` — Verify and stage a backup, then restore it with the
  captured immutable application image. Existing storage and configuration are
  retained; a failed switch is rolled back automatically.
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
- `setup` — Runs the initial setup process for Telebugs.
- `start` — Start Telebugs.
- `stop` — Stop Telebugs.
- `status` — Checks the container, `/up`, `/ready`, local databases, storage,
  migrations, critical workers, queue latency, and notification failure warning.
  - `--json` prints the detailed local result for scripts.

## Flags

- `-h`, `--help` — Displays help information for the `telebugs` command.

Use `telebugs [command] --help` to see detailed help for a specific command.
