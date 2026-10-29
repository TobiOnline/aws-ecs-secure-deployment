"""Build first, then run: python3 scripts/verify-container.py [image]."""
import json
import subprocess
import sys
import time
import urllib.request

image = sys.argv[1] if len(sys.argv) > 1 else "aws-ecs-secure-deployment:stage3"
def docker(*args):
    return subprocess.check_output(["docker", *args], text=True).strip()

metadata = json.loads(docker("image", "inspect", image))[0]
assert metadata["Config"]["User"] == "10001:10001"
print("Image:", image, flush=True)
print("Image ID:", metadata["Id"], flush=True)
print("Size bytes:", metadata["Size"], flush=True)
print("Configured non-root user:", metadata["Config"]["User"], flush=True)
container = docker(
    "run", "-d", "--read-only", "--cap-drop=ALL",
    "--security-opt=no-new-privileges:true", "--pids-limit=100",
    "--memory=128m", "--cpus=0.5",
    "-p", "127.0.0.1::8000", image,
)
try:
    endpoint = docker("port", container, "8000/tcp")
    for _ in range(60):
        info = json.loads(docker("inspect", container))[0]
        if not info["State"]["Running"]:
            raise RuntimeError(docker("logs", container))
        if info["State"]["Health"]["Status"] == "healthy":
            break
        time.sleep(1)
    else:
        raise RuntimeError("Container never became healthy")
    print("Container health: healthy", flush=True)
    print("Runtime UID:", docker("exec", container, "id", "-u"), flush=True)
    owner = docker("exec", container, "stat", "-c", "%u:%g", "/app/runtime")
    assert owner == "10001:10001"
    print("Task-style writable volume owner:", owner, flush=True)
    assert docker("exec", container, "id", "-u") == "10001"
    for path, expected in [("/", {"service": "aws-ecs-secure-deployment", "status": "ok"}), ("/health", {"status": "healthy"})]:
        with urllib.request.urlopen("http://" + endpoint + path, timeout=3) as response:
            body = json.load(response)
            assert response.status == 200 and body == expected
            print(f"GET {path} -> HTTP {response.status} {json.dumps(body, sort_keys=True)}", flush=True)
    print("Read-only root filesystem; all capabilities dropped; no new privileges.", flush=True)
finally:
    docker("rm", "-fv", container)
    print("Temporary test container removed.", flush=True)
