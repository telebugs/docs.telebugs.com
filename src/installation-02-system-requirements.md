# System Requirements

Telebugs can run on almost any hardware. This includes a VPS, cloud server, home server, or even a Raspberry Pi. It supports both AMD64 (also known as x86-64, x64, x86_64, and Intel 64) and ARM64 (also known as AArch64) architectures. In short, if Docker runs on it, Telebugs will too.

## Supported Platforms

Telebugs works with over 100 programming languages and frameworks through Sentry SDKs. Popular options include JavaScript (Node.js, React, Angular), Python (Django, Flask), Ruby (Rails), Java (Spring), PHP (Laravel), .NET (ASP.NET Core), and Go. For the full list, see Supported Platforms in the appendix.

## Error Throughput

Use this table to estimate sustained, fully processed error reports. These
numbers are about reports that have made it through the ingest queue and are
visible in Telebugs, not just HTTP requests accepted by the ingest endpoint.

| Server | Sustained processed reports/second | Sustained processed reports/day |
| ------ | ---------------------------------- | -------------------------------- |
| 2 vCPU / 4 GB RAM | ~50 | ~4,320,000 |
| 4 vCPU / 8 GB RAM | ~100 | ~8,640,000 |
| 8 vCPU / 16 GB RAM | ~200 | ~17,280,000 |
| 16 vCPU / 32 GB RAM | ~400 | ~34,560,000 |

The 2 vCPU / 4 GB RAM row is based on 10-minute benchmarks on a Hetzner CX23
VPS with local disk. In those tests, Telebugs processed about 50 reports per
second end-to-end under ingest-only and mixed ingest/UI workloads. The ingest
endpoint also accepted short bursts above 160 errors per second, with queued
reports draining afterward.

Larger rows are planning estimates. Actual throughput depends on CPU, RAM, disk
speed, application payload size, retention settings, notifications, and how much
UI traffic the same server is handling. Throughput is shared across all projects
in one Telebugs installation. With two busy projects, each gets about half. With
four busy projects, each gets about a quarter, and so on.

## Benchmark Methodology

Telebugs includes a source-level benchmark harness at `bin/load`. This is not
part of the customer-facing `telebugs` CLI. It is meant for repeatable release
and sizing benchmarks.

The benchmark starts an isolated Dockerized Telebugs instance in the
`performance` environment, creates a throwaway project token, runs k6 against
the Sentry envelope endpoint, waits for the ingest queue to drain, and prints
both intake and processing rates.

For the 2 vCPU / 4 GB RAM baseline above, we ran these 10-minute tests on a
Hetzner CX23 VPS:

```bash
bin/load --users 100 --duration 10m --read-ratio 0 --groups 200 --drain-timeout 3600
bin/load --users 100 --duration 10m --read-ratio 10 --groups 200 --drain-timeout 3600
bin/load --users 100 --duration 10m --read-ratio 20 --groups 200 --drain-timeout 3600
```

The important result fields are:

- **Envelope accept rate:** how quickly the ingest endpoint accepted incoming
  reports during the k6 run. This is the burst intake rate.
- **Reports processed end-to-end:** how many reports per second were fully
  processed after including any queue drain time. This is the sustained sizing
  number used in the table.
- **HTTP p95 latency:** the 95th percentile response time during the load test.
- **HTTP failures and failed jobs:** both should stay near zero for a healthy
  run.
- **Peak pending ingest payloads:** how much backlog accumulated while Telebugs
  absorbed the burst.

For capacity planning, prefer `Reports processed end-to-end`. A high
`Envelope accept rate` with a large pending queue means Telebugs absorbed the
burst successfully, but the server would need more CPU, faster disk, or a lower
incoming error rate to sustain that load indefinitely.

Telebugs also includes **Ingest Protection** under **Settings** > **Instance**.
It defaults to 3,000 accepted errors per minute, which matches the 50 errors per
second sustained baseline for a small 2 vCPU / 4 GB RAM server. If an error
storm exceeds the configured limit, Telebugs returns `429 Too Many Requests`
before writing to the ingest queue.

## Recommended Minimum Specs

- **RAM:** 1 GB
- **Disk space:** 40 GB
- **CPU:** 1 core

## Recommended Specs for Small to Medium Projects

- **RAM:** 4 GB
- **Disk space:** 40-80 GB
- **CPU:** 2 cores

## Operating System Compatibility

- Tested on Linux (Ubuntu, Debian, Alpine, Rocky) and any OS that supports Docker.
- Also works on macOS.

**Rocky Linux 9 note:** Rocky works well once Docker is installed, but the
Telebugs installer may not be able to install Docker automatically there. If you
see a message that Docker installation is not supported on this platform,
install Docker first, then run your Telebugs installation command again:

```bash
sudo dnf config-manager --add-repo https://download.docker.com/linux/rhel/docker-ce.repo
sudo dnf -y install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo systemctl --now enable docker
sudo usermod -a -G docker YOUR_USER
```

Replace `YOUR_USER` with the Linux user that will run Telebugs. Log out and back
in, or run `newgrp docker`, so the new group membership is active. If automatic
updates complain that `cron` is not installed, install or enable Rocky's
`cronie` package; if needed, add a daily `telebugs update` job manually with
`crontab -e`.

See the [Rocky Linux Docker guide][1] for the latest Docker installation
details.

[1]: https://docs.rockylinux.org/gemstones/containers/docker/
