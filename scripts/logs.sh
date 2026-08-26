#!/usr/bin/env bash
# Follow logs for all app pods. Assumes only that kubectl is installed.
set -euo pipefail
kubectl -n itemsvc logs -l app=item-service --prefix --tail=50 -f
