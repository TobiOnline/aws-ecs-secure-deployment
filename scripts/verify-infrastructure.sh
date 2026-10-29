#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
.tools/terraform -chdir=infrastructure/terraform fmt -check
.tools/terraform -chdir=infrastructure/terraform validate -no-color
