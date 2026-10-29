# AWS Secure Container Deployment

Personal DevSecOps portfolio project: build, secure, deploy, monitor and tear down a small Flask application on ECS Fargate.

## Status
Stages 0-2 complete with local screenshots and runtime/scan evidence. AWS CLI/SSO and Stockholm inventory verified on October 29; Stage 3 is partial. No project workload deployed. See docs/SESSION-STATE.md for the current dated handoff and docs/SECURITY.md for remaining image findings.

## Scope
Flask endpoints and tests, a non-root container, private ECR, ECS Fargate, CloudWatch, GitHub Actions with OIDC, incident recovery and verified cleanup. No ALB, NAT gateway or EKS in the initial scope. Terraform was added by the owner's October 29 request; installation and infrastructure implementation remain pending.

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
docker build -t aws-ecs-secure-deployment:stage2 .
python3 scripts/verify-container.py
bash scripts/scan-image.sh
```

The verification script starts a temporary container bound only to localhost, checks health,
UID 10001 and both endpoints, then removes the container. It tests a read-only filesystem,
dropped Linux capabilities and no-new-privileges. Those runtime settings must also be
applied explicitly in future deployments; the Dockerfile alone does not enforce them.
The image exposes port 8000, logs to stdout/stderr and runs Gunicorn with one worker.

The base is the official Python 3.14 slim trixie image pinned by digest (container Python
3.14.10 in this build; host development Python 3.14.4). No compiler stage is needed:
dependencies install as wheels, and pip is removed after installation. Docker build context
allows only the application and runtime lock, excluding credentials, evidence and Git.

The scan uses the official Trivy image pinned in .trivy-image. It scans an exported image
without Docker-socket access. Large image archives and vulnerability DB cache remain ignored
under .cache/. The gate fails on fixable HIGH/CRITICAL findings; a passing gate does not
mean there are no vulnerabilities. Review the full report and security notes before deployment.
