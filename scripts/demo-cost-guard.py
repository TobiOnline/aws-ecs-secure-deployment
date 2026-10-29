"""Finite local failsafe: scale the approved demo service to zero after 45 minutes."""
import json
import subprocess
import time
from pathlib import Path

root = Path(__file__).resolve().parent.parent
deadline = time.monotonic() + 2700
seen = False
while time.monotonic() < deadline:
    result = subprocess.run(["aws", "ecs", "describe-services", "--cluster", "aws-ecs-secure-deployment", "--services", "aws-ecs-secure-deployment", "--profile", "tobi-admin", "--region", "eu-north-1", "--output", "json", "--no-cli-pager"], capture_output=True, text=True, check=False)
    if result.returncode == 0:
        services = json.loads(result.stdout).get("services", [])
        active = any(service["status"] == "ACTIVE" for service in services)
        if seen and not active:
            (root / ".cache/cost-guard-status").write_text("Service removed; guard exited")
            raise SystemExit(0)
        seen = seen or active
    time.sleep(30)
if seen:
    result = subprocess.run(["aws", "ecs", "update-service", "--cluster", "aws-ecs-secure-deployment", "--service", "aws-ecs-secure-deployment", "--desired-count", "0", "--profile", "tobi-admin", "--region", "eu-north-1", "--no-cli-pager"], capture_output=True, text=True, check=False)
    (root / ".cache/cost-guard-status").write_text("Deadline reached; scale-to-zero " + ("succeeded" if result.returncode == 0 else "failed; manual cleanup required"))
else:
    (root / ".cache/cost-guard-status").write_text("Deadline reached; no service observed")
