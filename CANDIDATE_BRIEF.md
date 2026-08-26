# Candidate Brief — item-service stability

## The situation
`item-service` is a small FastAPI + Postgres service that runs in Kubernetes
(namespace `itemsvc`). It was recently scaled up and has become unstable: pods are
restarting and erroring, and on-call has flagged it.

## Setup
You'll need a Kubernetes cluster you can reach with `kubectl` (any cluster is fine —
a local one such as kind/minikube/Docker Desktop, or a remote one). The app image is
already published, so you don't need to build anything.

The `scripts/` folder has small helper scripts, but they're entirely optional — each is
just a thin wrapper around ordinary `kubectl`. Use the helpers or run the commands
directly, whichever you prefer.

Apply the manifests — either:
```bash
./scripts/apply.sh
```
or directly:
```bash
kubectl apply -f k8s/
```

Check status — either `./scripts/status.sh`, or directly:
```bash
kubectl -n itemsvc get pods
kubectl -n itemsvc get events --sort-by=.lastTimestamp
```

Give it a minute or two to settle. If your cluster has metrics-server you can also use
`kubectl -n itemsvc top pod`; if not, use `kubectl -n itemsvc describe pod <pod>` and
the pods' RESTARTS column to reason about resource behavior.

## Part 1 — Investigate
Figure out what's wrong. Use whatever you'd normally reach for — pod status, logs,
events, resource usage, and the source in `app/`. Talk us through your process: what
you're checking, what you expect, and what each finding tells you. Identify as many of
the service's problems as you can and explain the root cause of each.

## Part 2 — Review the fix
A teammate has opened a pull request that attempts to fix the reported problems. Review
it as you would any PR: leave inline comments and give a short walkthrough of your
reasoning. We care whether each change is correct, complete, and safe — and what you'd
want changed before it ships. Your running cluster is still available, so feel free to
check the PR's claims against what you actually observe.

## Part 3 — Decision
Would you approve, request changes, or something else? What single change to process or
tooling would most reduce the chance of this class of problem recurring?

## Useful commands
```
kubectl -n itemsvc get pods
kubectl -n itemsvc describe pod <pod>
kubectl -n itemsvc logs <pod>              # add --previous for a crashed container
kubectl -n itemsvc logs deploy/postgres    # database server logs
kubectl -n itemsvc get events --sort-by=.lastTimestamp
kubectl -n itemsvc top pod                 # only if metrics-server is installed
```

## Cleanup
Either `./scripts/teardown.sh`, or directly:
```bash
kubectl delete namespace itemsvc
```
