# Roadmap

- [x] Stage 0: personal workspace, baseline docs, private origin, push, accidental-directory absence and screenshot verified. Evidence: evidence/screenshots/00-personal-workspace-and-git.png; baseline ae4dec5, screenshot shows synced commit 42d59c2.
- [x] Stage 1: Flask app, six passing tests, pinned dependencies, live Gunicorn validation and screenshot evidence saved. See evidence/test-results/01-* and evidence/screenshots/01-local-tests-health.png.
- [x] Stage 2: digest-pinned non-root container built; restricted runtime/health/HTTP checks pass; scan remediations and remaining findings documented. Screenshot: evidence/screenshots/02-docker-running-and-scan.png; reports: evidence/test-results/02-*; implementation fe709b0.
- [ ] Stage 3: approved AWS cost/IAM foundation, private ECR and immutable image evidence.
- [ ] Stage 4: approved temporary ECS deployment, network controls, service health and logs.
- [ ] Stage 5: OIDC CI/CD, passing and blocked workflows, gated deployment evidence.
- [ ] Stage 6: monitoring, reversible incident, diagnosis and verified rollback.
- [ ] Stage 7: security review, case study, release, cleanup verification and cost review.

Each stage remains partial until its validation, documentation, evidence, commit, push and session-state requirements are addressed.

## 2026-10-29 audited plan - current dependencies

The earlier checklist remains the historical stage sequence. Stage 3 is now PARTIAL:
CLI/SSO, regional inventory and budget presence verified; architecture, credits, least-privilege
access and ECR image publication are incomplete. No deployed workload or CI/CD evidence exists.
Audit source: evidence/commands/2026-10-29-project-audit.json.

Progress measure: original MVP outcomes 1 and 2 complete; outcomes 3-7 incomplete:
2/7 = 28.6% (rounded 29%). Stages 0-2 complete does not mean 3/8 of project effort.
Terraform is a newly requested requirement and is not counted as already completed.

- [x] Audit existing repo/history/docs, test evidence, screenshots and scan findings.
- [x] Re-run six app tests, dependency check and hardened local container checks.
- [x] Verify AWS CLI/SSO and Stockholm service inventory; confirm budget/rule presence.
- [~] AWS account setup evidence: root/admin MFA, paid plan and initial credits user-reported; screenshots and current credit/expiry verification pending.
- [ ] Finalize architecture and costs: default-VPC/subnet suitability, minimal temporary exposure, no ALB/NAT by default, log retention, teardown and residual-image-risk review. Depends on fresh pricing, credit/budget verification and access design.
- [ ] Install Terraform locally; verify official archive checksum/signature as applicable; record version. Protect local state/plans/variables from Git.
- [ ] Implement Terraform configuration for reviewed network, ECR, ECS, logs and IAM; pin provider constraints/lock; fmt/validate and review plan. Depends on architecture; plan may read AWS but apply requires approval.
- [ ] Define least-privilege execution, task and GitHub OIDC roles; restrict trust to intended repository/ref/environment. Existing AdministratorAccess is bootstrap only. IAM changes require explicit approval.
- [ ] Stage 3 completion: approved private ECR repository, versioned image push and digest evidence. Depends on approved foundation plan and refreshed image scan.
- [ ] GitHub Actions: pinned actions, tests/lint, secret/dependency/image scans, OIDC push and gated deploy; demonstrate passing and deliberately blocked runs. Cloud delivery depends on approved roles/ECR; local workflow authoring can proceed earlier.
- [ ] Stage 4: approved short-lived ECS Fargate rollout in eu-north-1, restricted access, healthy service and external endpoint checks where approved. Depends on ECR image, roles and reviewed network/cost plan.
- [ ] Stage 6 monitoring/recovery: CloudWatch logs, justified alarm, controlled fault and rollback; collect dated before/during/after evidence. Depends on healthy deployment and approved simulation.
- [ ] End-to-end release validation: new image/task revision delivered through CI; verify controls and document limitations.
- [ ] Stage 7: approved teardown, verify all project-created resources across relevant regions/services, review delayed costs, finalize runbook/diagram/case study, secret/history review and tagged release.

At each meaningful checkpoint update engineering log, evidence index and session state.
No apply, IAM changes, paid resources or destructive cleanup without the user's explicit approval.

## 2026-10-29 implementation batch update

- [x] Terraform 1.17.1 project-local install and official checksum verification.
- [x] AWS provider 6.71.0 signature-verified by Terraform, lockfile recorded.
- [x] Local state/tool/plan/input ignore rules added.
- [~] Architecture, cost and IAM proposal authored; approval and selected-route check pending.
- [~] Terraform foundation/service/OIDC authored; fmt/validate and read-only plans pass; not applied.
- [x] Negative guard plan rejects missing digest/operator /32.
- [x] Fargate-compatible volume adaptation builds and runs; fresh image scan recorded.
- [ ] Terraform milestone screenshot evidence.
- [ ] Credit/expiry/budget alert evidence and spend allowance approval.
- [ ] Foundation/IAM approval and apply, actual ECR push/digest, service approval and rollout.
- [ ] CI/CD workflows, monitoring incident/rollback, end-to-end delivery and final teardown/release.

MVP ratio remains 2/7 (29% rounded): prepared infrastructure is not deployed infrastructure.
Earlier pending tool-install items are now complete; Terraform deployment remains incomplete.

### 2026-10-29 evidence update
- [x] Terraform milestone screenshot saved and inspected: evidence/screenshots/03f-terraform-validation.png.
- [ ] Current credit/expiry/plan and budget threshold evidence.
- [ ] Explicit project spending allowance and foundation/IAM provisioning approval.

### 2026-10-29 billing evidence and permissions update
- [x] User approved USD 1 total project usage allowance and the described foundation/IAM scope.
- [x] Redacted credits, budget overview and October bill screenshots saved and inspected.
- [ ] Resolve credits discrepancy: summary balance versus both rows marked Expired.
- [ ] Capture/verify actual budget notification threshold and account plan.
- [ ] Proceed with approved foundation only after billing readiness is resolved and plan refreshed.
No OIDC/public-service/destructive approval inferred.

### 2026-10-29 billing readiness result
- [x] Account plan independently verified: PAID, ACTIVE.
- [x] Free Tier API remaining credits USD 0.00; expired-row discrepancy resolved conservatively.
- [x] Budget threshold verified: monthly actual cost greater than USD 0.01; subscriber configuration present.
- [ ] Clarify authorization for actual charges up to USD 1 given zero usable Free Tier balance, or resolve credits with AWS Billing Support first.
Foundation/IAM scope remains approved; no cloud changes made.

### 2026-10-29 foundation execution
- [x] Approved nine-resource foundation applied; no app task or public endpoint.
- [x] Versioned image published to private ECR; digest recorded.
- [~] Stage 3 implemented; screenshot evidence and final checkpoint push pending.
- [~] Manual CI workflow authored; local lint/tests/history-secret/runtime dependency checks pass. Actual workflow runs pending.
- [ ] Remaining OIDC, service, restricted ingress, alarm, recovery and teardown approvals/execution.

### 2026-10-29 pipeline readiness and blockers
- [x] Local lint/tests/history-secret/runtime-audit checks pass; workflow YAML parsed.
- [x] Temporary local runner package verified; not registered/started.
- [~] Foundation/ECR implemented; screenshots and push pending.
- [ ] GitHub workflow scope refresh; prepared commits cannot push without it.
- [ ] Explicit remaining seven-resource demo/recovery/cleanup approval.
- [ ] Actual passing/failing GitHub runs, OIDC delivery, deployment, recovery and cleanup evidence.
Native ECR scan is unsupported for this image; local Trivy remains required.

### 2026-10-29 real CI progress
- [x] Remaining full demo/fault/cleanup approval and GitHub workflow scope obtained.
- [x] Intentional failing workflow proves later delivery steps skipped (40862041799).
- [x] Approved main-only GitHub OIDC access applied; static AWS keys absent.
- [~] Passing workflow 40862493388 running; app deployment still disabled.
- [ ] Service/ingress/alarm deployment, live checks, recovery, CI revision delivery and approved teardown.
- [ ] Actual ECR/CI/deployment/cleanup screenshots; browser automation blocked by URL-confidence safety check.

- [x] Diagnose actual OIDC failure and apply exact immutable repo/main trust correction; successful rerun still pending.

### 2026-10-29 live validation
- [x] Real passing security/OIDC image-publication workflow (40864000531).
- [x] ECS service, operator /32 ingress and CPU alarm deployed.
- [x] Actual one-task health, both HTTP 200 endpoints, logs and alarm OK evidenced.
- [~] Controlled bad release and recovery in progress.
- [ ] CI-driven new task revision, teardown verification, final case study/cost review and missing screenshots.

- [x] Real failed revision 2 and automatic recovery to healthy revision 1 evidenced.
- [~] Final CI image publication passed; task update blocked by metadata-read permission, minimal correction applied/in progress.
