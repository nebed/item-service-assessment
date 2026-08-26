#!/usr/bin/env bash
# Apply the exercise manifests to whatever cluster your current kubectl context
# points at. Assumes only that kubectl is installed and configured.
set -euo pipefail
cd "$(dirname "$0")/.."

kubectl apply -f k8s/00-namespace.yaml
kubectl apply -f k8s/10-postgres.yaml
kubectl apply -f k8s/20-app.yaml

echo
echo "Applied. Check status with: ./scripts/status.sh"
echo "(The app image comes from your registry as set in k8s/20-app.yaml.)"
