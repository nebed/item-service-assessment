# item-service

A small FastAPI + Postgres service that runs on Kubernetes.

This repository is part of a technical exercise. Please start with
**`CANDIDATE_BRIEF.md`** — it explains the scenario and what we'd like you to do.

## What's here
- `app/` — the service source code
- `k8s/` — Kubernetes manifests (namespace, Postgres, and the service)
- `scripts/` — optional helper scripts (thin wrappers around `kubectl`); you can use
  them or run the equivalent `kubectl` commands directly, whichever you prefer

## Requirements
- A Kubernetes cluster you can reach with `kubectl`. Anything works — a local cluster
  (kind, minikube, Docker Desktop) or a remote one. You just need `kubectl` pointed at
  it (`kubectl cluster-info` should succeed).
- No build step: the container image is already published, so applying the manifests is
  all that's needed.

## Getting it running
```bash
# apply everything to whatever cluster your current kubectl context points at
kubectl apply -f k8s/          # or: ./scripts/apply.sh

# see what's happening
kubectl -n itemsvc get pods    # or: ./scripts/status.sh
```

Give it a minute or two to settle, then head to `CANDIDATE_BRIEF.md` for the task.

## Cleanup when you're done
```bash
kubectl delete namespace itemsvc    # or: ./scripts/teardown.sh
```
