# item-service — Debugging + Code Review Assessment

A two-part exercise for platform / backend engineers:
1. **Debug** a service that's failing in Kubernetes.
2. **Review** a pull request that attempts to fix it.

The app image is pre-published to a registry, so the only requirement is a Kubernetes
cluster reachable via `kubectl`. No local build, no cluster-type assumptions.

## Layout
- `app/` — the service source (this is the version running in the cluster)
- `k8s/` — namespace, Postgres, and the app Deployment/Service (pure YAML)
- `scripts/` — optional helper wrappers around `kubectl`: `apply.sh`, `status.sh`,
  `logs.sh`, `teardown.sh`. Every one is a one-liner you can run directly instead;
  they exist only for convenience.
- `CANDIDATE_BRIEF.md` — hand this to the candidate
- `pr/` — reference copy of the fix and its diff (see note below)

## Before you share this repo
1. **Build and push the image** (one time), as a **multi-platform** image so it runs
   on both amd64 and arm64 clusters. It's referenced in `k8s/20-app.yaml` as
   `docker.io/uchenebed/item-service:v1`:
   ```bash
   docker login
   # one-time: create a buildx builder that can do multi-arch
   docker buildx create --name multiarch --use   # skip if you already have one
   docker buildx build \
     --platform linux/amd64,linux/arm64 \
     -t docker.io/uchenebed/item-service:v1 \
     --push app
   ```
   `buildx ... --push` builds both architectures and publishes a single manifest list
   in one step (a plain `docker build` produces only your machine's arch, which fails
   with `exec format error` on the other). Verify both arches are present:
   ```bash
   docker buildx imagetools inspect docker.io/uchenebed/item-service:v1
   ```
   If you change the app code later, rebuild+push a new tag (`:v2`, ...) the same way
   and bump the `image:` line in `k8s/20-app.yaml` to match.
2. **Keep the interviewer guide out of the repo.** `INTERVIEWER_GUIDE.md` is the answer
   key — it must not be pushed anywhere the candidate can see it. Store it locally only.
3. Open the PR (`fix/stability-issues` -> `main`) in the repo so the candidate can
   review and comment on it.

## Candidate flow
The helper scripts are optional — candidates can use them or run the equivalent
`kubectl` commands directly (the candidate brief shows both).
```bash
git clone <repo>
cd code-review-exercise
./scripts/apply.sh        # or: kubectl apply -f k8s/
./scripts/status.sh       # or: kubectl -n itemsvc get pods
```
Then investigate, then review the PR. See `CANDIDATE_BRIEF.md`.

## Expected failing state
- One app pod stays `CrashLoopBackOff` — its logs show the Postgres error
  `sorry, too many clients already` (3 replicas x pool 10 = 30 connections, which
  exceeds the ~24-25 usable given `max_connections=30`).
- The two running pods' memory climbs and they periodically `OOMKilled`/restart
  (an unbounded in-memory cache).
- The logs are a flood of low-value INFO lines that bury the real errors.

## Reset between candidates
Either the helper or the direct command:
```bash
./scripts/teardown.sh && ./scripts/apply.sh
# or:
kubectl delete namespace itemsvc && kubectl apply -f k8s/
```
