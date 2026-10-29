"""Run the trusted manual main workflow using a verified ephemeral local runner."""
import argparse
import hashlib
import io
import os
import subprocess
import tarfile
import time
import urllib.request
from pathlib import Path

root = Path(__file__).resolve().parent.parent
parser = argparse.ArgumentParser()
parser.add_argument("--failure", action="store_true")
parser.add_argument("--deliver", action="store_true")
parser.add_argument("--deploy", action="store_true")
parser.add_argument("--rerun")
args = parser.parse_args()
if args.deploy and not args.deliver:
    raise SystemExit("--deploy requires --deliver")
runner = root / ".cache/actions-runner"
if not (runner / "bin/Runner.Listener").exists():
    url = "https://github.com/actions/runner/releases/download/v2.338.2/actions-runner-linux-x64-2.338.2.tar.gz"
    expected = "baebf204307bac6193480852732f0aba2ae97b6c5597c244f4d5558390147c40"
    with urllib.request.urlopen(url, timeout=120) as response:
        payload = response.read()
    if hashlib.sha256(payload).hexdigest() != expected:
        raise SystemExit("Runner archive checksum mismatch")
    runner.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
        archive.extractall(runner, filter="data")
if (runner / ".runner").exists():
    raise SystemExit("A configured runner already exists; verify its job before replacing it")
env = os.environ.copy()
env["DOTNET_SYSTEM_GLOBALIZATION_INVARIANT"] = "1"
env["AWS_EC2_METADATA_DISABLED"] = "true"
for key in ["AWS_PROFILE", "AWS_ACCESS_KEY_ID", "AWS_SECRET_ACCESS_KEY", "AWS_SESSION_TOKEN"]:
    env.pop(key, None)
repo = "TobiOnline/aws-ecs-secure-deployment"
token = subprocess.check_output(["gh", "api", "-X", "POST", "repos/" + repo + "/actions/runners/registration-token", "--jq", ".token"], text=True).strip()
with (root / ".cache/runner-config.log").open("w") as out:
    configured = subprocess.run([str(runner / "bin/Runner.Listener"), "configure", "--url", "https://github.com/" + repo, "--token", token, "--name", "ecs-demo-" + str(int(time.time())), "--labels", "ecs-demo", "--unattended", "--ephemeral", "--disableupdate"], cwd=runner, env=env, stdout=out, stderr=subprocess.STDOUT, check=False)
del token
if configured.returncode:
    raise SystemExit("Runner configuration failed; inspect private .cache/runner-config.log")
with (root / ".cache/runner-console-current.log").open("w") as out:
    process = subprocess.Popen([str(runner / "bin/Runner.Listener"), "run"], cwd=runner, env=env, stdout=out, stderr=subprocess.STDOUT, start_new_session=True)
(root / ".cache/runner-pid").write_text(str(process.pid))
if args.rerun:
    command = ["gh", "run", "rerun", args.rerun, "--failed", "--repo", repo]
else:
    command = ["gh", "workflow", "run", "ci.yml", "--repo", repo, "--ref", "main", "-f", "demonstrate_failure=" + str(args.failure).lower(), "-f", "deliver=" + str(args.deliver).lower(), "-f", "deploy=" + str(args.deploy).lower()]
result = subprocess.run(command, cwd=root, capture_output=True, text=True, check=False)
if result.returncode:
    process.terminate()
    raise SystemExit("Dispatch failed; inspect repository runner registration before retrying")
print("Ephemeral runner started and workflow requested. Track it with gh run list.")
