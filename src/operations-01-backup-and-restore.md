# Backup and Restore

The `telebugs` command creates a single verified archive for persistent
Telebugs data and recovery configuration. The archive contains sensitive
recovery secrets, so treat it like production credentials as well as production
data.

## Create a Backup

Connect to the Telebugs server and run:

```bash
telebugs data backup
```

The default filename is timestamped in UTC, for example
`telebugs-backup-20260809T120000Z.tar.gz`. To choose a path:

```bash
telebugs data backup /mnt/offsite/telebugs-production
```

The `.tar.gz` suffix is added when omitted. The destination must be outside the
Telebugs storage directory, its parent directory must already exist, and it must
have enough free space. An existing file is never overwritten. If the configured
storage path contains a symbolic link, the CLI follows it when measuring,
validating, and archiving data; the destination must also be outside the resolved
storage tree.

When Telebugs is running, the command stops it for the duration of validation,
archiving, and archive verification so the three SQLite databases and stored
files come from one quiet point in time. It restarts the captured application
image afterward and waits for readiness. If Telebugs was already stopped, it
remains stopped. Backup time grows with stored data, file count, disk speed, and
the destination, so use a maintenance window for a large installation.

If a backup is interrupted, do not rely on a partial archive. A normal interrupt
cancels file inventory, archiving, or verification, removes the unpublished
partial file, and attempts to restart a previously running instance. Confirm
with `telebugs status`, and run `telebugs start` if the process or host was
terminated before recovery completed. A published archive is still usable only
after `telebugs data verify` succeeds.

## What a Successful Backup Means

The command reports success only after all of these steps finish:

1. The primary, cache, and queue SQLite databases exist and pass
   `PRAGMA quick_check`.
2. Every Active Storage database record has a stored file of the expected size
   and database checksum.
3. All persistent storage is inventoried with its size, mode, and SHA-256 hash.
4. The manifest records database schema versions and the exact immutable
   Telebugs image digest, and the recovery configuration must identify the same
   image.
5. The recovery configuration, encryption keys, and application secret are in
   the archive, and the manifest records their configuration file's SHA-256
   checksum.
6. The compressed archive is closed, synced, verified against its manifest,
   and atomically published with mode `0600`.
7. A previously running instance restarts and passes `/ready`. If the captured
   image predates the readiness endpoint, the CLI accepts `/up` instead and
   prints a legacy-compatibility warning.

The persistent-storage portion covers the SQLite databases, attachments, source
maps, and locally stored TLS state. The archive separately contains the CLI
recovery configuration, including application encryption keys and secrets. It
does not back up the host operating system, firewall, DNS, Docker installation,
external mail service, external webhook destinations, the container image
itself, or Docker logs. The manifest records the immutable image digest;
restoration still needs that image locally or available from the Telebugs
registry.

Restoring on a replacement server also requires registry access when the exact
image is not already present. If the credentials archived with an older backup
no longer have access, provide current credentials to the restore process with
`TELEBUGS_REGISTRY_USERNAME` and `TELEBUGS_REGISTRY_PASSWORD`; `TELEBUGS_TOKEN`
can be used instead of the password override. These overrides are read from the
environment and are not written into the restored Telebugs configuration.
If the captured image cannot be retrieved, the CLI reports Docker's reason and
exits before staging data or changing the current installation. Keep the
archive, correct registry access or make the captured digest available locally,
and run restore again.

Copy every successful archive to storage outside the Telebugs server. Preserve
its restrictive permissions and encrypt the backup destination. A backup left
on the same disk is not disaster recovery.

## Verify an Archive

Verification is read-only:

```bash
telebugs data verify /backups/telebugs-production.tar.gz
```

It checks the archive format and required creation timestamp, recovery
configuration checksum, every file hash, file size and mode, and the complete
inventory. Use it after copying an archive to remote storage and before every
restore.

Verification detects corruption and incomplete archives; it is not an external
digital signature. Keep archives in access-controlled, tamper-resistant storage
as well as encrypting them.

Archives created by the old, pre-manifest backup command are rejected. They do
not contain enough evidence for the CLI to promise a safe restore.
Unsupported future archive formats are also rejected before the installation is
changed. Use the current Telebugs CLI for restoration; it pairs the stored data
with the captured application image so database migrations are not guessed.

## Restore

Make the current `telebugs` CLI available on the replacement server, transfer
the archive, and run:

```bash
telebugs data restore /backups/telebugs-production.tar.gz
```

On an existing installation, the CLI asks before replacing data. Automation can
use `--yes` only after independently confirming the target:

```bash
telebugs data restore /backups/telebugs-production.tar.gz --yes
```

The restore verifies the complete archive before changing the installation. It
then retrieves the exact captured image by immutable digest, extracts into a
staging directory, runs the database and file checks again, and only then stops
the current instance and switches storage.

The queue database is restored with the rest of the data. Pending or retrying
jobs, including notification deliveries, can run as soon as the restored
container starts. The CLI prints a warning before the switch. This preserves
work during real disaster recovery, but it also means notification delivery is
at least once across recovery and an old delivery may be repeated.

For an existing installation, the product and domain must match. Current
host-specific values such as the storage path, installation token, registry
identity, and update schedule stay with the host; the archived application
secrets and data are restored together. On a fresh host, Telebugs uses its
standard `/var/telebugs` storage location. If the configured storage path is a
symbolic link, restore stages and switches data on the target filesystem while
leaving the configured link and Docker binding unchanged.

Restore retains the previous storage by atomically renaming directories. The
resolved Telebugs storage path must therefore be a directory *inside* its
filesystem, not the filesystem's mount point. For a dedicated data disk, mount
the disk at a parent such as `/mnt/telebugs-data`, create
`/mnt/telebugs-data/telebugs`, and point the configured storage path (normally
`/var/telebugs`) at that child directory. A symbolic link is supported. The CLI
tests this layout before downloading an image, staging data, or stopping
Telebugs.

## What a Successful Restore Means

A restore is successful when:

- the manifest, recovery configuration, and every archived file verify;
- all three SQLite databases pass integrity checks;
- every Active Storage blob exists at the expected size and database checksum;
- the exact captured Telebugs image is available;
- restored storage has the ownership expected by the container;
- restored files and directories are synced to disk before the storage switch;
- the restored container starts and `/ready` returns `200`; for a captured image
  that predates `/ready`, `/up` returns `200` and the CLI prints a
  legacy-compatibility warning; and
- on an existing installation, the CLI reports where it retained the
  pre-restore storage and configuration.

If any step after the switch fails on an existing installation, the CLI
automatically puts back the previous storage and configuration and restarts the
previous image when it was running. On a fresh host, it removes the partial
installation and preserves the failed restored storage for diagnosis. Do not
delete retained pre-restore or failed restore data until you understand the
failure. If stopping or removing the current container fails before the file
switch, the CLI makes a bounded attempt to return a previously running container
to service and leaves storage unchanged.

Image rollback and data restore are different. `telebugs rollback` switches to
the image saved before the last update; it does not reverse migrations or
restore data. `telebugs update` warns about this and does not create a backup
automatically. Create an explicit restore point before an update when the change
window requires one:

```bash
telebugs data backup /backups/pre-update
telebugs update
```

## Run a Restore Drill

Use a disposable server or isolated VM, never the production storage path.
Before restoring, prevent the drill host from reaching production email, push,
and webhook destinations. The restored queue can start delivery immediately;
network isolation or outbound firewall rules provide the boundary before you
can sign in and replace destinations with drill-safe configuration.

1. Copy the newest off-server archive to the drill host.
2. Run `telebugs data verify`.
3. Restore it with the CLI.
4. Run `telebugs status` and require liveness and readiness to pass.
5. Sign in, open recent errors, and download or inspect representative
   attachments and source maps.
6. Replace notification destinations with drill-safe endpoints and allow only
   the required test egress.
7. Send a controlled test error, confirm it is processed, and test the
   notification channels you depend on.
8. Record the archive date, restore duration, Telebugs version, and result, then
   destroy the drill host securely.

If restore printed the legacy `/up` warning, update the drill instance to a
Telebugs release with readiness diagnostics and require `telebugs status` to
pass before declaring the drill complete.

Run a drill before relying on the first backup, after a material storage or
deployment change, and periodically according to your recovery objective.

Telebugs' automated tests cover archive corruption, unsafe archive paths,
missing files, configuration integrity, legacy archive rejection, cancellation,
staging, pre-switch container recovery, and filesystem rollback primitives. They
do not replace a host-level drill that proves Docker switching and restart,
registry access, remote backup retrieval, DNS, TLS, and operator access.
