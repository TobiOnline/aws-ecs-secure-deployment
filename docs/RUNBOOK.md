# Demo operations runbook

Workload: eu-north-1, project aws-ecs-secure-deployment. Use local SSO profile tobi-admin.
No credentials or account IDs in evidence. Paid usage target under USD 1, not a guaranteed cap.

## Health and logs
After approved deployment:
```bash
python3 scripts/collect-demo-evidence.py deployment
```
This captures service/task health, actual HTTP results, selected sanitized CloudWatch messages
and CPU-alarm state. It omits the public endpoint from shared evidence. The local endpoint
is stored only in ignored .cache/demo-endpoint.

## Delivery
Manual Secure delivery workflow on main only. Default validates without AWS access.
A deliberate failing-test input must block before credentials/image delivery.
Deliver/deploy inputs are enabled only under explicit approved cloud scope.
OIDC role has short-lived credentials; never store static AWS access keys.

## Recovery
Record known-good task revision and digest before a reversible fault.
Use a controlled failing task revision; preserve ECS rollout evidence and restore known-good
revision if circuit breaker does not recover. First deployment has no prior healthy revision.
Do not delete Identity Center, shared IAM roles or default networking during incident handling.

## Cost and teardown
Do not leave a desired-count=1 service overnight. Stopping a service-owned task alone is
insufficient: ECS replaces it. Under approved teardown, delete/scale down the service first,
preserve logs/evidence, delete only reviewed project images, then apply reviewed Terraform destroy.
Retain local state until independent post-destroy inventory succeeds. Billing may lag.

## Reproduce tools and workflow
From a fresh clone in WSL/Linux x86_64, inspect scripts before execution:
```bash
python3 scripts/install-terraform.py
.tools/terraform -chdir=infrastructure/terraform init
bash scripts/verify-infrastructure.sh
```
Installer verifies the pinned official release archive hash. Use SSO and obtain explicit
resource/IAM/cost approval before applying the reviewed Terraform configuration.

The manual workflow uses an ephemeral local runner to avoid hosted-compute charges:
```bash
python3 scripts/run-local-ci.py
python3 scripts/run-local-ci.py --failure
```
Only trusted main code is eligible; never accept untrusted PR jobs on this host.
The script downloads the checksum-pinned official runner if absent and uses a fresh workspace.
An ephemeral registration disappears after one job. The host is not a security sandbox.
GitHub token needs repository runner/workflow access; do not paste it into scripts.
Deliver/deploy flags require the corresponding cloud approvals and configured OIDC role identifier.

After approved deployment and incident evidence:
```bash
APPROVED_REVERSIBLE_FAULT=true python3 scripts/simulate-recovery.py
APPROVED_DEMO_CLEANUP=true python3 scripts/cleanup-demo.py --execute
```
Cleanup previews exact project deletes, scales service down, removes reviewed image manifests,
destroys Terraform-managed project resources and deregisters exact-family task revisions.
It preserves default/shared account infrastructure. Verify independent inventory afterward.
Local 45-minute guard is a fallback only; it does not survive every host/network failure or cap bills.
