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
