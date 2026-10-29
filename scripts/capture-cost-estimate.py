"""Conservative compute/IP estimate from observed ECS task lifetimes; not an AWS bill."""
import hashlib
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

root = Path(__file__).resolve().parent.parent
def aws(*args):
    return json.loads(subprocess.check_output(["aws", *args, "--profile", "tobi-admin", "--region", "eu-north-1", "--output", "json", "--no-cli-pager"], text=True))
arns = aws("ecs", "list-tasks", "--cluster", "aws-ecs-secure-deployment", "--desired-status", "STOPPED")["taskArns"]
arns += aws("ecs", "list-tasks", "--cluster", "aws-ecs-secure-deployment", "--desired-status", "RUNNING")["taskArns"]
arns = sorted(set(arns))
tasks = aws("ecs", "describe-tasks", "--cluster", "aws-ecs-secure-deployment", "--tasks", *arns)["tasks"] if arns else []
rows = []
for task in tasks:
    if task["taskDefinitionArn"].rsplit("/", 1)[-1].split(":")[0] != "aws-ecs-secure-deployment":
        continue
    start = datetime.fromisoformat(task["createdAt"])
    end = datetime.fromisoformat(task["stoppedAt"]) if task.get("stoppedAt") else datetime.now(UTC)
    seconds = max(60, (end - start).total_seconds())
    vcpu = int(task.get("cpu", "256")) / 1024
    memory = int(task.get("memory", "512")) / 1024
    rate = vcpu * 0.0445 + memory * 0.0049 + 0.005
    rows.append({"task_reference_hash": hashlib.sha256(task["taskArn"].encode()).hexdigest()[:12], "revision": int(task["taskDefinitionArn"].rsplit(":", 1)[1]), "created": task["createdAt"], "stopped": task.get("stoppedAt"), "status": task["lastStatus"], "conservative_seconds": round(seconds, 2), "estimated_compute_ipv4_usd": round(seconds / 3600 * rate, 8)})
result = {"date": "2026-10-29", "region": "eu-north-1", "tasks": rows, "conservative_compute_ipv4_estimate_usd": round(sum(r["estimated_compute_ipv4_usd"] for r in rows), 8), "not_final_bill": True, "assumptions": "Charges estimated for entire created-to-stopped interval (conservative versus pull start); minimum 60 seconds per task; no credits assumed. Excludes ECR/logs/alarm/transfer/tax. Actual billing can lag."}
(root / "evidence/commands/2026-10-29-task-cost-estimate.json").write_text(json.dumps(result, indent=2) + "\n")
print("Observed task count:", len(rows))
print("Conservative compute+IPv4 estimate USD:", result["conservative_compute_ipv4_estimate_usd"])
