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

## 2026-10-29 AWS access audit

SSO profile tobi-admin/session tobi-sso is configured for AdministratorAccess;
current STS call succeeds. This broad role is existing bootstrap access, not least privilege
for application tasks or GitHub Actions. No IAM settings changed in the audit.
Root/admin MFA are user-reported; independent evidence pending.
Workload region is eu-north-1; Identity Center is in us-east-1.
Future OIDC trust and execution/task policies require explicit approval before application.

Historical scan linkage verified: Trivy ImageID matches Docker archive configuration digest;
ordered filesystem layers match current image. Docker inspect's manifest identity differs,
so direct string comparison alone is insufficient. Findings remain historical October 28 data.
Do not treat a fixable-only gate as an all-findings pass or suppress unpatched HIGH entries.
Refresh before cloud rollout and document the risk decision.

Terraform state, plans and provider/CLI caches must be excluded from Git before use.
Commit reproducibility lockfiles as appropriate, never credentials or secret variable values.

## 2026-10-29 Terraform proposal and refreshed image review

No IAM changes applied. Proposed execution role scoped to this ECR/log group; task role
has no policies; optional OIDC role trusts only this repository's main branch and AWS audience.
No static AWS keys or credential files. RegisterTaskDefinition wildcard resource is unavoidable
for that API and region-limited; other resource/PassRole permissions scoped. Review trust and
workflow dispatch gates together before enabling; no Environment-based claim currently used.

State/plans/tooling/tfvars excluded from Git; provider lock committed. Local state requires
secure backup. Raw plans can contain account IDs and are not shareable evidence.
ECS service-linked role is absent and may be auto-created by initial ECS use; include it in
approval and do not delete if shared.

Fargate volume ownership seeded from Dockerfile VOLUME /app/runtime and checked locally.
Read-only root and dropped capabilities configured; local no-new-privileges/tmpfs do not
translate to Fargate. No production-ready or identical-hardening claim.

Fresh scan dated October 29 retains 44 HIGH/58 MEDIUM/61 LOW/1 UNKNOWN, no CRITICAL or
fixable HIGH/CRITICAL findings. Full report preserved; risk not resolved. Operator /32 only,
temporary access, no sensitive payload and explicit risk acknowledgment required before rollout.
