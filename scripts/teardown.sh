#!/usr/bin/env bash
# Remove everything this exercise created. Assumes only that kubectl is installed.
set -euo pipefail
kubectl delete namespace itemsvc --ignore-not-found
