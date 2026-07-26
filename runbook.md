# CLO 835 Project : Self-healing and probe tuning
## S.R.Selva Roshan | 126332246

# Runbook

## Prerequisites

To begin running this project please make sure that the following are installed and ready before proceeding with cloning the repo
:- Docker | Kind | Kubectl

If you do not have these present in your EC2, please follow the commands below

Install Docker
```bash
  sudo apt-get update && sudo apt-get install -y ca-certificates curl
  sudo install -m 0755 -d /etc/apt/keyrings
  sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
  echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  sudo apt-get update && sudo apt-get install -y docker-ce docker-ce-cli containerd.io
  sudo usermod -aG docker $USER
  newgrp docker
```  

Install kind v0.31.0
```bash
  curl -sLo kind https://kind.sigs.k8s.io/dl/v0.31.0/kind-linux-amd64
  sudo install -o root -g root -m 0755 kind /usr/local/bin/kind
```

Install kubectl v1.35.0 (exact match to kind's default K8s version)
```bash
  curl -LO "https://dl.k8s.io/release/v1.35.0/bin/linux/amd64/kubectl"
  chmod +x kubectl && sudo mv kubectl /usr/local/bin/
```

Run these commands to verify the installation is successful
```bash
  docker version
  kind version
  kubectl version --client
```

Clone the project repository
```bash
  git clone https://github.com/R3X0N05/clo835-project-srsivagnanasundaram.git
  cd clo835-project-srsivagnanasundaram
```

Variables in the Project - Declare before running commands on terminal
```bash
NS="probes-126332246"
DEP="flaky-126332246"
SVC="flaky-svc-126332246"
```

## -------------------- Section 1 : Bootstrap ----------------------------

run below commands in order
```bash
chmod +x bootstrap.sh
./bootstrap.sh
kubectl get pods -n probes-126332246 -w
```

Please wait patiently for all 3 deployed pods to be running successfully with restartCount set at 0

## ------------------ Section 2 : Demonstrate deployed probes ----------------------

run below commands in order
```bash
kubectl get pods -n probes-126332246
grep -A 30 'startupProbe' manifests/30-deployment.yaml
```

## ---------------- Section 3 : Demonstrate rotating hostnames using curl --------------------

run below commands in order
```bash
kubectl exec -it curl-client -n probes-126332246 -- \
  sh -c 'while true; do curl -s http://flaky-svc-126332246/; sleep 0.5; done'
```

This demonstrates the three different pods using hostnames to show all of them contain my student id

## -------------- Section 4 : Demonstrate self-heal live -------------------
 
run below commands in order
```bash
POD=$(kubectl get pods -n probes-126332246 -o name | head -1 | cut -d/ -f2)
kubectl port-forward pod/$POD 8080:8080 -n probes-126332246 &
sleep 1
curl -X POST http://localhost:8080/wedge
kill %1
```

Open a second terminal to show the live demonstration of kill it command which will take 30s as which is failurethreshold x periodSeconds = 3 x 10
```bash
kubectl get pods -n probes-126332246 -w
```

Run the command below to verify that there is only 1 restarted pod
```bash
kubectl get pod $POD -n probes-126332246 \
 -o jsonpath='{.status.containerStatuses[0].restartCount}'
#-> 1
```

Run the command below to verify that liveness was successful
```bash
kubectl describe pod $POD -n probes-126332246 | grep -A 5 "Liveness"
kubectl get events -n probes-126332246 --sort-by=.lastTimestamp | tail -20
```

This demonstrates the liveness probe failing and then terminating the container

## ---------- Section 5 : Demonstrate slow-start and how probe tolerates 90 seconds without restarting ---------

run below commands in order
```bash
kubectl create configmap flaky-config-126332246 \
    --from-literal=STARTUP_DELAY_SECONDS=90 \
    --from-literal=HEALTHZ_LATENCY_MS=0 \
    -n probes-126332246 \
    --dry-run=client -o yaml | kubectl apply -f -

kubectl rollout restart deployment/flaky-126332246 -n probes-126332246
kubectl rollout status deployment/flaky-126332246 -n probes-126332246
```

Run below commands to observe the pods not restart for 90 seconds
```bash
kubectl get pods -n probes-126332246 -w
```

You can observe newly deployed pods at 0/1 without restarting while old pods
keep serving throughout demonstarting readiness gating

## ------------ Section 6 : Demonstarting readiness gating on two paths ----------------

Demonstrating the first path which is wedge showing liveness killing the pod
run below commands in order
```bash
kubectl get endpoints flaky-svc-126332246 -n probes-126332246
```
This demonstates the endpoint dropping briefly and coming back when the pod is restarted

Demonstrating the second path which is slow healthz where the readinesss removes pod and liveness does not try to interact with it
run below commands in order
```bash
kubectl create configmap flaky-config-126332246 \
 --from-literal=STARTUP_DELAY_SECONDS=0 \
 --from-literal=HEALTHZ_LATENCY_MS=2500 \
 -n probes-126332246 \
 --dry-run=client -o yaml | kubectl apply -f -

kubectl rollout restart deployment/flaky-126332246 -n probes-126332246
kubectl rollout status deployment/flaky-126332246 -n probes-126332246

kubectl get pods -n probes-126332246

# Demonstrating pods ready without restarting
kubectl get endpoints flaky-svc-126332246 -n probes-126332246
```
Demonstarting no addresses being listed

run below commands in order to restore
```bash
kubectl create configmap flaky-config-126332246 \
    --from-literal=STARTUP_DELAY_SECONDS=0 \
    --from-literal=HEALTHZ_LATENCY_MS=0 \
    -n probes-126332246 \
    --dry-run=client -o yaml | kubectl apply -f -

kubectl rollout restart deployment/flaky-126332246 -n probes-126332246
kubectl rollout status deployment/flaky-126332246 -n probes-126332246
```

## ------------- Section 7 : Demonstrate time to kill formula -----------------

below shows the math behind the time to kill formula that's being used
```
time to kill = failureThreshold * periodSeconds
            + timeoutSeconds per poll (when endpoint is slow)
good probe: 3 x 10 = 30 seconds
bad probe: 1 x 2 = 2 seconds (poll timesout at 1 second)
```

## -------------- Section 8 : For Professor's Twist ---------------------

run nano predictions and fill in the numbers professor's provides
```bash
nano predictions.md
```

## ----------- Section 9 : Demonstrate Healthly app into CrashLoopBackOff ---------

run below commands in order
```bash
kubectl create configmap flaky-config-126332246 \
    --from-literal=STARTUP_DELAY_SECONDS=0 \
    --from-literal=HEALTHZ_LATENCY_MS=2000 \
    -n probes-126332246 \
    --dry-run=client -o yaml | kubectl apply -f -

kubectl rollout restart deployment/flaky-126332246 -n probes-126332246
kubectl rollout status deployment/flaky-126332246 -n probes-126332246
```

Run below command to verify that the app is in healthy state before applying the bad manifest
```bash
kubectl exec -it curl-client -n probes-126332246 -- curl -s http://flaky-svc-126332246/
```
This will demonstrate a hello message from my pod

Run below command to apply the bad manifest and we can watch it live the pod trying to restart but failing to CrashLoopBackOff
```bash
kubectl apply -f manifests/90-bad-liveness.yaml
kubectl get pods -n probes-126332246 -w
```

Run below commands to prove that the probe and restarting failed
```bash
kubectl describe pod -n probes-126332246 -l app=flaky-126332246 | grep -A 3 "Liveness probe failed"
kubectl get events -n probes-126332246 --sort-by=.lastTimestamp | tail -20
```

# ------------- Section 10: Demonstrate recovery -----------------

run below commands in order to recover the pods back to the healthy state
```bash
kubectl apply -f manifests/30-deployment.yaml

kubectl create configmap flaky-config-126332246 \
  --from-literal=STARTUP_DELAY_SECONDS=0 \
  --from-literal=HEALTHZ_LATENCY_MS=0 \
  -n probes-126332246 \
  --dry-run=client -o yaml | kubectl apply -f -
```

Run below commands to demonstrate that pods have recovered back to healthy state
```bash
kubectl rollout restart deployment/flaky-126332246 -n probes-126332246
kubectl rollout status deployment/flaky-126332246 -n probes-126332246
kubectl get pods -n probes-126332246
```

# ------------- Section 11 : Cleanup Environment -----------

run below commands in order to cleanup environment
```bash
kind delete cluster --name probe-126332246
```

# ------ END OF DEMONSTRATION - THANK YOU ---------