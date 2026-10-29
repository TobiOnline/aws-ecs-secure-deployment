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

## 2026-10-29 - Terraform and architecture preparation batch

Installed Terraform 1.17.1 into ignored project-local .tools from official release;
SHA256 matched official HTTPS checksums. Independent GPG signature verification not performed.
AWS provider 6.71.0 installed with HashiCorp signature verification by Terraform;
committed provider lockfile. Added ignores for tooling, state, plans, variable values and cache.

Authored proposed foundation, optional service and optional GitHub OIDC Terraform in
infrastructure/terraform. fmt and validate pass. Read-only foundation plan: 9 resources;
illustrative full plan: 15. Full plan used a documentation IP and placeholder digest,
not deployable inputs. Negative plan rejected enabled deployment without approved /32 and digest.
No apply or AWS mutation. Raw plans stay ignored; address/action summaries are sanitized.

Read-only network review found three default subnets, public IP mapping and an IGW default route.
Exact selected-subnet effective route must be confirmed before apply.
No existing GitHub provider found. ECS service-linked role absent; automatic creation by ECS
must be included in foundation IAM approval; preserve if shared.

Built Fargate-ready local image stage3: app-owned /app/runtime volume declared in Dockerfile.
Gunicorn temporary files use it because Fargate does not support tmpfs. Read-only root,
UID 10001, volume ownership, healthy endpoints and temporary-container cleanup verified.
Local no-new-privileges remains a local check, not a claimed Fargate setting.
Six app tests and dependency check pass. Fresh Trivy scan completed; 0 CRITICAL,
44 HIGH, 58 MEDIUM, 61 LOW, 1 UNKNOWN; no fixable HIGH/CRITICAL entries.
New dated evidence preserves all October 28 artifacts. Risk remains unresolved, not suppressed.

Drafted architecture diagram, Terraform operation/state/teardown instructions and Stockholm costs.
One task + IPv4 about USD 0.018575/hour at observed list rates; logs/storage/transfer extra.
Proposed USD 1 project allowance has not been approved; credits, expiry, alert delivery and
MFA console screenshots still missing. CI workflow itself remains unimplemented.

CI owns later service task revisions; Terraform ignores that field after initial creation.
Wildcard ECS task-registration permission is documented and region-restricted; remaining
ECR/service/PassRole permissions scoped. OIDC trusts only repository main; branch-subject
trust must be redesigned if a GitHub Environment is used.

Next: capture local Terraform milestone evidence, obtain account credit/budget proof and
concrete foundation/IAM approval. Replan with real reviewed inputs before applying.

## 2026-10-29 - Terraform screenshot evidence
Received and visually inspected user screenshot showing correct personal project path, Terraform v1.17.1 on linux_amd64 and successful verify-infrastructure.sh validation. Saved as evidence/screenshots/03f-terraform-validation.png; no credentials visible. This submission contains no explicit spending or provisioning approval. Credit/expiry/plan and budget threshold evidence remain missing; no AWS changes made.

## 2026-10-29 - Billing screenshots and approval synchronization

User explicitly approved USD 1 total project usage allowance, then approved the explained
Stockholm foundation/IAM changes (9 Terraform resources and automatic ECS service-linked-role
prerequisite). Approval does not include GitHub OIDC trust, public running service or teardown.
These approvals persist; do not request them again unless scope or risk materially changes.

User supplied billing/credits/budget screenshots and approved local-script redaction.
Created clearly named redacted copies; originals preserved in Downloads and never copied
to Git. Opaque rectangles cover account identifiers, credit IDs and browser profile picture.
Pixel comparison confirms every unredacted pixel unchanged; outputs visually checked.
Hashes/rectangles/method recorded in evidence/commands/2026-10-29-screenshot-redactions.json.

Observed: credits summary USD 120 total remaining / USD 119.97 estimated remaining,
USD 0.03 estimated used, while both listed credits show Expired with October 28, 2026
expiration. Do not count this as usable credit confirmation. October estimated bill is
USD 0.00, pending. Budget overview shows USD 1, OK threshold status and Healthy.
Actual notification threshold, recipient delivery and paid/free plan not shown.
Provisioning remains paused for credit-status discrepancy resolution; no AWS changes.

## 2026-10-29 - Credit discrepancy resolved through read-only API

Free Tier GetAccountPlanState reports PAID, ACTIVE and accountPlanRemainingCredits USD 0.00.
This agrees with the screenshot's Expired rows. Do not treat the displayed USD 119.97
estimated summary as usable credit. Account-specific API result is saved in sanitized
evidence/commands/2026-10-29-billing-readiness.json.

Budget API confirms monthly COST budget USD 1, actual spend USD 0.00, ACTUAL notification
GREATER_THAN absolute USD 0.01, notification state OK and three configured subscribers.
Subscriber addresses not printed or stored; delivery not proven. IncludeCredit is true,
so the budget is not a gross-credit-consumption cap. Alerts do not stop resources.

Earlier USD 1 allowance and foundation/IAM approval persist, but paid/zero-credit state
materially changes the expected payment source. Ask whether the user authorizes up to
USD 1 actual charges or wants AWS Billing Support clarification first. No provisioning,
IAM mutation, upgrade or support message sent.

Official guidance: expired credits are unavailable for use:
https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/useconsolidatedbilling-credits.html

## 2026-10-29 - Actual-charge authorization
User selected 'Proceed with the under-$1 target' after explicit disclosure that final billing cannot be guaranteed and credits are unavailable. Authorized actual charges, short deployment window and prompt teardown. Previously approved foundation/IAM scope retained. No hard cap claimed.

## 2026-10-29 - Approved foundation applied and image published
Actual charges targeting under USD 1 explicitly accepted. Refreshed regional pricing and exact nine-create plan, verified BASIC ECR scanning and selected subnet effective IGW route, then applied foundation: nine added, no task/public endpoint/OIDC. Published tested stage3 image under commit-SHA tag; digest in evidence/commands/2026-10-29-ecr-image.json. ECR scan query did not return findings; local Trivy evidence remains separate. Local CI checks pass: lint, six tests, Gitleaks history and runtime dependency audit. Manual-only main workflow and delivery code prepared; no GitHub run yet. Screenshots pending.

## 2026-10-29 - Delivery preparation and access blocker
Foundation created and ECR image published. Native ECR BASIC manual scan returned
UnsupportedImageTypeException for this image; retain local Trivy results (44 unpatched HIGH),
do not claim an ECR scan pass. Pipeline local lint/tests/Gitleaks history/runtime audit pass.

Manual-only workflow commit 155bc39 was rejected by GitHub on push because OAuth token lacks
workflow scope. User asked to run gh auth refresh -h github.com -s workflow. No workflow run
or OIDC role created. Corrected a YAML quoting issue during local inspection and parsed final YAML.
Temporary runner 2.338.2 downloaded with official asset digest verified; invariant globalization
mode resolves missing ICU without system install. Runner is not registered or running.

Prepared guarded evidence/recovery/cleanup scripts; not executed. Current remaining Terraform
plan includes seven creates: OIDC provider/role/policy, task definition, service, /32 ingress,
CPU alarm. Full demo/failure/teardown approval requested in one batch, still pending.
No Fargate tasks running. Latest source/evidence/docs committed locally; push blocked by scope.

## 2026-10-29 - Final demo authorization and real CI gate
User completed GitHub workflow-scope refresh and explicitly approved all remaining seven resources, temporary local runner, 44-HIGH residual risk for this short demo, reversible failure/rollback and project-only teardown. Default VPC/Identity Center/shared service roles preserved. Commits pushed successfully. Deliberate-failure workflow 40862041799 failed at Tests; all later build/credential/delivery steps skipped. Ephemeral runner deregistered after job. Approved OIDC provider/role/policy applied separately while deployment disabled; role ARN configured as GitHub secret, no static AWS keys. Passing OIDC publication workflow 40862493388 in progress. Browser screenshot automation stopped because current URL could not be established safely; no further UI input attempted. Screenshots remain missing.

## 2026-10-29 - OIDC mismatch diagnosed and corrected
Passing workflow first attempt failed at role assumption after all security checks passed. GitHub repository API and sanitized CloudTrail identity confirmed immutable subject (owner/repository IDs appended), while Terraform used legacy name-only subject. Verified current GitHub official OIDC docs; changed only the existing role trust to exact immutable main subject, no wildcard expansion. Read-only plan showed one role update; applied within approved repo/main scope. Saved failure and correction evidence. Rerun requested on fresh ephemeral runner. No Fargate task started during troubleshooting.

## 2026-10-29 - Live deployment and passing OIDC delivery
Corrected publication workflow 40864000531 passed all steps, including actual OIDC assumption and ECR publication. Previous retry failed on root-owned scanner cache during checkout; fixed scanner to host UID/GID and isolated security cache, plus unique ephemeral workspaces. No gate bypassed. Applied remaining four approved service/ingress/CPU-alarm resources, with current operator /32 and local 45-minute scale-to-zero guard. Initial live API evidence: one RUNNING/HEALTHY task, revision 1 COMPLETED; / and /health HTTP 200; CloudWatch messages captured and CPU alarm OK at 80 percent threshold. Controlled bad-release/recovery operation now in progress. UI screenshot automation unavailable at URL-confidence safety boundary; requested user captures without delaying cleanup.

## 2026-10-29 - Recovery proven and delivery metadata permission corrected
Controlled revision 2 exited code 1; observed three stopped failed tasks during rollout, while healthy revision 1 remained running. ECS automatically restored revision 1; recovery HTTP/health/log/alarm checks pass (incident/recovered evidence). Final CI run 40865452609 passed security/OIDC/publication but DescribeTaskDefinition was denied on resource *. AWS service-authorization table confirms no resource-level scope for that read API. Corrected only the existing delivery policy: DescribeTaskDefinition joins RegisterTaskDefinition with wildcard resource and Stockholm region condition; other ECR/service/PassRole scopes unchanged. Retry tags now include run attempt. No admin role granted. Guarded cleanup supports index-manifest dependency retries and captures conservative task-lifetime estimate before cluster deletion.

## 2026-10-29 - End-to-end delivery, teardown and closeout
Final CI run 40866951465 passed all steps and deployed revision 3 from source c9cb57a.
Published/requested/runtime digest matches recorded in end-to-end-version and final-deployment
evidence. Healthy task, both HTTP 200 endpoints, logs and alarm OK verified before teardown.
31 real CPU datapoints preserved. No public downtime claimed during the prior automatic rollback.

Executed approved project-only teardown: scaled service to zero, waited for tasks stopped,
captured six task lifetimes, removed 12 image manifests, destroyed all 16 managed resources and
deregistered two non-Terraform project revisions. Independent inventory confirms 0 clusters,
repositories, project log groups/alarms/security groups/active task revisions; all three project
roles and GitHub provider absent; Terraform managed state empty. Default VPC remains.
Temporary runner registrations absent, stale delivery role secret removed; finite local guard
stopped after verification. Default network, Identity Center and shared service role preserved.

Conservative observed compute/IPv4 estimate USD 0.01150609; other fees/tax excluded and actual
AWS bill delayed. No zero-cost or hard-cap claim. Case study/architecture/runbook updated.
Live cloud/CI screenshots are still missing; screenshot automation stopped safely and no paid
runtime was kept waiting for visuals. Original MVP outcomes 1-6 verified; outcome 7 partial
for final billing/visual evidence (6/7 = 86% rounded). Release v0.1.0-demo prepared at close.

Release-close checks observed: six app tests passed, pip check clean, lint passed across app/tests/scripts, Terraform fmt/validate passed, Gitleaks full Git-history report has zero findings. Targeted candidate-text scan found no AWS account identifier/access-key/private-key patterns. Ignored operational state/plan files restricted to owner-only permissions where controlled.
