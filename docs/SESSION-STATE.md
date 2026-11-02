# Session state

Current handoff: see the November 2 billing/documentation closeout at the end of this file. No demo workload remains running; earlier snapshots are historical.

Date: 2026-10-28 (Africa/Lagos)
Stage: 3 - preflight; Stages 0, 1 and 2 COMPLETE.

## Verified
- Personal project: /home/olawo/DevSecOps/aws-ecs-secure-deployment.
- Accidental Webforx directory absence verified; no content deleted.
- Private origin: https://github.com/TobiOnline/aws-ecs-secure-deployment.git.
- GitHub authenticated as TobiOnline; HTTPS pushes use gh credential helper.
- Stage 0 and Stage 1 screenshots inspected and saved under evidence/screenshots/.
- Host Python 3.14.4; Flask 3.1.3; Gunicorn 26.2.0; pytest 9.2.0. Six tests pass.
- Docker 29.6.2 and Compose v5.3.1 available through Ubuntu WSL integration.
- Container Python 3.14.10; base pinned in Dockerfile; non-root UID 10001.
- Container health and HTTP checks pass with restricted runtime; temporary container removed.
- Trivy 0.76.1 scan: five fixable HIGH entries removed with pip; 44 HIGH remain without listed fixes.
- Full scan and residual-risk decisions in docs/SECURITY.md and evidence/test-results/02-*.
- No AWS resources created; AWS account, region, credits and pricing unverified.

## Pending
- Stage 2 screenshot saved and inspected: evidence/screenshots/02-docker-running-and-scan.png.
- AWS CLI unavailable in WSL at last check; AWS access setup required for Stage 3.
- Cloud rollout requires current pricing, budget/credit verification, concrete approval and residual-risk disclosure.
- Stage 2 implementation pushed as fe709b0. User reports possible USD 100 credit; amount, expiry, account plan and eligibility remain unverified.

## Next action
Help user verify AWS console access, plan, credit balance/expiry and existing charges; then select region and prepare concrete cost/resource approval. No provisioning yet.

## Working preferences
Batch questions and approvals where practical. Explain current stage, current activity
and what it enables in plain language. User targets same-day progress; retain all acceptance gates.

## 2026-10-29 synchronized handoff - authoritative current state

This dated section supersedes outdated availability and account-status notes above;
the October 28 snapshot is retained for traceability.

Current checkpoint: Stage 3 PARTIAL. Stages 0-2 accepted; Stages 4-7 not started.
Original MVP acceptance ratio: 2/7 = 29% rounded; Terraform newly required and not implemented.

Environment verified in Ubuntu: Python 3.14.4, Docker server 29.6.2, AWS CLI v2.39.1.
Profile tobi-admin; SSO session tobi-sso; default region eu-north-1;
Identity Center region us-east-1; role configured AdministratorAccess.
STS and regional read-only inventory calls succeeded; no credential values stored.
Terraform executable not found. Git baseline feffb33, main tracking the personal origin.

User-reported: account label TOBI, root and administrator MFA, paid account,
USD 100 credits initially available. Do not treat those as saved AWS console evidence.
Current balance/expiry and current charges remain unverified.
Zero Spend Budget presence verified: COST budget amount USD 1, one notification rule;
threshold, delivery and credit filters still need inspection.

Verified Stockholm inventory: 0 ECS clusters/ECR repositories/EC2 instances/modern or
classic load balancers; default VPC present. This is not a global resource/cost inventory.
No cloud changes made by this audit.

Local revalidation: pip check and six tests pass; current image healthy as UID 10001,
both endpoints pass under restricted runtime; temporary container removed.
Historical scan matches archive config and all current filesystem layers; remaining
44 HIGH are documented, not resolved or accepted for production. Refresh before rollout.
Existing screenshots 00/01/02 confirmed; AWS screenshots remain missing.

Decisions: Terraform added by explicit October 29 user request; preserve existing app/history/docs.
Do not use bootstrap AdministratorAccess for GitHub or task roles.
Batch safe inspections/tests; request concrete approval for IAM, paid provisioning and destruction.

Open blockers: Terraform unavailable; architecture/IaC/OIDC/CI not authored; current credit,
budget detail and AWS security screenshots missing; residual-image-risk review required.
No active SSO access blocker was observed. Historical AWS troubleshooting details not supplied.

Exact next batch:
1. Install verified Terraform into an approved project-local ignored tools path.
2. Draft Stockholm architecture/cost/cleanup proposal and Terraform config; fmt/validate locally.
3. Refresh vulnerability scan and assess remaining findings.
4. Batch request missing account/budget screenshots and concrete cloud/IAM approval after plan review.
No Terraform apply, IAM mutation or cloud provisioning is authorized by this audit alone.

Audit evidence: evidence/commands/2026-10-29-project-audit.json.
Docs changed in this batch: README plus engineering log, roadmap, session state, evidence index,
security and cost/cleanup appendices. Commit/push status is verified in Git at batch close.

## 2026-10-29 Terraform batch - latest handoff

Stage 3 remains PARTIAL; original MVP ratio remains 29%. No cloud apply or IAM mutation.
Terraform now installed at .tools/terraform (1.17.1), SHA256 verified from official HTTPS
checksums; independent GPG signature not verified. AWS provider 6.71.0 lockfile recorded.
Configuration under infrastructure/terraform passes fmt/validate.
Foundation plan: 9 Terraform creates. Full illustrative plan: 15 creates, placeholder inputs.
Missing-input negative plan correctly rejected deployment. Raw plans/logs ignored in .cache.

No existing GitHub OIDC provider; AWSServiceRoleForECS absent.
Default VPC has three default subnets with public-IP mapping; IGW default route observed.
Verify selected subnet's exact effective route before apply.
Potential automatic ECS service-linked-role creation requires inclusion in IAM approval.

Image aws-ecs-secure-deployment:stage3 built and tested: app-owned /app/runtime volume,
read-only root, non-root UID, both HTTP endpoints healthy; test container/volume removed.
Fresh dated Trivy findings unchanged: 44 HIGH with no listed fix; no CRITICAL/fixable HIGH.
Current implementation scripts default to stage3 and preserve dated scan evidence.
Historical October 28 files unchanged. Container local hardening is not identical to Fargate.

Proposed architecture/costs and operating/teardown instructions are reviewable.
Task+IP list cost about USD 0.018575 per task-hour; storage/logs/transfer extra.
Proposed USD 1 total project usage allowance NOT approved; current credit/expiry and billing
evidence still missing. No GitHub workflow authored or triggered.

Next batch depends on grouped user response:
- Supply redacted current credits/expiry/plan and budget threshold evidence.
- Approve a concrete spending allowance and the 9-resource foundation plus automatic ECS
  service-linked-role prerequisite; no public task or GitHub trust in that first phase.
- Capture Terraform version/validation/plan-summary screenshot at proposed
  evidence/screenshots/03f-terraform-validation.png (MISSING).
Then replan/check selected route and apply only the approved phase; publish versioned
image only after approval. GitHub OIDC and actual service rollout need reviewed approval later.
Current changed scope: Terraform, Docker runtime adaptation, repeatable scan utilities,
architecture/cost/security/handoff docs, new dated build/runtime/scan/plan evidence.
Git commit and push verified at batch close.

## 2026-10-29 latest evidence update
Terraform screenshot received and saved: evidence/screenshots/03f-terraform-validation.png, showing version 1.17.1 and successful validation. Supersedes earlier MISSING status for this screenshot only. Account credit/budget screenshots, spending allowance and foundation/IAM approval remain pending. Screenshot upload is not provisioning authorization. Next: obtain these together, then refresh/check the approved plan before any apply. No AWS changes.

## 2026-10-29 billing evidence - latest authoritative update

USD 1 project usage allowance and the explained 9-resource Stockholm foundation/IAM changes,
including possible ECS service-linked-role creation, are explicitly approved by the user.
Do not ask for those same approvals again. GitHub OIDC, public task rollout and teardown
remain outside this approval.

Redacted screenshot copies saved:
- evidence/screenshots/03c-aws-credits-and-expiry.png
- evidence/screenshots/03d-aws-budget-overview.png
- evidence/screenshots/03g-aws-october-bill.png
Original Downloads files unchanged; only sanitized copies committed. User authorized
deterministic local redaction. Outside redaction rectangles, pixels are unchanged.

Financial blocker: credits page summary says USD 120 remaining / USD 119.97 estimated
remaining, but both credit rows are Expired dated October 28, 2026. Usable credits cannot
be assumed. Bill screenshot is USD 0.00 estimated/pending. Budget overview confirms USD 1
and Healthy/OK, but not actual threshold, delivery or plan type.
No AWS changes during redaction. Current next action: resolve credit status and inspect
budget details read-only; retain approvals while readiness is investigated.

## 2026-10-29 billing API result - latest next action

Verified read-only Free Tier API: PAID/ACTIVE, remaining credits USD 0.00.
Do not count the screenshot's USD 119.97 estimated summary as usable credits.
Verified budget: USD 1 monthly, actual cost USD 0, absolute ACTUAL > USD 0.01 notification,
OK state, three configured subscribers; addresses not recorded and delivery not tested.
IncludeCredit=true; budget is not a hard/gross spending cap.

Spending allowance/foundation scope approvals remain valid, but payment-source risk changed:
possible actual charges, not credit consumption. Await user decision to authorize up to
USD 1 actual charges or contact AWS Billing Support to investigate credit status first.
Do not provision pending this clarification. No AWS mutations in this batch.
Evidence: evidence/commands/2026-10-29-billing-readiness.json.

## 2026-10-29 authorization update
User explicitly accepts actual charges targeting under USD 1, no guaranteed cap, short run and prompt teardown. Credit investigation no longer blocks the approved foundation. Refresh and validate the exact plan, then apply foundation only; no task/OIDC in initial apply.

## 2026-10-29 foundation execution - current state
User accepts actual charges targeting under USD 1, short deployment and prompt teardown. Approved nine-resource foundation applied; no Fargate task/public endpoint/OIDC yet. Tested image published; exact tag/digest in evidence/commands/2026-10-29-ecr-image.json. Terraform state is local/ignored: preserve it. Current next batch: commit prepared manual CI, run it on checksum-verified ephemeral local runner (no hosted compute), obtain approval for remaining seven-resource OIDC/service/alarm proposal and controlled recovery/teardown. Screenshot evidence missing for actual ECR/foundation.

## 2026-10-29 current blockers after foundation
Foundation exists and image is stored in ECR. No Fargate task, public endpoint or OIDC role.
Native BASIC scan unsupported for image (UnsupportedImageTypeException); local Trivy findings
remain the security evidence. Do not claim native scan passed.

Prepared CI local checks pass, final YAML parsed, scripts compile. Runner downloaded/verified
but not registered; DOTNET_SYSTEM_GLOBALIZATION_INVARIANT=1 needed on this WSL runtime.
No GitHub-hosted compute triggered; no GitHub workflow runs yet.
Commit 155bc39 push rejected: gh login lacks workflow scope. User must run
gh auth refresh -h github.com -s workflow, then notify us. Do not print authentication codes/tokens.

Pending separate async approval covers exact remaining seven creates, documented 44-HIGH risk,
temporary local runner, controlled failure/rollback and project-only teardown. Actual-charge
under-USD-1 target is already approved; do not request it again.

Next: once workflow scope and remaining approval arrive, push prepared source, dispatch trusted
CI on ephemeral local runner, apply refreshed approved remaining plan, verify/recover/deploy and
promptly clean up project-only resources. State and ignored raw plans must be preserved.
Screenshot/evidence collection still required; no cloud milestone claimed fully complete yet.
Local commits ahead of origin; push unavailable until workflow permission refresh.

## 2026-10-29 live demo in progress - latest
All remaining demo/fault/teardown permissions explicitly approved, with under-USD-1 actual-charge target and residual 44-HIGH risk accepted for this temporary demo. GitHub workflow-scope refresh complete; commits through 65f4146 pushed. Real failing workflow 40862041799 proves test failure skips credentials/build/delivery. OIDC provider and scoped role/policy now applied, no static AWS keys; GitHub role secret configured. Passing publication workflow 40862493388 running on ephemeral local runner. No Fargate app service yet. Next: verify passing OIDC publication, apply reviewed remaining four service/ingress/alarm resources, collect health/log evidence, run controlled bad rollout/recovery, demonstrate CI task revision delivery, then promptly execute approved project cleanup. Preserve local Terraform state until post-cleanup inventory. Automatic screenshot path stopped at browser URL-policy boundary; mark missing, request user captures without delaying teardown.

## 2026-10-29 OIDC correction - latest
Run 40862493388 attempt 1 failed role assumption because this new repo uses immutable GitHub subject IDs. Exact main-only trust corrected and applied; no access expansion. Rerun in progress. Prepared finite local 45-minute scale-to-zero failsafe for subsequent app run, but no task running yet. Next: verify rerun, deploy remaining four approved resources, collect/recover/CI-deliver and promptly teardown.

## 2026-10-29 deployed demo - latest
Passing OIDC publication workflow 40864000531 succeeded. All 16 project Terraform resources now applied. Initial service has one healthy running task, revision 1, successful HTTP endpoints, logs and CPU alarm OK. Controlled fault/recovery script currently running; do not interrupt with a concurrent service update. Finite 45-minute local guard active. Next: verify recovery, run a final CI-driven task revision deployment, collect evidence and execute approved teardown immediately. Screenshots missing unless user supplies them; never delay cleanup for screenshots.

## 2026-10-29 recovery and final delivery retry
Automatic rollback proven: bad revision 2 exit 1 rejected, revision 1 restored and HTTP 200 verified. Final CI publication succeeded but metadata read denied before service update; correcting required API-wide read with Stockholm-only condition. Existing healthy service remains revision 1. Next: fresh final deployment workflow with corrected policy/code; after success collect evidence and run approved teardown. Local 45-minute scale-zero guard remains active.

## 2026-10-29 final operational handoff - authoritative current state
Technical demo complete; cloud resources cleaned up. Portfolio closeout PARTIAL.
Original MVP outcomes 1-6 verified; final cost/evidence outcome partial: 6/7 = 86% rounded.

Final passing deployment workflow: 40866951465. Delivered healthy revision 3, exact image digest
match and both endpoints HTTP 200. Prior controlled revision 2 failed and automatically
restored revision 1. All security checks, history scan and runtime audit exercised.
Native ECR scan unsupported; 44 unpatched HIGH Trivy findings documented/accepted for demo.

Teardown removed all 16 Terraform-managed resources and 12 manifests; extra project task
revisions deregistered. Independent cleanup evidence confirms no project workload, IAM/OIDC,
log/alarm/security-group resources; state empty; no temporary runner or stale role secret.
Default VPC/Identity Center/shared service role remain. No live app endpoint.
Local finite cost guard stopped after verification. Do not recreate resources without new approval.

Compute+IPv4 conservative estimate USD 0.01150609; excludes ancillary fees/tax. Final bill pending.
Evidence: end-to-end-version, final-deployment, ci-final-deployment, incident-recovery,
cpu-metrics, teardown, task-cost-estimate and cleanup-verification JSON files under
evidence/commands/2026-10-29-*.
Source/operations docs and demo release tag v0.1.0-demo are finalized at batch close;
consult Git history/tag and origin for exact commit/push identity.

Remaining work needs no running AWS app:
1. After billing updates, review final project-service charges in AWS Billing and record result.
2. Capture real GitHub workflow screenshots; cloud runtime screenshots were not captured before
   teardown. Record missing images honestly; no redeploy merely for screenshots without approval.
3. Account MFA screenshots and AWS Support credit-review outcome remain separate
   account-setup evidence, not proof of application deployment.
Previous snapshots above are retained as history; this section supersedes deployment blockers.

## 2026-10-29 latest CI evidence update
Passing/failing CI summary screenshots saved as evidence/screenshots/05a-ci-success-summary.png and 05b-ci-blocked-summary.png. User originals unchanged; tabs/profile picture redacted, remaining pixels unchanged. Run IDs visually match previously verified API records. CI screenshot summary gap closed; step-level proof remains in existing run JSON. No AWS resources restarted. Remaining closeout: final billing confirmation and other uncaptured cloud screenshots. Next: review updated AWS Bills when available; no paid deployment needed. Demo tag v0.1.0-demo remains the earlier release snapshot; main includes subsequent evidence closeout.


## 2026-11-02 - Billing evidence and final documentation closeout

User-supplied November 2 screenshots were inspected and sanitized. The primary image
08a-billing-month-summary.png shows October 2026 account cost USD 0.23 and November
month-to-date USD 0.02: USD 0.25 combined observed account cost, below the USD 1 target.
This is account-level dashboard evidence, not a project-attributed service breakdown or
a finalized invoice. The November USD 0.02 alone is not the October project's total.
The service chart also displays non-ECS categories, including KMS; exact charge attribution
and any continuing account-level charges are not established by these captures. No new
AWS inventory or mutations were performed, and no workload was restarted. October 29
cleanup verification remains the last independent resource inventory.

08b-budget-observed-spend.png is supporting evidence: USD 1 budget, USD 0.02 displayed
spend, and Exceeded (1). The existing alert threshold was USD 0.01; an exceeded alert
does not imply the USD 1 allowance was exceeded. This capture and the home dashboard's
OK indicator differ; neither proves alert delivery or enforces a spending cap.

Opaque masks hide browser tabs/profile, AWS account number and administrator identity.
Original Downloads images are unchanged; all pixels outside masks verified unchanged.
Hashes and masks: evidence/commands/2026-11-02-billing-redactions.json.

Technical implementation, rollback, teardown and documentation handoff are complete.
Strict original acceptance remains 6/7 (86% rounded): outcome 7 has billing evidence now,
but final project-attributed invoice confirmation and uncaptured live cloud screenshots
remain documented limitations. These are optional follow-up evidence items for the
closed demonstration; no redeployment is needed. Do not label this 100% evidence coverage.
No automatic scanning triggers, repository visibility changes or paid resources were added.
