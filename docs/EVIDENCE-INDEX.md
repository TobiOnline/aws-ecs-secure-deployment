# Evidence index

| Milestone | Evidence | Date | Result | Privacy |
|---|---|---|---|---|
| Stage 0 preflight | Observed command outputs in Codex chat | 2026-10-28 | Personal project absent before creation; accidental directory empty; tool/auth blockers observed | No credentials captured |
| Stage 0 screenshot | evidence/screenshots/00-personal-workspace-and-git.png | 2026-10-28 | Correct personal path; clean main matching origin/main at 42d59c2 | Inspected: no credentials visible; username/hostname visible |
| Stage 0 commit/push | Local baseline ae4dec5; remote main 344d706 | 2026-10-28 | Private repository and matching local/remote main verified | Inspect remote before sharing |

Repository: https://github.com/TobiOnline/aws-ecs-secure-deployment (PRIVATE, verified 2026-10-28). Screenshot captured and inspected.

| Accidental-directory resolution | WSL test confirmed path absent (Codex command output) | 2026-10-28 | Already absent at cleanup recheck; no deletion needed | No secrets |
