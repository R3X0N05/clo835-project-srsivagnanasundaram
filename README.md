# CLO835-PROJECT 15 | SELF-HEALING AND PROBE TUNING

![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.35-blue) ![kind](https://img.shields.io/badge/kind-v0.31-green) ![Docker](https://img.shields.io/badge/Docker-29.x-blue) ![Python](https://img.shields.io/badge/Python-3.11-blue)

**By:** S.R.Selva Roshan | 126332246

---

## Contents

- [Project Overview](#project-overview)
- [System Architecture](#system-architecture)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Probe Math](#probe-math)
- [Key Learning Outcomes](#key-learning-outcomes)
- [References](#references)

---

## Project Overview

In this project, we deploy an unreliable Flask app which is created that way on purpose to a local kind cluster
to demonstrate how K8S startup, readiness, and liveness probes work together to keep apps healthy and makes sure
that they recover from any failures.

The app can be adjusted to create a startup delay and health-check response time tat runtime though ConfigMap, without
having to rebuild the container image. This allows to demonstrate easily, similar real-world situations. Eg: slow application startup, stuck pods, traffic being held back unitl a pod is ready, and probe settings which are configured with aggressive intents.

Another part of this project is the anti-demo which demonstrates what happens if a strict liveness probe is used to force a healthy application to go into CrashLoopBackOff. This is to highlight an important understanding, that it's not always the app causing the problem but rather a misconfigured health check.

---

## System Architecture

```text
                    +---------------------------+
                    |   curl-client pod         |
                    |   (curlimages/curl)        |
                    +------------+--------------+
                                 |
                                 | HTTP requests
                                 v
                    +---------------------------+
                    |   flaky-svc-126332246     |
                    |   ClusterIP Service       |
                    +------------+--------------+
                                 |
                    +------------+--------------+
                    |                           |
                    v                           v
         +----------+--------+      +----------+--------+
         | flaky pod (1 of 3)|      | flaky pod (2 of 3)|
         | startupProbe      |      | startupProbe      |
         | readinessProbe    |      | readinessProbe    |
         | livenessProbe     |      | livenessProbe     |
         +-------------------+      +-------------------+
                    |
                    v
         +----------+--------+
         | flaky pod (3 of 3)|
         | startupProbe      |
         | readinessProbe    |
         | livenessProbe     |
         +-------------------+
```

---

## Repository Structure

```text
clo835-project-srsivagnanasundaram/
│
├── app/
│   └── app.py
│
├── manifests/
│   ├── 00-namespace.yaml
│   ├── 10-configmap.yaml
│   ├── 30-deployment.yaml
│   ├── 40-service.yaml
│   ├── 50-curl-pod.yaml
│   └── 90-bad-liveness.yaml
│
├── evidence/
│
├── Dockerfile
├── requirements.txt
├── kind-config.yaml
├── bootstrap.sh
├── runbook.md
├── predictions.md
└── README.md
```

| File / Directory | Description |
|---|---|
| `app/app.py` | Flask app with /healthz, /wedge, and / routes |
| `Dockerfile` | Builds the flaky app image |
| `manifests/` | Kubernetes manifests applied in numbered order |
| `manifests/90-bad-liveness.yaml` | Anti-demo only — do not apply during normal operation |
| `kind-config.yaml` | kind cluster definition (1 control-plane + 2 workers) |
| `bootstrap.sh` | Brings up the full environment from a clean host |
| `runbook.md` | Step-by-step demo commands |
| `predictions.md` | Probe math worksheet for the instructor twist |
| `evidence/` | Terminal transcripts from dry runs |

---

## Prerequisites

- Docker
- kind v0.31.0
- kubectl v1.35.0

See `runbook.md` for installation commands.

---

## Quick Start

```bash
chmod +x bootstrap.sh
./bootstrap.sh
kubectl get pods -n probes-126332246 -w
```

Wait until all 3 pods show `1/1 Running` with restart count 0.

---

## Probe Math

| Probe | Config | Calculation | Result |
|---|---|---|---|
| startupProbe | period 5s / threshold 25 | 25 x 5 = 125s | max boot window |
| readinessProbe | period 5s / threshold 2 | 2 x 5 = 10s | time to leave endpoints |
| livenessProbe | period 10s / threshold 3 | 3 x 10 = 30s | time to kill |

---

## Key Learning Outcomes

- What startup, readiness, and liveness probes each do and which failure each one handles
- How failureThreshold x periodSeconds combines into a time-to-kill budget
- How readiness gates Service endpoints so unready pods receive zero traffic without being killed
- How a mis-tuned liveness probe produces CrashLoopBackOff on a healthy app
- How to predict probe behaviour from numbers before applying a manifest

## References

- Kubernetes Documentation — https://kubernetes.io/docs/
- Configure Liveness, Readiness and Startup Probes — https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
- kind (Kubernetes in Docker) — https://kind.sigs.k8s.io/

---



