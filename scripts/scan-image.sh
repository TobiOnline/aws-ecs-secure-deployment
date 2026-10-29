#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
image="${1:-aws-ecs-secure-deployment:stage3}"
report_name="${2:-$(date -u +%F)-trivy.json}"
case "$report_name" in
  */*|..*) echo "Use a report filename, not a path" >&2; exit 1 ;;
esac
scanner="$(cat .trivy-image)"
cache_dir="$PWD/.cache/security-scan"
mkdir -p "$cache_dir" evidence/test-results
docker save -o "$cache_dir/scan-image.tar" "$image"
docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -v "$cache_dir:/cache" -v "$PWD/evidence/test-results:/reports"   "$scanner" image --quiet --cache-dir /cache/trivy --input /cache/scan-image.tar   --scanners vuln --format json --output "/reports/$report_name"
python3 scripts/summarize-scan.py "evidence/test-results/$report_name"
