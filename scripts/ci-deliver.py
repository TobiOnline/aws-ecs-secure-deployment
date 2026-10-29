"""OIDC-only delivery from a manual main-branch GitHub workflow."""
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path

root = Path(__file__).resolve().parent.parent
if os.environ.get("GITHUB_REF") != "refs/heads/main":
    raise SystemExit("Delivery restricted to main")
if not os.environ.get("AWS_ACCESS_KEY_ID") or not os.environ.get("AWS_SESSION_TOKEN"):
    raise SystemExit("Short-lived workflow credentials required")
def aws(*args):
    return json.loads(subprocess.check_output(["aws", *args, "--region", "eu-north-1", "--output", "json", "--no-cli-pager"], text=True))
repo = aws("ecr", "describe-repositories", "--repository-names", "aws-ecs-secure-deployment")["repositories"][0]
tag = os.environ["GITHUB_SHA"] + "-" + os.environ["GITHUB_RUN_NUMBER"]
image = repo["repositoryUri"] + ":" + tag
(root / ".cache").mkdir(exist_ok=True)
with tempfile.TemporaryDirectory(prefix="docker-oidc-", dir=root / ".cache") as auth:
    env = os.environ.copy()
    env["DOCKER_CONFIG"] = auth
    token = subprocess.check_output(["aws", "ecr", "get-login-password", "--region", "eu-north-1"], text=True)
    login = subprocess.run(["docker", "login", "--username", "AWS", "--password-stdin", image.split("/")[0]], input=token, text=True, capture_output=True, env=env, check=False)
    del token
    if login.returncode:
        raise SystemExit("ECR login failed")
    subprocess.run(["docker", "tag", "aws-ecs-secure-deployment:stage3", image], env=env, check=True)
    push = subprocess.run(["docker", "push", image], env=env, capture_output=True, text=True, check=False)
    if push.returncode:
        raise SystemExit("Image push failed")
digest = aws("ecr", "describe-images", "--repository-name", "aws-ecs-secure-deployment", "--image-ids", "imageTag=" + tag)["imageDetails"][0]["imageDigest"]
print("Published tag:", tag, "digest:", digest)
if os.environ.get("APPROVED_DEPLOY") == "true":
    for _ in range(20):
        service = aws("ecs", "describe-services", "--cluster", "aws-ecs-secure-deployment", "--services", "aws-ecs-secure-deployment")["services"][0]
        primary = next(item for item in service["deployments"] if item["status"] == "PRIMARY")
        if primary.get("rolloutState") == "COMPLETED":
            break
        time.sleep(15)
    else:
        raise SystemExit("Existing rollout is not stable; refusing to interrupt it")
    # Use the active healthy revision, not the latest registered family revision:
    # the latest registration may be a failed release being rolled back.
    task = aws("ecs", "describe-task-definition", "--task-definition", service["taskDefinition"])["taskDefinition"]
    allowed = {"family", "taskRoleArn", "executionRoleArn", "networkMode", "containerDefinitions", "volumes", "placementConstraints", "requiresCompatibilities", "cpu", "memory", "runtimePlatform", "ephemeralStorage"}
    task = {key: value for key, value in task.items() if key in allowed}
    task["containerDefinitions"][0]["image"] = repo["repositoryUri"] + "@" + digest
    revision = aws("ecs", "register-task-definition", "--cli-input-json", json.dumps(task))["taskDefinition"]
    aws("ecs", "update-service", "--cluster", "aws-ecs-secure-deployment", "--service", "aws-ecs-secure-deployment", "--task-definition", revision["taskDefinitionArn"])
    subprocess.run(["aws", "ecs", "wait", "services-stable", "--cluster", "aws-ecs-secure-deployment", "--services", "aws-ecs-secure-deployment", "--region", "eu-north-1"], check=True)
    print("Service stable at task revision:", revision["revision"])
