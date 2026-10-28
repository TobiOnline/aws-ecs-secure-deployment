# Roadmap

- [x] Stage 0: personal workspace, baseline docs, private origin, push, accidental-directory absence and screenshot verified. Evidence: evidence/screenshots/00-personal-workspace-and-git.png; baseline ae4dec5, screenshot shows synced commit 42d59c2.
- [x] Stage 1: Flask app, six passing tests, pinned dependencies, live Gunicorn validation and screenshot evidence saved. See evidence/test-results/01-* and evidence/screenshots/01-local-tests-health.png.
- [~] Stage 2: digest-pinned non-root image built; restricted runtime, health and HTTP checks pass; scan remediation and residual findings documented. Evidence: evidence/test-results/02-*. Screenshot pending.
- [ ] Stage 3: approved AWS cost/IAM foundation, private ECR and immutable image evidence.
- [ ] Stage 4: approved temporary ECS deployment, network controls, service health and logs.
- [ ] Stage 5: OIDC CI/CD, passing and blocked workflows, gated deployment evidence.
- [ ] Stage 6: monitoring, reversible incident, diagnosis and verified rollback.
- [ ] Stage 7: security review, case study, release, cleanup verification and cost review.

Each stage remains partial until its validation, documentation, evidence, commit, push and session-state requirements are addressed.
