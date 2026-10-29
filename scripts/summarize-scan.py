"""Summarize the full scan and fail on HIGH/CRITICAL findings with fixes."""
import json
import sys
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

root = Path(__file__).resolve().parent.parent
report_path = root / (sys.argv[1] if len(sys.argv) > 1 else "evidence/test-results/" + datetime.now(UTC).strftime("%Y-%m-%d") + "-trivy.json")
report = json.loads(report_path.read_text())
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
lines = ["Trivy vulnerability summary", f"Full report: {report_path.relative_to(root)}"]
lines += [f"{level}: {counts[level]}" for level in ("CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN")]
lines += [f"Fixable HIGH/CRITICAL findings: {len(blocking)}", *sorted(rows)]
summary = "\n".join(lines) + "\n"
report_path.with_name(report_path.stem.replace("-trivy", "-scan-summary") + ".txt").write_text(summary)
print("\n".join(lines[:8]))
raise SystemExit(1 if blocking else 0)
