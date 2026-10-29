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
