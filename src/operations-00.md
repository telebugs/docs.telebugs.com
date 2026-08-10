# Operations

Telebugs is designed for one server and one operator-friendly command. Its
operational contract is deliberately modest:

- a backup is complete, internally verified, and restorable with the captured
  application version;
- `/up` answers whether the web application is alive;
- `/ready` answers whether the instance can accept and process errors and run
  notification work;
- `telebugs status` explains readiness locally without publishing diagnostic
  details on the internet; and
- admins see permanently failed notification deliveries in Telebugs and can use
  the existing jobs page to review them.

This is not a monitoring platform. The host still needs normal server backups,
disk and memory monitoring, certificate and DNS ownership, network monitoring,
and a place outside the server to store Telebugs archives.

Start with [Backup and Restore](operations-01-backup-and-restore.md), then add an
external check for [liveness or readiness](operations-02-health-and-status.md).
If an admin banner reports a delivery failure, follow the
[notification failure guide](operations-03-notification-delivery-failures.md).
