# Terraform proposal - not applied

Tooling: project-local Terraform 1.17.1; AWS provider 6.71.0 locked in .terraform.lock.hcl.
Workload region eu-north-1; local AWS_PROFILE=tobi-admin uses SSO.
Identity Center stays in us-east-1. Terraform creates no Identity Center configuration.

## Safe validation
From repository root:
```bash
.tools/terraform -chdir=infrastructure/terraform init -backend=false
.tools/terraform -chdir=infrastructure/terraform fmt -check
.tools/terraform -chdir=infrastructure/terraform validate
AWS_PROFILE=tobi-admin .tools/terraform -chdir=infrastructure/terraform plan
```

A plan reads AWS and may contain account/resource identifiers. Raw saved plans/logs belong
only under ignored .cache/. Share sanitized address/action summaries, not raw plans.
No apply, IAM change, image push or destroy without explicit approval.

## Two phases
1. Defaults: foundation only (9 Terraform resources). Private immutable ECR + lifecycle policy,
one-day CloudWatch log group, empty ECS cluster, security group and HTTPS egress,
execution role with one scoped inline policy, empty-permissions task role.
No task, public IP allocation, ingress or GitHub trust by default.
2. After separate approvals and an actual published ECR digest, enable_deployment=true.
Supply real image_digest and demo_client_cidr as a single approved IPv4 /32 in ignored inputs.
This adds task definition, one-task service and restricted ingress.
enable_github_oidc=true separately adds a provider, delivery role and inline policy.
Reuse existing_github_oidc_provider_arn if one exists; never destroy a shared provider.

Planning with both switches gives 15 resources in the current empty account.
The stored full-proposal summary uses a placeholder digest/documentation IP ONLY and is
not executable deployment approval. Generate a fresh plan with verified inputs before applying.
AWS may automatically create its ECS service-linked role if absent; review that prerequisite.

## Ownership and permissions
Execution role pulls only this repository's image and writes only this log group's streams.
Task role has no policies. GitHub role trusts main in TobiOnline/aws-ecs-secure-deployment,
with sts.amazonaws.com audience. No pull-request or other-repository trust.
GitHub can push images to this repo, update only this service and pass only these two roles.
RegisterTaskDefinition requires wildcard resource scope and is region-restricted;
this is an acknowledged IAM scope limitation to review before applying.
A workflow using a GitHub Environment changes the OIDC subject and requires a reviewed
trust-policy change; the current proposal expects branch-subject/manual workflow gating.

After initial creation, CI owns service task-definition revisions (ignore_changes).
Terraform still defines the initial task definition; updating that block alone will not
roll the service. Use the approved delivery/rollback flow and keep image records current.

## Network and runtime
Uses an existing default VPC/subnet; never manages or destroys the default VPC.
Three default subnets, public-IP mapping and an internet-gateway default route were observed.
Confirm the exact chosen subnet's effective route before apply.
One task, Linux x86_64, 0.25 vCPU/0.5 GiB, default 20 GiB ephemeral storage, Fargate 1.4.0.
Temporary HTTP on port 8000 restricted to the operator /32; no domain/TLS or ALB.
No confidential data. Outbound TCP 443 is internet-wide for ECR/S3/CloudWatch.
Public-IP assignment enables outbound image pulls without NAT. It is billable while running.

Read-only root, UID/GID 10001, dropped capabilities and init process are configured.
Fargate does not support the local tmpfs/no-new-privileges settings; no claim of identical
runtime hardening. /app/runtime is a writable task-scoped volume with ownership seeded by
the Dockerfile VOLUME declaration. Volume ownership is tested locally; ECS behavior still
requires deployment evidence. One-day log retention; Container Insights disabled.
ECS circuit breaker enabled; initial deployment has no previous healthy revision to roll back to.

## State and teardown
Local state is ignored and must be backed up securely outside Git. No paid remote backend yet.
Do not delete state to clean up infrastructure. Review destroy plan and obtain explicit approval.
ECR force_delete=false deliberately prevents accidental deletion of stored images.
Deleting ECR images, the repository, logs and any OIDC provider needs reviewed approval;
export sanitized evidence first. Retention does not remove a log group.
Do not remove shared/default infrastructure or Identity Center.

Sources: docs/ARCHITECTURE.md and docs/COST-AND-CLEANUP.md.
