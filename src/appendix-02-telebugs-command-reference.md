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

- `data` — Manage application data.

## Manage versions (previews, pins, and rollbacks)

- `update` — Update Telebugs to the latest version (or a specific tag with `--tag` / `-t`).
  - Use `telebugs update --tag rest-api-preview-20250610-abc1234` to try a private preview build on your instance.
  - The previous running image is tagged locally as `:previous` for safety.
- `rollback` — Roll back to the image that was running before the last update (uses the local `:previous` tag).

## Additional commands

- `help` — Displays help information for the `telebugs` command.
- `setup` — Runs the initial setup process for Telebugs.
- `start` — Start Telebugs.
- `stop` — Stop Telebugs.
- `status` — Displays the current status of the Telebugs instance.
- `update` — Update Telebugs to the latest version.

## Flags

- `-h`, `--help` — Displays help information for the `telebugs` command.

Use `telebugs [command] --help` to see detailed help for a specific command.
