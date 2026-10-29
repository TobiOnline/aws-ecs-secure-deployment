# Cost and cleanup

No AWS resources created in this session. Account identity, region, free-tier/credit eligibility, pricing and actual charges are unverified.

Before provisioning: obtain explicit approval for exact resources, region, expected charges, exposure and cleanup window; verify current pricing and account eligibility; configure budget/billing alerts. Alerts do not cap spending.

The empty accidental Webforx directory remains untouched pending explicit cleanup confirmation.

Stage 2: local Docker pulls/build/scan only; no AWS resources created. Temporary runtime containers removed by verification script. Local images and ignored .cache files retained for reproduction.

## 2026-10-29 account baseline - supersedes earlier setup notes

User reports paid account TOBI with USD 100 promotional credits initially available.
Remaining balance, expiry and actual charges not yet independently verified.
Workload region eu-north-1; Identity Center region us-east-1.
The earlier N. Virginia price illustration is not a Stockholm deployment estimate;
verify current eu-north-1 prices immediately before proposing provisioning.

Read-only API checks found one Zero-named COST budget with USD 1 configured amount
and one notification rule. Budget name is not a hard cap; recipients, threshold, credit
filters and actual delivery remain unverified. USD 5 was an earlier suggestion,
not an approved spend allowance.

No ECS clusters, ECR repositories, EC2 instances, modern or classic load balancers found
in Stockholm; one default VPC exists. Not an all-region/all-service audit or proof of no bill.
Identity Center/account setup is separate from project workload provisioning.
No AWS resources provisioned, changed or deleted by this audit.
Local verification created a temporary container and removed it after successful checks.

Historical correction: accidental Webforx project path was verified absent on October 28;
the earlier paragraph saying it remained untouched awaiting confirmation is obsolete.
Future teardown requires explicit approval and verification against Terraform state plus
independent AWS inventory, with delayed billing reviewed separately.

## 2026-10-29 Stockholm proposal - not applied

Official public price-list snapshots saved in evidence/commands/2026-10-29-stockholm-pricing.json.
Rates below are list prices, not proof credits apply, a quote or a spending cap.

| Component | Rate / assumption |
|---|---|
| Fargate Linux x86 CPU | USD 0.0445 per vCPU-hour |
| Fargate memory | USD 0.0049 per GiB-hour |
| One task (0.25 vCPU + 0.5 GiB) | USD 0.013575 per hour |
| One public IPv4 | USD 0.005 per hour (AWS VPC pricing) |
| Combined task + IPv4 | USD 0.018575 per task-hour |
| ECR standard storage | USD 0.10 per GB-month |
| CloudWatch standard log ingestion | USD 0.54 per GB |
| CloudWatch log storage | USD 0.028 per GB-month |
| Optional future standard alarm | USD 0.10 per metric-month; not currently configured |

Illustration only: four single-task hours = USD 0.0743 compute/IP. Allowing 1 GB-month
ECR storage, 0.1 GB ingested logs and 0.1 GB-month stored logs brings that illustration
to about USD 0.2311, excluding tax, transfer and any other services. Rolling updates may
temporarily run two tasks; failed/restarted tasks also consume billable time.
No free tier, promotional offset, tax exemption or zero data-transfer cost is assumed.

Proposal: USD 1 total project usage allowance INCLUDING credit consumption, subject to user
approval and verified remaining credits. Not an enforced cap. Do not equate a budget alert
with automatic shutdown; billing/alerts can lag. Current allowance is NOT yet approved.

Phase 1 foundation plan: 9 Terraform resources, including scoped IAM roles/policy, empty
ECR/cluster/log group and no task/public endpoint. AWSServiceRoleForECS is absent; AWS may
create this account-wide ECS service-linked role automatically on initial ECS usage.
That implicit IAM prerequisite must be included in approval and must not be torn down
if shared. Optional GitHub trust would add three Terraform resources under separate approval.

Phase 2 deployment: actual immutable image digest and approved operator /32 required; planned
one task, temporarily two during updates; no ALB, NAT gateway or custom backend.
Image build/scan completed locally; no image pushed. Foundation and service must be replanned
after input changes and immediately before approved apply.

Cleanup: stop/remove service first, retain sanitized evidence, review Terraform destroy plan,
obtain explicit destructive approval, delete reviewed ECR images before protected repository,
and remove project log group/roles/security group/cluster. Default VPC/Identity Center remain.
Monitor delayed billing afterward. No automatic resource deletion or timer has been configured.

Sources:
- https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonECS/current/eu-north-1/index.json
- https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonECR/current/eu-north-1/index.json
- https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonCloudWatch/current/eu-north-1/index.json
- https://aws.amazon.com/vpc/pricing/
