"""Install pinned Terraform locally; no AWS or system configuration changes."""
import hashlib
import io
import urllib.request
import zipfile
from pathlib import Path

root = Path(__file__).resolve().parent.parent
target = root / ".tools/terraform"
if target.exists():
    raise SystemExit("Terraform already exists; preserve it and check .tools/terraform version")
url = "https://releases.hashicorp.com/terraform/1.17.1/terraform_1.17.1_linux_amd64.zip"
expected = "4638628058e71a55212b1c563712eac03b902128f40740f3dc8174df12135061"
with urllib.request.urlopen(url, timeout=120) as response:
    payload = response.read()
if hashlib.sha256(payload).hexdigest() != expected:
    raise SystemExit("Terraform archive checksum mismatch")
target.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(io.BytesIO(payload)) as archive:
    target.write_bytes(archive.read("terraform"))
target.chmod(0o755)
print("Pinned Terraform installed in .tools; archive checksum verified.")
