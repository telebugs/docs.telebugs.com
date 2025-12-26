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
