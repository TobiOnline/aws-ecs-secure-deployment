# Roadmap

- [x] Stage 0: personal workspace, baseline docs, private origin, push, accidental-directory absence and screenshot verified. Evidence: evidence/screenshots/00-personal-workspace-and-git.png; baseline ae4dec5, screenshot shows synced commit 42d59c2.
- [~] Stage 1: app factory and six tests validated; pinned dependencies and live Gunicorn checks complete (evidence/test-results/01-local-tests.txt, 01-live-http.txt). Screenshot pending. Remaining acceptance scope: Flask / and /health, success/failure tests, pinned compatible dependencies, local endpoint checks, docs and Git evidence.
- [ ] Stage 2: non-root container, build/runtime/health validation, vulnerability scan and image evidence.
- [ ] Stage 3: approved AWS cost/IAM foundation, private ECR and immutable image evidence.
- [ ] Stage 4: approved temporary ECS deployment, network controls, service health and logs.
- [ ] Stage 5: OIDC CI/CD, passing and blocked workflows, gated deployment evidence.
- [ ] Stage 6: monitoring, reversible incident, diagnosis and verified rollback.
- [ ] Stage 7: security review, case study, release, cleanup verification and cost review.

Each stage remains partial until its validation, documentation, evidence, commit, push and session-state requirements are addressed.
