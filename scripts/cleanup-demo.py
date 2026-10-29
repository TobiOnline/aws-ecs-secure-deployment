"""Preview/destroy this project's Terraform resources only, after explicit approval."""
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

root = Path(__file__).resolve().parent.parent
execute = "--execute" in sys.argv
if execute and os.environ.get("APPROVED_DEMO_CLEANUP") != "true":
    raise SystemExit("Explicit destructive-cleanup approval required")
env = os.environ.copy()
env["AWS_PROFILE"] = "tobi-admin"
tf = str(root / ".tools/terraform")
directory = root / "infrastructure/terraform"
plan = root / ".cache/teardown.tfplan"
def aws(*args):
    return json.loads(subprocess.check_output(["aws", *args, "--profile", "tobi-admin", "--region", "eu-north-1", "--output", "json", "--no-cli-pager"], text=True))
with (root / ".cache/teardown-plan.log").open("w") as out:
    subprocess.run([tf, "-chdir=" + str(directory), "plan", "-destroy", "-input=false", "-no-color", "-var-file=" + str(root / ".cache/demo.tfvars.json"), "-out=" + str(plan)], env=env, stdout=out, stderr=subprocess.STDOUT, check=True)
data = json.loads(subprocess.check_output([tf, "-chdir=" + str(directory), "show", "-json", str(plan)], env=env, text=True))
changes = [c for c in data.get("resource_changes", []) if c["mode"] == "managed"]
if not changes or any(c["change"]["actions"] != ["delete"] for c in changes):
    raise SystemExit("Unexpected cleanup plan; stopped")
allowed_addresses = {x["address"] for x in json.loads((root / "evidence/commands/2026-10-29-approved-foundation.json").read_text())["planned_changes"]}
allowed_addresses |= {x["address"] for x in json.loads((root / "evidence/commands/2026-10-29-remaining-deployment-plan.json").read_text())["changes"]}
if any(c["address"] not in allowed_addresses for c in changes):
    raise SystemExit("Unexpected resource outside reviewed project scope")
for c in changes:
    if "aws_vpc." in c["address"] or "aws_subnet." in c["address"] or "service_linked" in c["address"]:
        raise SystemExit("Shared/default infrastructure in destroy plan; stopped")
print("Reviewed project deletions:", len(changes), flush=True)
if not execute:
    raise SystemExit("Preview only. No resources deleted.")
services = aws("ecs", "describe-services", "--cluster", "aws-ecs-secure-deployment", "--services", "aws-ecs-secure-deployment")["services"]
if services and services[0]["status"] == "ACTIVE":
    aws("ecs", "update-service", "--cluster", "aws-ecs-secure-deployment", "--service", "aws-ecs-secure-deployment", "--desired-count", "0")
active_tasks = aws("ecs", "list-tasks", "--cluster", "aws-ecs-secure-deployment", "--desired-status", "RUNNING")["taskArns"]
if active_tasks:
    subprocess.run(["aws", "ecs", "wait", "tasks-stopped", "--cluster", "aws-ecs-secure-deployment", "--tasks", *active_tasks, "--profile", "tobi-admin", "--region", "eu-north-1"], check=True)
subprocess.run(["python3", "scripts/capture-cost-estimate.py"], cwd=root, check=True)
images = aws("ecr", "list-images", "--repository-name", "aws-ecs-secure-deployment")["imageIds"]
# Delete by digest once even if multiple tags reference it.
ids = [{"imageDigest": digest} for digest in sorted({i["imageDigest"] for i in images})]
pending = ids
for attempt in range(5):
    retry = []
    for i in range(0, len(pending), 100):
        result = aws("ecr", "batch-delete-image", "--repository-name", "aws-ecs-secure-deployment", "--image-ids", json.dumps(pending[i:i+100]))
        for failure in result.get("failures", []):
            if failure["failureCode"] == "ImageNotFound":
                continue
            if failure["failureCode"] != "ImageReferencedByManifestList":
                raise SystemExit("Image cleanup failed; stopped before Terraform apply")
            retry.append(failure["imageId"])
    pending = retry
    if not pending:
        break
    time.sleep(2)
if pending:
    raise SystemExit("Referenced image manifests remain; stop and review before Terraform apply")
with (root / ".cache/teardown-apply.log").open("w") as out:
    subprocess.run([tf, "-chdir=" + str(directory), "apply", "-input=false", "-no-color", str(plan)], env=env, stdout=out, stderr=subprocess.STDOUT, check=True)
# CI/fault revisions are outside Terraform ownership; deregister only this project's family.
definitions = aws("ecs", "list-task-definitions", "--family-prefix", "aws-ecs-secure-deployment", "--status", "ACTIVE")["taskDefinitionArns"]
definitions = [arn for arn in definitions if arn.rsplit("/", 1)[-1].split(":")[0] == "aws-ecs-secure-deployment"]
for arn in definitions:
    aws("ecs", "deregister-task-definition", "--task-definition", arn)
summary = {"time": datetime.now(ZoneInfo("Africa/Lagos")).isoformat(), "terraform_resources_destroyed": len(changes), "image_digests_deleted": len(ids), "project_revisions_deregistered": len(definitions), "default_vpc_and_identity_center_preserved": True, "independent_inventory_still_required": True}
(root / "evidence/commands/2026-10-29-teardown.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
