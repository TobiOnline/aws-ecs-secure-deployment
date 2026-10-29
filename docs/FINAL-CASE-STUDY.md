# Secure, short-lived Flask deployment on ECS Fargate

## Problem
Build a small cloud deployment that can be explained, reproduced and removed without
leaving an idle workload or storing long-lived AWS credentials in GitHub.

## Architecture
A Flask app exposes JSON / and /health endpoints. Gunicorn serves it from a digest-pinned
Python slim image, with UID 10001, a read-only root and an app-owned temporary volume.
Terraform defines private ECR, ECS Fargate, scoped IAM, network rules, one-day logs and a CPU alarm.
The Stockholm service uses the existing default VPC, one public subnet and operator-only /32
ingress. No load balancer, NAT gateway, database or custom domain.

## Build and security
Six automated tests cover both endpoints, 404, rejected writes and generic 500 responses.
The manual main-branch GitHub workflow runs lint, tests, history secret scanning, dependency
audit and image build/runtime/Trivy checks. Actions and scanner assets are pinned.
The deliberately failing test run 40862041799 blocks all later build/credentials/delivery steps.
A real passing run, 40864000531, published through OIDC with no static AWS keys.

Initial scan remediation removed pip-vendored runtime tooling and five fixable HIGH entries.
The refreshed scan still contains 44 HIGH, 58 MEDIUM, 61 LOW and one UNKNOWN finding;
none of its HIGH/CRITICAL findings lists an available fix. This was an explicitly accepted
temporary-demo risk, not production security approval. ECR BASIC scan returned
UnsupportedImageTypeException for the published artifact; local Trivy findings are the evidence.

## Operational validation
Initial live revision 1 reached HEALTHY/RUNNING and both endpoints returned HTTP 200.
CloudWatch recorded application logs; CPU alarm was OK with an 80 percent/two-minute threshold.
It is a console-only alarm with no notification action, and did not demonstrate an alert on
deployment failure. The deployment incident is detected through ECS rollout/task state and logs.

A controlled revision 2 exited with code 1. During the incident, revision 1 remained running
while ECS recorded failed replacement tasks. The circuit breaker automatically restored
revision 1 between 12:20 and 12:25 Africa/Lagos on October 29. Recovery evidence confirms HTTP 200
and healthy task state. No public downtime is claimed.

Final CI-driven task-revision delivery and teardown are still in progress at this draft checkpoint.
The final section must be updated with observed results before claiming completion.

## Failures and lessons
- New GitHub repositories use immutable OIDC subjects. A legacy name-only trust condition
  denied assumption. GitHub configuration plus CloudTrail identified the exact subject;
  the correction retained exact repository/main trust without wildcard expansion.
- A root-owned scanner cache broke a reused runner checkout. Scanner runs now use the host
  UID/GID, isolated cache and unique ephemeral workspaces.
- A delivery pipeline must use the active healthy task definition, not the latest registered
  family revision, because the latest registration can be the failed release.
- Fargate temporary-volume behavior differs from local tmpfs. Dockerfile volume ownership
  was prepared and checked locally; actual Fargate endpoints proved the resulting server runs.
- The account's expired credits could not be treated as usable balance. A read-only API
  confirmed paid status/zero Free Tier credits. Owner explicitly accepted a paid under-USD-1
  target with no guaranteed cap, a short run and prompt teardown.

## Evidence and limits
All evidence paths are indexed in EVIDENCE-INDEX.md. Historical local screenshots are saved.
Live cloud/CI screenshots remain missing: browser automation stopped at a URL-confidence
safety boundary, and no screenshot was fabricated. Sanitized API/HTTP results, run URLs,
image digests and Git history supply the current reproducible evidence.
MFA setup was owner-reported and is separate from this workload's deployment controls.

This is a learning demo: no TLS/custom domain, availability guarantee, production risk
acceptance, external alarm notifications or enforced AWS spending cap. Final billing is delayed.
