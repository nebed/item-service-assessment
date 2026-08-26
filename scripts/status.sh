#!/usr/bin/env bash
# Show current state of the exercise workloads. Assumes only that kubectl is installed.
set -euo pipefail

echo "== pods =="
kubectl -n itemsvc get pods

echo
echo "== recent events =="
kubectl -n itemsvc get events --sort-by=.lastTimestamp | tail -20
