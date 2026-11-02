# AWS Secure Container Deployment

Personal DevSecOps portfolio project: build, secure, deploy, monitor and tear down a small Flask application on ECS Fargate.

## Status
Cloud demonstration completed and torn down on October 29, 2026:
six app tests, a non-root container, real failing/passing security workflows, OIDC image
publication, healthy ECS revision 3, CloudWatch logs/CPU alarm and automatic rollback from
a controlled failed release were verified. All 16 Terraform-managed resources were removed;
independent inventory and empty state confirmed. No demo service remains online.

Conservative compute + IPv4 estimate: USD 0.01150609, excluding logs/storage/alarm/transfer/tax.
Billing screenshots received November 2 show October account cost USD 0.23 and November
month-to-date USD 0.02 (USD 0.25 combined observed account cost, below the USD 1 target).
These are dashboard figures, not a final invoice or project-attributed service breakdown.
Technical work and documentation handoff are complete. CI and billing screenshots are saved;
other live cloud screenshots remain missing, supported by sanitized API evidence instead.
Strict original acceptance remains 6/7 (86% rounded) because final invoice attribution and
full visual evidence are unresolved. See docs/EVIDENCE-INDEX.md and the November 2 handoff.

## Scope
Flask endpoints and tests, a non-root container, private ECR, ECS Fargate, CloudWatch, GitHub Actions with OIDC, incident recovery and verified cleanup. No ALB, NAT gateway or EKS in the initial scope. Terraform was added by the owner's October 29 request. Version 1.17.1 and the locked AWS provider describe the deployed-and-removed infrastructure.

See docs/SESSION-STATE.md for the verified handoff and docs/ROADMAP.md for acceptance gates.

## Run locally (WSL/Linux)
Tested on Python 3.14.4. Runtime and development dependencies, including transitive packages, are pinned.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
bash scripts/verify-local.sh
.venv/bin/gunicorn --bind 127.0.0.1:8000 --workers 1 --access-logfile - 'app:create_app()'
```

In another terminal:
```bash
curl -i http://127.0.0.1:8000/
curl -i http://127.0.0.1:8000/health
```

Stop the server with Ctrl+C. The app returns JSON for success and HTTP errors.
Health is process liveness only: there are no external dependencies to probe.
The server binds localhost for local checks; container networking will be configured in Stage 2.
Gunicorn writes access/error logs to stdout/stderr; do not place sensitive data in request URLs.
Unexpected errors return a generic JSON response; internal diagnostics remain in server logs.

## Dependency sources
Versions were resolved from official PyPI metadata and tested locally:
[Flask](https://pypi.org/project/Flask/),
[Gunicorn](https://pypi.org/project/gunicorn/),
[pytest](https://pypi.org/project/pytest/).
Pins provide repeatable version selection; vulnerability review remains a separate checkpoint.

## Container verification
Docker Desktop WSL integration must be enabled for Ubuntu.

```bash
docker build -t aws-ecs-secure-deployment:stage3 .
python3 scripts/verify-container.py
bash scripts/scan-image.sh
```

The verification script starts a temporary container bound only to localhost, checks health,
UID 10001 and both endpoints, then removes the container. It tests a read-only filesystem,
dropped Linux capabilities and no-new-privileges. An app-owned runtime volume is checked locally to prepare for Fargate. Fargate used read-only root, UID 10001 and dropped capabilities; local no-new-privileges is not a supported Fargate setting. See docs/SECURITY.md for the differences.
The image exposes port 8000, logs to stdout/stderr and runs Gunicorn with one worker.

The base is the official Python 3.14 slim trixie image pinned by digest (container Python
3.14.10 in this build; host development Python 3.14.4). No compiler stage is needed:
dependencies install as wheels, and pip is removed after installation. Docker build context
allows only the application and runtime lock, excluding credentials, evidence and Git.

The scan uses the official Trivy image pinned in .trivy-image. It scans an exported image
without Docker-socket access. Large image archives and vulnerability DB cache remain ignored
under .cache/. The gate fails on fixable HIGH/CRITICAL findings; a passing gate does not
mean there are no vulnerabilities. Review the full report and security notes before deployment.

## Infrastructure and replay
See [architecture](docs/ARCHITECTURE.md) and [Terraform instructions](infrastructure/terraform/README.md). Run bash scripts/verify-infrastructure.sh for local validation. Terraform state, plans and tooling are ignored; .terraform.lock.hcl is committed. The implementation was applied, validated and destroyed. Recreating it incurs charges and requires renewed cost/exposure approval; see infrastructure/terraform/README.md and docs/RUNBOOK.md.

## Demonstrated delivery
- [Intentional test failure blocks delivery](https://github.com/TobiOnline/aws-ecs-secure-deployment/actions/runs/40862041799)
- [Passing security/OIDC publication](https://github.com/TobiOnline/aws-ecs-secure-deployment/actions/runs/40864000531)
- [Successful end-to-end ECS revision delivery](https://github.com/TobiOnline/aws-ecs-secure-deployment/actions/runs/40866951465)

Read docs/FINAL-CASE-STUDY.md for outcomes, failures, limitations and cost/cleanup evidence.
