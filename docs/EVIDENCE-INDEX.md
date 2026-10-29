# Evidence index

| Milestone | Evidence | Date | Result | Privacy |
|---|---|---|---|---|
| Stage 0 preflight | Observed command outputs in Codex chat | 2026-10-28 | Personal project absent before creation; accidental directory empty; tool/auth blockers observed | No credentials captured |
| Stage 0 screenshot | evidence/screenshots/00-personal-workspace-and-git.png | 2026-10-28 | Correct personal path; clean main matching origin/main at 42d59c2 | Inspected: no credentials visible; username/hostname visible |
| Stage 0 commit/push | Local baseline ae4dec5; remote main 344d706 | 2026-10-28 | Private repository and matching local/remote main verified | Inspect remote before sharing |

Repository: https://github.com/TobiOnline/aws-ecs-secure-deployment (PRIVATE, verified 2026-10-28). Screenshot captured and inspected.

| Accidental-directory resolution | WSL test confirmed path absent (Codex command output) | 2026-10-28 | Already absent at cleanup recheck; no deletion needed | No secrets |

| Stage 1 tests | evidence/test-results/01-local-tests.txt | 2026-10-28 | pip check passed; 6 tests passed | No secrets |
| Stage 1 live HTTP | evidence/test-results/01-live-http.txt; 01-gunicorn.log | 2026-10-28 | Gunicorn returned expected 200/200/404; stopped afterward | Localhost only; no secrets |
| Stage 1 screenshot | evidence/screenshots/01-local-tests-health.png | 2026-10-28 | Six tests pass and saved HTTP checks visible | Inspected: no credentials |

| Stage 2 build | evidence/test-results/02-build.txt | 2026-10-28 | Final image builds successfully | No credentials |
| Stage 2 runtime | evidence/test-results/02-runtime.txt | 2026-10-28 | Non-root, healthy, both endpoints pass; image ID and size recorded; test removed | Localhost only |
| Stage 2 scan | evidence/test-results/02-trivy.json; 02-scan-summary.txt; 02-scan-before.txt | 2026-10-28 | Five fixable HIGH entries removed; 44 unpatched HIGH remain | Public package/image identifiers |
| Stage 2 screenshot | evidence/screenshots/02-docker-running-and-scan.png | 2026-10-28 | Non-root healthy container, successful endpoints and full severity counts visible | Inspected: no credentials |

## 2026-10-29 audit and missing AWS evidence

Existing local evidence was inspected, not accepted merely because paths exist:
test transcript contains six passing tests; live transcript contains 200/200/404;
runtime transcript identifies UID/image/size and successful HTTP checks. Recomputed scan
counts match the summary. Exported config identity and ordered layer comparison establish
scan linkage to the current local image. Existing PNGs match the screenshots reviewed in chat.

| Evidence | Status | Result / limitation |
|---|---|---|
| evidence/commands/2026-10-29-project-audit.json | Saved | Sanitized current tests/tooling/SSO/inventory/budget audit and screenshot hashes |
| screenshots/00, 01, 02 under evidence/ | Existing, valid PNGs, reviewed in prior chat | Local stages only; no AWS screenshots |
| evidence/test-results/02-trivy.json | Existing, October 28 scan validated | 44 HIGH remain; not a fresh October 29 DB scan |
| evidence/screenshots/03a-root-mfa.png | MISSING; proposed path only | Capture MFA-enabled status; hide account/email/device identifiers and never capture codes, QR seeds or recovery codes |
| evidence/screenshots/03b-admin-mfa-sso.png | MISSING; proposed path only | Capture administrator MFA/SSO status without portal URL, credentials or tokens |
| evidence/screenshots/03c-credits-plan.png | MISSING; proposed path only | Show plan, remaining credit and expiry; redact billing/account identifiers |
| evidence/screenshots/03d-budget-alert.png | MISSING; proposed path only | Show amount, thresholds and alert configured; redact recipient/account identifiers |
| evidence/screenshots/03e-stockholm-inventory.png | MISSING; proposed path only | Show selected services empty in Stockholm; limited scope must be stated |
| evidence/screenshots/03-ecr-image.png | NOT STARTED | Save only after actual approved image publication |
| evidence/screenshots/04-ecs-service-health.png | NOT STARTED | Real deployment, service health and logs required |
| evidence/screenshots/05-ci-passing-and-blocked.png | NOT STARTED | Actual passing and intentionally failed workflows required |
| evidence/screenshots/06-cloudwatch-incident.png | NOT STARTED | Observed incident and recovery required |
| evidence/screenshots/07-cleanup-verification.png | NOT STARTED | Actual teardown and cost/resource verification required |

MFA/plan/initial credit statements are user-reported until suitable evidence is saved or verified.
No missing screenshot was created or marked as captured by this audit.

## 2026-10-29 Terraform preparation evidence

| Evidence | Result |
|---|---|
| evidence/commands/2026-10-29-terraform-install.json | Terraform version, official source/checksum; independent GPG not verified |
| infrastructure/terraform/.terraform.lock.hcl | AWS provider 6.71.0 and integrity hashes |
| evidence/test-results/2026-10-29-terraform-validation.txt | Final configuration validates |
| evidence/commands/2026-10-29-foundation-plan.json | 9 proposed Terraform creates; no apply |
| evidence/commands/2026-10-29-full-proposal-plan.json | 15 proposed creates; documentation-only IP/digest; no apply |
| evidence/commands/2026-10-29-terraform-guards.json | Missing-input deployment rejected |
| evidence/commands/2026-10-29-ecs-prerequisites.json | No GitHub provider; service-linked role absent; limited network facts |
| evidence/commands/2026-10-29-stockholm-pricing.json | Official ECS/ECR/CloudWatch regional price-list data |
| evidence/test-results/2026-10-29-container-build.txt | Fargate-ready image build succeeds |
| evidence/test-results/2026-10-29-container-runtime.txt | Healthy/non-root/read-only; app-owned runtime volume verified |
| evidence/test-results/2026-10-29-local-tests.txt | Six tests and dependency check pass |
| evidence/test-results/2026-10-29-trivy.json | Fresh full report; 44 HIGH remain |
| evidence/test-results/2026-10-29-scan-summary.txt | Severity counts and fixable gate result |
| evidence/screenshots/03f-terraform-validation.png | MISSING - proposed filename only |

No raw Terraform plan, AWS credentials, account IDs or real operator IP saved in shareable
plan evidence. AWS account setup screenshots listed above remain MISSING.

### 2026-10-29 Terraform screenshot captured
| Evidence | Status | Result / privacy |
|---|---|---|
| evidence/screenshots/03f-terraform-validation.png | SAVED and visually inspected | Terraform 1.17.1, correct personal path and successful configuration validation; no credentials visible |

This supersedes the earlier MISSING entry for 03f only. Other AWS screenshots remain missing.

### 2026-10-29 redacted AWS billing evidence
| Path | Status | What it proves / limits |
|---|---|---|
| evidence/screenshots/03c-aws-credits-and-expiry.png | Saved, redacted, visually checked | Summary balance shown; both credit rows Expired October 28; usable credit NOT verified; plan not shown |
| evidence/screenshots/03d-aws-budget-overview.png | Saved, redacted, visually checked | USD 1 budget, Healthy and OK; exact alert threshold not shown |
| evidence/screenshots/03g-aws-october-bill.png | Saved, redacted, visually checked | October 2026 estimated bill USD 0.00, Pending; not final cost |
| evidence/commands/2026-10-29-screenshot-redactions.json | Saved | Source/output hashes, redaction rectangles, unchanged-outside-mask verification |

Earlier proposed credits-plan/budget-alert filenames remain unsaved; these actual captures
partially fulfill those evidence needs, without claiming plan/threshold verification.
User authorized opaque redaction; account/credit identifiers and profile picture concealed.
Originals retained outside Git; amount/date/status pixels preserved.
