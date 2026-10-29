"""Approved reversible bad-release simulation; never invoke without authorization."""
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

if os.environ.get("APPROVED_REVERSIBLE_FAULT") != "true":
    raise SystemExit("Explicit fault/recovery authorization required")
root = Path(__file__).resolve().parent.parent
def aws(*args):
    return json.loads(subprocess.check_output(["aws", *args, "--profile", "tobi-admin", "--region", "eu-north-1", "--output", "json", "--no-cli-pager"], text=True))
def service():
    return aws("ecs", "describe-services", "--cluster", "aws-ecs-secure-deployment", "--services", "aws-ecs-secure-deployment")["services"][0]
started = datetime.now(ZoneInfo("Africa/Lagos")).isoformat()
good = service()["taskDefinition"]
task = aws("ecs", "describe-task-definition", "--task-definition", good)["taskDefinition"]
allowed = {"family", "taskRoleArn", "executionRoleArn", "networkMode", "containerDefinitions", "volumes", "placementConstraints", "requiresCompatibilities", "cpu", "memory", "runtimePlatform", "ephemeralStorage"}
task = {key: value for key, value in task.items() if key in allowed}
task["containerDefinitions"][0]["command"] = ["python", "-c", "raise SystemExit('controlled deployment fault for recovery evidence')"]
bad = aws("ecs", "register-task-definition", "--cli-input-json", json.dumps(task))["taskDefinition"]
aws("ecs", "update-service", "--cluster", "aws-ecs-secure-deployment", "--service", "aws-ecs-secure-deployment", "--task-definition", bad["taskDefinitionArn"])
print("Controlled failing revision registered:", bad["revision"], flush=True)
observed = False
automatic = False
for attempt in range(28):
    current = service()
    observed = observed or any(d.get("rolloutState") == "FAILED" for d in current["deployments"])
    observed = observed or any("failed" in e["message"].lower() or "circuit breaker" in e["message"].lower() for e in current.get("events", [])[:8])
    primary = next(d for d in current["deployments"] if d["status"] == "PRIMARY")
    if primary["taskDefinition"] == good and primary.get("rolloutState") == "COMPLETED":
        automatic = True
        break
    if attempt % 2 == 0:
        print("Waiting for circuit breaker/recovery:", attempt + 1, flush=True)
    time.sleep(15)
if not automatic:
    aws("ecs", "update-service", "--cluster", "aws-ecs-secure-deployment", "--service", "aws-ecs-secure-deployment", "--task-definition", good)
    subprocess.run(["aws", "ecs", "wait", "services-stable", "--cluster", "aws-ecs-secure-deployment", "--services", "aws-ecs-secure-deployment", "--profile", "tobi-admin", "--region", "eu-north-1"], check=True)
current = service()
assert current["taskDefinition"] == good and current["runningCount"] == 1
summary = {"started": started, "ended": datetime.now(ZoneInfo("Africa/Lagos")).isoformat(), "good_revision": int(good.rsplit(":", 1)[1]), "controlled_bad_revision": bad["revision"], "failure_observed_in_service": observed, "automatic_rollback": automatic, "known_good_restored": True, "running": current["runningCount"], "public_downtime_claimed": False}
(root / "evidence/commands/2026-10-29-incident-recovery.json").write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps(summary, indent=2))
subprocess.run(["python3", "scripts/collect-demo-evidence.py", "recovered-service"], cwd=root, check=True)
