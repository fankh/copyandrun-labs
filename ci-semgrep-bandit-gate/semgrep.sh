#!/usr/bin/env bash
set -euo pipefail
semgrep \
  --config rules \
  --config p/owasp-top-ten \
  --error \
  --sarif -o semgrep.sarif \
  app
