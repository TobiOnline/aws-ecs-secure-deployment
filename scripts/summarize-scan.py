"""Summarize the full scan and fail on HIGH/CRITICAL findings with fixes."""
import json
from collections import Counter
from pathlib import Path

root = Path(__file__).resolve().parent.parent
report = json.loads((root / "evidence/test-results/02-trivy.json").read_text())
if "Results" not in report or not report.get("Metadata", {}).get("OS"):
    raise SystemExit("Incomplete scan report: OS metadata or results missing")
counts = Counter()
blocking = []
rows = []
for result in report.get("Results", []):
    for finding in result.get("Vulnerabilities", []):
        severity = finding["Severity"]
        counts[severity] += 1
        fixed = finding.get("FixedVersion", "")
        rows.append(f"{severity} {finding['VulnerabilityID']} {finding['PkgName']} {finding['InstalledVersion']} fixed={fixed or 'not available'}")
        if severity in ("HIGH", "CRITICAL") and fixed:
            blocking.append(finding)
lines = ["Trivy vulnerability summary", "Full report: evidence/test-results/02-trivy.json"]
lines += [f"{level}: {counts[level]}" for level in ("CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN")]
lines += [f"Fixable HIGH/CRITICAL findings: {len(blocking)}", *sorted(rows)]
summary = "\n".join(lines) + "\n"
(root / "evidence/test-results/02-scan-summary.txt").write_text(summary)
print("\n".join(lines[:8]))
raise SystemExit(1 if blocking else 0)
