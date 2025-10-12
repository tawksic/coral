#!/bin/bash
# Complete local development workflow
# Builds, loads into K8s, and deploys - ready to test immediately
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/.."
NAMESPACE="coral-dev"
LOCAL_PORT=8080

echo "[1/6] Cleaning up old deployment..."
kubectl delete namespace $NAMESPACE --ignore-not-found=true --wait=true

echo "[2/6] Creating namespace..."
kubectl create namespace $NAMESPACE

echo "[3/6] Building images with :dev tag..."
docker build -t harbor.tawksic.com/coral/api:dev -f $PROJECT_ROOT/Dockerfile.app $PROJECT_ROOT

echo "[4/6] Loading images into minikube..."
minikube image load harbor.tawksic.com/coral/api:dev

echo "[5/6] Deploying to K8s namespace: $NAMESPACE..."
kubectl apply -f $PROJECT_ROOT/k8s/secrets.yaml -n $NAMESPACE
kubectl apply -f $PROJECT_ROOT/k8s/service.yaml -n $NAMESPACE

sed -e 's/:latest/:dev/g' \
    -e 's/imagePullPolicy: Always/imagePullPolicy: Never/g' \
    $PROJECT_ROOT/k8s/deployment.yaml | kubectl apply -f - -n $NAMESPACE

echo "[6/6] Waiting for deployment..."
kubectl rollout status deployment coral -n $NAMESPACE --timeout=60s

echo "Deployment complete"
echo ""

kubectl port-forward service/coral $LOCAL_PORT:80 -n $NAMESPACE > /dev/null 2>&1 &
PF_PID=$!
echo "Port-forward running in background (PID: $PF_PID)"
echo "Access at: http://localhost:$LOCAL_PORT"
echo "To stop: kill $PF_PID"
echo ""
