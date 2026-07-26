#!/bin/bash

# Boostrap for CLO835 Project
# Prequisites: Kind, Docker and Kubectl

set -euxo pipefail

#Declaring ID and namespace
STUDENT_ID="126332246"
NS="probes-${STUDENT_ID}"

#creating kind cluster
kind create cluster --name "probe-${STUDENT_ID}" --config kind-config.yaml --wait 120s

#retrieving docker image from docker hub and loading it to kind cluster
docker pull r3x0n05/flaky-${STUDENT_ID}:v1
kind load docker-image r3x0n05/flaky-${STUDENT_ID}:v1 --name probe-${STUDENT_ID}

#manifests being applied in order
kubectl apply -f manifests/00-namespace.yaml
kubectl apply -f manifests/10-configmap.yaml
kubectl apply -f manifests/30-deployment.yaml
kubectl apply -f manifests/40-service.yaml
kubectl apply -f manifests/50-curl-pod.yaml

#rollout 
kubectl rollout status deployment/flaky-${STUDENT_ID} -n ${NS} --timeout=300s

#retrieving deployed pods
kubectl get pods -n ${NS}