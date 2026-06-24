# System Requirements

Telebugs can run on almost any hardware. This includes a VPS, cloud server, home server, or even a Raspberry Pi. It supports both AMD64 (also known as x86-64, x64, x86_64, and Intel 64) and ARM64 (also known as AArch64) architectures. In short, if Docker runs on it, Telebugs will too.

## Supported Platforms

Telebugs works with over 100 programming languages and frameworks through Sentry SDKs. Popular options include JavaScript (Node.js, React, Angular), Python (Django, Flask), Ruby (Rails), Java (Spring), PHP (Laravel), .NET (ASP.NET Core), and Go. For the full list, see Supported Platforms in the appendix.

## Error Throughput

Use this table to estimate what your server can handle.

| CPU cores | Est. max errors/second | Est. max errors/day |
| --------- | ---------------------- | ------------------- |
| 2         | 30                     | 2,592,000           |
| 4         | 60                     | 5,184,000           |
| 8         | 120                    | 10,368,000          |
| 16        | 240                    | 20,736,000          |

These numbers are rough estimates. Actual throughput depends on CPU, RAM, application complexity, and error volume. Throughput is shared across all projects in one Telebugs installation. With two projects, each gets about half. With four projects, each gets about a quarter, and so on.

## Recommended Minimum Specs

- **RAM:** 1 GB
- **Disk space:** 40 GB
- **CPU:** 1 core

## Recommended Specs for Small to Medium Projects

- **RAM:** 4 GB
- **Disk space:** 80 GB
- **CPU:** 3 cores

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
