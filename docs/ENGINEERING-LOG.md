# Engineering log

## 2026-10-28 - Stage 0 preflight
Inspected WSL Ubuntu and the two guide-specified paths read-only. The personal project was absent; the accidental Webforx project directory was empty. Left the latter untouched. Created only the personal project baseline.

Tool checks: Git 2.53.0, Python 3.14.4, venv support, gh 2.46.0. GitHub authentication absent; Docker unavailable in Ubuntu; AWS CLI missing.

Decision: keep Stage 0 narrow. No dependency selection, system installation or cloud provisioning. Workspace identity must be checked before mutation; installed CLI presence does not establish authentication.

Next: resolve GitHub authentication, repository authorization, screenshot evidence and empty-directory confirmation.

Configured repository-local Git identity from the user's supplied name/email. Reviewed the staged baseline and passed git diff --cached --check. Created baseline commit ae4dec5; working tree was clean immediately afterward. No remote configured; push remains incomplete.

GitHub authentication verified as TobiOnline over SSH. The intended repository TobiOnline/aws-ecs-secure-deployment was not found. Local main is clean and has no remote. Ready for private repository creation approval, then origin setup and push.

With explicit approval, created private TobiOnline/aws-ecs-secure-deployment. SSH authentication failed; changed this repository's origin to HTTPS and pushed using the existing GitHub CLI credential helper without exposing credentials. Verified local and remote main both at 344d706. No AWS resources created. Screenshot and empty-directory confirmation remain pending.

User approved cleanup. Immediate read-only recheck found the accidental Webforx project directory already absent; verified absence without deleting anything. User requests grouped questions/permissions and a same-day completion target. Stage 0 remains partial only for screenshot evidence.

Accepted the user's terminal screenshot and copied the original PNG to evidence/screenshots/00-personal-workspace-and-git.png. Verified readable personal workspace path, clean main tracking origin/main and matching commit 42d59c2. No credentials visible. VS Code's window title says Webforx, while the terminal proves the intended personal path. Stage 0 acceptance items now addressed; Stage 1 is next.

## 2026-10-28 - Stage 1 application
Checked official PyPI metadata against Python 3.14.4; installed Flask 3.1.3, Gunicorn 26.2.0 and pytest 9.2.0 in isolated .venv and pinned runtime/dev transitive versions. Implemented app factory, JSON endpoints and HTTP/server error handling. Six tests cover happy paths, 404, 405 with Allow header preserved, and generic 500 responses. pip check passed. Live localhost Gunicorn checks validated 200/200/404 and server was stopped. Evidence saved under evidence/test-results/01-*. Screenshot pending. Lesson: unit tests verify behavior; a live WSGI check also validates server startup and request handling. Docker integration remains the next environment blocker.

Stage 1 screenshot received, inspected and saved. Docker Desktop integration verified in Ubuntu (29.6.2; Linux x86_64). User requests plain-language current-stage explanations and practical next outcomes.

## 2026-10-28 - Stage 2 container
Built official digest-pinned Python slim image with UID/GID 10001, minimal allowlisted context,
pinned runtime dependencies, Gunicorn, stdout/stderr logs and HTTP health check. Single stage
is sufficient: wheels require no compiler; removed pip after install to reduce runtime tooling.
Container Python is 3.14.10; host is 3.14.4.

Restricted runtime checks passed: read-only root filesystem, dropped capabilities, no-new-privileges,
localhost-only port, health and both HTTP endpoints. Temporary containers removed.
Initial Trivy scan found five fixable HIGH entries in pip-vendored packages; removed pip,
rebuilt and rescanned. Final counts: 0 CRITICAL, 44 HIGH, 58 MEDIUM, 61 LOW, 1 UNKNOWN.
No fixable HIGH/CRITICAL remain; unpatched Debian findings retained and documented without suppression.
Full reachability not assessed; do not claim vulnerability-free or production-ready.
Application tests still pass (six). Saved build, runtime and scan evidence.
Image ID and observed size are in 02-runtime.txt; screenshot pending.

Next: capture Stage 2 screenshot, verify AWS access and prepare cost/resource approval.

Stage 2 screenshot received and inspected; restricted runtime and severity summary visible. Saved evidence and marked Stage 2 complete with residual-risk documentation. User is new to AWS and reports possible USD 100 credits; credit balance/expiry/plan are not yet verified. Prioritize conserving credit and checking billing before resource creation.

## 2026-10-29 - AWS account setup handoff and repository audit

This entry records AWS environment setup separately from the completed local implementation.
Previous entries remain historical facts at their recorded dates.

User-reported setup: account TOBI, paid plan, USD 100 promotional credits initially available,
root MFA enabled and administrator MFA enabled. These are handoff statements, not independent
console verification; current credit balance/expiry, MFA screenshots and plan evidence are missing.

Verified now: AWS CLI v2.39.1 installed in Ubuntu; profile tobi-admin uses SSO session tobi-sso;
default workload region eu-north-1; Identity Center region us-east-1; configured role
AdministratorAccess. STS identity request succeeded without saving identifiers or credentials.
This confirms current CLI access, not the MFA enforcement or least privilege of that role.
Identity Center/SSO configuration is present; no Identity Center settings were changed.

Access troubleshooting: the handoff says setup/troubleshooting is complete, but does not provide
the original AWS error or remediation sequence. Do not invent it. Current SSO and inventory
calls succeed; no login/session blocker observed. Earlier Git SSH trouble remains a separate
historical Git issue. A recursive file inventory hit permission denied in the ignored
scanner-owned .cache/trivy/fanal directory; no permissions changed, and tracked-file inspection
completed without traversing that cache.

Billing protection: one Zero-named COST budget found with USD 1.00 budget amount and one
notification rule. User calls this Zero Spend Budget. The name alone is not a zero-dollar
spending limit; exact threshold, recipient delivery and treatment of credits are not verified.
A budget is an alert, not a hard cap. No current promotional balance or charges were queried.

Read-only Stockholm inventory: 0 ECS clusters, 0 ECR repositories, 0 EC2 instances,
0 modern load balancers and 0 classic load balancers; 1 default VPC. This is limited to
those services/region and does not establish zero account-wide charges.

Local audit: read README and every existing docs file, Git history and all tracked implementation
and evidence; baseline was feffb33 with clean main. Six tests and pip check pass again.
Existing image runs healthy as UID 10001 with read-only root, dropped capabilities and both
HTTP endpoints returning 200; temporary test container removed. Three existing PNG screenshots
validated and hashed; no AWS screenshot added. Historical Trivy JSON recomputation matches
44 HIGH, 58 MEDIUM, 61 LOW, 1 UNKNOWN, 0 CRITICAL. Scanner ImageID is the exported archive's
config digest; Docker inspect shows a different manifest identity. Confirmed archive config
reference and all ordered filesystem layers match; no evidence of a stale-image mismatch.
Historical scan is dated October 28 and must be refreshed before rollout.

Scope decision: user's October 29 request explicitly adds Terraform before deployment,
superseding the guide's earlier optional/post-MVP timing. Terraform not found in PATH.
No infrastructure, IAM security, account plan or billing settings changed in this audit.
AdministratorAccess is the existing bootstrap access, not the proposed CI/workload permission model.

Progress: 2 of 7 original MVP outcomes complete (28.6%, rounded to 29%); Stages 0-2 accepted,
Stage 3 partial, Stages 4-7 not started. This ratio is a transparent acceptance count,
not an estimate of remaining hours; Terraform adds work outside the original denominator.

Evidence: evidence/commands/2026-10-29-project-audit.json.
Next batch: project-local Terraform installation with verified download, proposed low-cost
Stockholm architecture and local Terraform configuration/validation. Protect state/plan files
from Git before generating them. Refresh scan and pricing, resolve credit/budget evidence,
then request concrete IAM/provisioning approval before any cloud changes.
