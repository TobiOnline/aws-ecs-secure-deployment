#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
image="${1:-aws-ecs-secure-deployment:stage2}"
scanner="$(cat .trivy-image)"
mkdir -p .cache evidence/test-results
docker save -o .cache/stage2-image.tar "$image"
docker run --rm   -v "$PWD/.cache:/cache"   -v "$PWD/evidence/test-results:/reports"   "$scanner" image --quiet --cache-dir /cache/trivy   --input /cache/stage2-image.tar --scanners vuln   --format json --output /reports/02-trivy.json
python3 scripts/summarize-scan.py
