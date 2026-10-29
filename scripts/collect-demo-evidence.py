"""Collect sanitized ECS/CloudWatch/HTTP evidence using the local SSO profile."""
import json
import re
import subprocess
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

root = Path(__file__).resolve().parent.parent
label = sys.argv[1] if len(sys.argv) > 1 else "deployment"
if not re.fullmatch(r"[a-z0-9-]+", label):
    raise SystemExit("Use a simple evidence label")
def aws(*args):
    return json.loads(subprocess.check_output(["aws", *args, "--profile", "tobi-admin", "--region", "eu-north-1", "--output", "json", "--no-cli-pager"], text=True))
service = aws("ecs", "describe-services", "--cluster", "aws-ecs-secure-deployment", "--services", "aws-ecs-secure-deployment")["services"][0]
tasks = aws("ecs", "list-tasks", "--cluster", "aws-ecs-secure-deployment", "--service-name", "aws-ecs-secure-deployment")["taskArns"]
result = {"time": datetime.now(ZoneInfo("Africa/Lagos")).isoformat(), "region": "eu-north-1", "service_status": service["status"], "desired": service["desiredCount"], "running": service["runningCount"], "pending": service["pendingCount"], "deployments": [{"status": d["status"], "revision": int(d["taskDefinition"].rsplit(":", 1)[1]), "rollout": d.get("rolloutState")} for d in service["deployments"]]}
if tasks:
    details = aws("ecs", "describe-tasks", "--cluster", "aws-ecs-secure-deployment", "--tasks", *tasks)["tasks"]
    result["task_health"] = [{"status": t["lastStatus"], "health": t.get("healthStatus"), "container_health": [c.get("healthStatus") for c in t["containers"]]} for t in details]
    eni = next(d["value"] for a in details[0]["attachments"] for d in a.get("details", []) if d["name"] == "networkInterfaceId")
    interface = aws("ec2", "describe-network-interfaces", "--network-interface-ids", eni)["NetworkInterfaces"][0]
    address = interface.get("Association", {}).get("PublicIp")
    if address:
        result["http"] = {}
        for path in ["/", "/health"]:
            with urllib.request.urlopen("http://" + address + ":8000" + path, timeout=15) as response:
                result["http"][path] = {"status": response.status, "body": json.load(response)}
        (root / ".cache" / "demo-endpoint").write_text("http://" + address + ":8000")
logs = aws("logs", "filter-log-events", "--log-group-name", "/ecs/aws-ecs-secure-deployment", "--limit", "20")
result["log_messages"] = [re.sub(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", "[IP]", event["message"]) for event in logs.get("events", [])]
result["alarm"] = [{"state": alarm["StateValue"], "metric": alarm.get("MetricName"), "threshold": alarm.get("Threshold")} for alarm in aws("cloudwatch", "describe-alarms", "--alarm-names", "ecs-demo-high-cpu")["MetricAlarms"]]
target = root / "evidence" / "commands" / ("2026-10-29-" + label + ".json")
target.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: v for k, v in result.items() if k != "log_messages"}, indent=2))
print("CloudWatch messages captured:", len(result["log_messages"]))
