"""Install only the pinned official Gitleaks binary into ignored project tooling."""
import hashlib
import io
import tarfile
import urllib.request
from pathlib import Path

root = Path(__file__).resolve().parent.parent
url = "https://github.com/gitleaks/gitleaks/releases/download/v8.30.1/gitleaks_8.30.1_linux_x64.tar.gz"
expected = "551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb"
with urllib.request.urlopen(url, timeout=90) as response:
    payload = response.read()
if hashlib.sha256(payload).hexdigest() != expected:
    raise SystemExit("Gitleaks checksum mismatch")
target = root / ".tools" / "gitleaks"
target.parent.mkdir(exist_ok=True)
with tarfile.open(fileobj=io.BytesIO(payload), mode="r:gz") as archive:
    target.write_bytes(archive.extractfile("gitleaks").read())
target.chmod(0o755)
print("Pinned Gitleaks installed; checksum verified.")
