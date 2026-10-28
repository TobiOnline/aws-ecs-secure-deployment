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
