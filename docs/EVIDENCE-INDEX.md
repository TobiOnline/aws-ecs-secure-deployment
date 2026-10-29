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
