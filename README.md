# AWS Secure Container Deployment

Personal DevSecOps portfolio project: build, secure, deploy, monitor and tear down a small Flask application on ECS Fargate.

## Status
Stage 0 complete. Stage 1 app validated locally: six tests pass and Gunicorn HTTP checks pass. Screenshot evidence pending. No container or AWS infrastructure deployed.

## Scope
Flask endpoints and tests, a non-root container, private ECR, ECS Fargate, CloudWatch, GitHub Actions with OIDC, incident recovery and verified cleanup. No ALB, NAT gateway, EKS or Terraform in the initial scope.

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
