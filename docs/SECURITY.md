# Security decisions and outstanding risk

## Stage 2 - 2026-10-28
- Official Python 3.14 slim trixie base pinned by manifest digest in Dockerfile.
- App runs as UID/GID 10001; code and dependencies remain owned by root.
- No credentials, Git metadata or development tools copied into the build context.
- Runtime verified with read-only root filesystem, /tmp tmpfs, all capabilities dropped,
  no-new-privileges, memory/CPU/PID limits and localhost-only published port.
- Production WSGI serving; debug mode disabled; JSON errors hide internal details from clients.
- These checks are local evidence, not an AWS deployment or proof against every exploit.

## Vulnerability review
Trivy 0.76.1 (official image pinned in .trivy-image) scanned the exported image.
Before remediation: 49 HIGH findings, including five fixable HIGH entries in
pip-vendored msgpack, setuptools and urllib3. Removed pip after dependency installation.
After remediation: 0 CRITICAL, 44 HIGH, 58 MEDIUM, 61 LOW, 1 UNKNOWN;
no fixable HIGH/CRITICAL entries and no Python dependency vulnerability entries reported.

Remaining findings affect Debian base packages including ncurses, util-linux, systemd
libraries, libacl and perl. The report lists no FixedVersion for these entries.
Some involve command-line/system facilities not directly used by the two Flask routes,
but exploit reachability has NOT been fully assessed. Non-root execution, dropped
capabilities, read-only runtime and short-lived local execution reduce exposure;
they do not resolve CVEs. No blanket suppression or claim of a clean image.

Disposition: retained and documented for this local learning checkpoint. Review updated
base packages and rescan before cloud rollout. Any cloud approval must disclose remaining
HIGH findings, temporary exposure and cleanup window. This is not production readiness.

Full findings: evidence/test-results/02-trivy.json.
Before/after: 02-scan-before.txt and 02-scan-summary.txt in that directory.
Gate: fail on HIGH/CRITICAL with an available fix. The complete report remains visible
including findings without fixes; reassess this policy before production use.

## Sources
- https://hub.docker.com/_/python
- https://www.trivy.dev/docs/latest/getting-started/installation/
- https://github.com/aquasecurity/trivy/blob/main/docs/guide/target/container_image.md
