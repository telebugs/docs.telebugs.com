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
maps, locally stored TLS state, and notification configuration stored by
Telebugs, including destination URLs and encrypted credentials. The archive
separately contains the CLI recovery configuration, including application
encryption keys and secrets. It does not back up the host operating system,
firewall, DNS, Docker installation, external mail, push, or webhook services,
the container image itself, or Docker logs. The manifest records the immutable
image digest; restoration still needs that image locally or available from the
Telebugs registry.

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

Current backups use format 2 and contain a version-2 license receipt bound to the
exact installation token and licensed domain. The CLI verifies that receipt
locally, so archive verification and restore authorization work without
`auth.telebugs.com`. Retrieving the captured container image can still require
registry access.

Format-1 manifest backups use the retired receipt format. The current CLI
contacts `auth.telebugs.com` during `data verify` or `data restore`.
Authorization succeeds only when the archived token is activated for the exact
archived domain. Auth returns a replacement receipt without changing the
licensed domain. Verification remains read-only: it does not rewrite the archive
or save the replacement receipt, so another verification or restore must
authorize again. A successful format-1 restore saves the replacement receipt in
the restored local configuration; the next backup is format 2 and can validate
it offline. If auth is unavailable, the command exits with an actionable error
before it installs Docker, creates restore directories, pulls an image, stops a
container, or changes storage. An invalid format-2 receipt is treated as
tampering and is never reissued.

Archives created by the old, pre-manifest backup command are rejected because
they do not contain enough evidence for the CLI to promise a safe restore.
Unsupported future archive formats are also rejected before the installation is
changed. Use the current Telebugs CLI for restoration; it pairs the stored data
with the captured application image so database migrations are not guessed.

## Restore

On a fresh replacement server, install the current recovery CLI:

```bash
bash -c "$(curl -fsSL https://auth.telebugs.com/restore)"
```

This public bootstrap detects Linux or macOS on x86_64 or arm64, downloads the
matching CLI through a short-lived URL, verifies its SHA-256 sidecar, and
atomically installs `/usr/local/bin/telebugs`. It does **not** receive or upload
your backup, install Docker, run setup, create Telebugs configuration, start a
container, or begin restoration. Possession of the CLI does not provide
registry access or authorize another domain. On Linux, restore installs Docker
when it is missing. On macOS, install and start Docker before running restore.

> **Do not run normal `telebugs setup` on a replacement server.** Setup is for
> a new installation. Restore derives the domain, registry identity, secrets,
> image digest, and recovery configuration from the archive.

Transfer the archive to the server. Before changing anything, verify it:

```bash
telebugs data verify /backups/telebugs-production.tar.gz
```

Then restore:

```bash
sudo telebugs data restore /backups/telebugs-production.tar.gz
```

On an existing installation, the CLI asks before replacing data. Automation can
use `--yes` only after independently confirming the target:

```bash
sudo telebugs data restore /backups/telebugs-production.tar.gz --yes
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

There is no restore domain argument or domain-change flag. The archive manifest,
recovery configuration, and signed receipt must agree on the exact licensed
domain and installation token before any host mutation. For an existing
installation, its product, token, and domain must agree too. Auth never changes
the licensed domain during legacy authorization.

Current host-specific values such as the storage path, registry identity, and
update schedule stay with an existing matching host; the archived application
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

Fetching the public recovery CLI sends best-effort download telemetry through
Telebugs auth to Telesink. A bootstrap request contains the request IP observed
by auth. A binary request also contains the selected operating system and
architecture. These public download events contain no license token, backup
identity, archive name, or path.

Restore sends best-effort lifecycle events to Telebugs auth: `started`,
`completed`, or `failed`; fresh or replacement target; backup format; a random
correlation ID; and, on failure, a fixed stage and rollback outcome. The request
uses the archived token and domain for authorization, but auth constructs the
customer email, licensed domain, and observed request IP from server-side state
before forwarding the event to Telesink. Paths, archive names, error messages,
secrets, tokens, database details, and notification destinations are not
included. Telemetry has a short timeout and no retries. An auth or Telesink
outage never changes verification, restoration, rollback, or the command exit
status.

## Bring a Replacement Server Online

A successful restore proves the container and local dependencies are ready when
the captured image provides `/ready`. For an older image, the documented `/up`
fallback proves only that the web process responds. Neither result proves that
public DNS reaches this server or that public TLS works. Before changing DNS,
test inside the container:

```bash
docker exec telebugs curl -fsS http://127.0.0.1:3000/up
docker exec telebugs curl -fsS http://127.0.0.1:3000/ready
```

Captured images from before `/ready` will return `404` for the second command;
the CLI reports its documented `/up` compatibility warning during restore.

Prepare the network cutover:

1. Allow inbound TCP ports `80` and `443` in the host firewall and cloud
   firewall.
2. Create a direct DNS `A` record for the archived licensed domain pointing to
   the replacement IPv4 address. Update or remove `AAAA` records as appropriate.
   Do not enable a CDN or DNS proxy; Telebugs terminates TLS itself.
3. Before waiting on resolver caches, test direct HTTP routing from another
   machine:

   ```bash
   curl -I --resolve errors.example.com:80:REPLACEMENT_IP \
     http://errors.example.com/up
   ```

   A redirect to `https://errors.example.com/up` proves port 80 reaches the
   replacement server's HTTP listener. Substitute the actual archived domain.
4. Change DNS, then compare a public resolver with the replacement server:

   ```bash
   dig +short A errors.example.com @1.1.1.1
   curl -4 https://api.ipify.org
   ```

5. After DNS resolves to the replacement IP, verify public TLS and both health
   endpoints:

   ```bash
   curl -fsS https://errors.example.com/up
   curl -fsS https://errors.example.com/ready
   ```

TLS issuance or renewal can time out while DNS still points elsewhere, a proxy
intercepts the challenge, or ports 80/443 are blocked. Keep direct DNS and both
ports available for automatic renewal. A `200` from the container alone does
not disprove a DNS, firewall, routing, or TLS problem—the completed field drill
demonstrated this distinction.

Keep the old same-domain server isolated during the documented rollback window.
Only one instance may serve production traffic. If cutover fails, point DNS back
to the old IP. For an in-place restore, use the retained pre-restore paths shown
by the CLI and investigate before deleting either copy.

## Fail Back to the Previous Server

Once a replacement restore has completed, it cannot be cancelled. Returning to
the previous server is a **failback**. If you retained both servers, first decide
whether the replacement accepted any errors, account changes, attachments, or
background work that you need to keep. Telebugs does not merge two SQLite data
sets.

If the replacement has no important new activity, do not restore the old backup
again. The previous server already contains its pre-cutover state:

1. Keep the previous server out of public DNS. Start it and verify it directly:

   ```bash
   telebugs start
   telebugs status
   curl -fsS --resolve errors.example.com:443:PREVIOUS_IP \
     https://errors.example.com/up
   ```

   Substitute the licensed domain and previous server IP. A captured image that
   predates `/ready` may only provide `/up`.
2. Stop Telebugs on the replacement server. This creates a brief maintenance
   window but prevents two copies from accepting different production data or
   delivering the same queued notifications:

   ```bash
   telebugs stop
   ```

3. Change the direct DNS `A` record back to `PREVIOUS_IP`. Update or remove
   `AAAA` records as appropriate and keep CDN or DNS proxying disabled.
4. Confirm that public DNS and TLS now reach the previous server:

   ```bash
   dig +short A errors.example.com @1.1.1.1
   curl -fsS https://errors.example.com/up
   curl -fsS https://errors.example.com/ready
   ```

   Omit `/ready` only for an older image that has the documented `/up`
   compatibility behavior.

If the replacement accepted activity that must survive failback, carry its
latest state back instead of restarting the stale copy:

1. On the replacement, create a fresh backup and stop Telebugs as soon as the
   command finishes. Backup restarts an instance that was running, so the
   explicit stop closes the snapshot window:

   ```bash
   telebugs data backup /root/telebugs-failback.tar.gz
   telebugs stop
   ```

   Activity accepted after the backup snapshot is not in the archive. Use a
   maintenance window or host-level ingress controls when that gap matters.
2. Transfer the archive to the previous server, then verify and restore it there:

   ```bash
   telebugs data verify /root/telebugs-failback.tar.gz
   telebugs data restore /root/telebugs-failback.tar.gz
   telebugs status
   ```

   The token and licensed domain must match before the previous installation is
   changed. Restore retains the previous server's pre-restore storage and
   configuration and uses the normal automatic rollback if readiness fails.
3. Test the previous server with `curl --resolve`, change DNS back, and run the
   public DNS and TLS checks above.

The queue database is part of every backup. Pending or retrying jobs can run
after failback, so email, push, and webhook delivery remains at least once. Never
leave both servers serving production traffic to hide DNS propagation: their
databases will diverge. Resolver caches may continue sending some clients to the
stopped replacement until the DNS TTL expires. For a planned migration, lower
the TTL in advance. Retain the replacement and both backup generations until
the rollback window closes, then remove the retired copy securely.

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

1. Start with a fresh host containing neither the CLI nor Docker.
2. Install the CLI with `bash -c "$(curl -fsSL https://auth.telebugs.com/restore)"`.
   Confirm that it created no Telebugs configuration or container.
3. Copy the newest off-server archive to the drill host.
4. Run `telebugs data verify`.
5. Restore it with the CLI without entering or overriding a domain.
6. Run `telebugs status` and require liveness and readiness to pass.
7. Prove that changing the archived domain or restoring over a differently
   licensed installation is rejected before mutation.
8. Keep public DNS on production during an isolated drill. For a real migration,
   follow the direct-DNS, ports 80/443, TLS, and public endpoint checks above.
9. Sign in, open recent errors, and download or inspect representative
   attachments and source maps.
10. Replace notification destinations with drill-safe endpoints and allow only
   the required test egress.
11. Send a controlled test error, confirm it is processed, and test the
   notification channels you depend on.
12. Record the archive date, restore duration, Telebugs version, and result, then
   destroy the drill host securely.

The license permits temporary same-domain overlap solely for an isolated restore
drill, migration, and rollback. The temporary copy must not become an additional
production instance, and only one endpoint may serve production traffic.

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
