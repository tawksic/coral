#!/bin/bash
# Complete production workflow
# Builds, pushes to Harbor, and deploys to production K8s
# TODO: Automate Harbor push via GitHub Actions/Jenkins instead of manual script
set -e

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/.."
NAMESPACE="coral-prod"
LOCAL_PORT=9080
VERSION=$(grep '^version = ' $PROJECT_ROOT/pyproject.toml | sed 's/version = "\(.*\)"/\1/')

echo "WARNING: This will build, push to Harbor, and deploy to namespace: $NAMESPACE"
echo "Version: v$VERSION"
read -p "Continue? (y/N) " -r
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled"
    exit 1
fi

echo "[1/5] Creating namespace..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -

echo "[2/5] Building production images..."
docker build -t harbor.tawksic.com/coral/api:latest -f $PROJECT_ROOT/Dockerfile.app $PROJECT_ROOT
docker build -t harbor.tawksic.com/coral/jenkins:latest -f $PROJECT_ROOT/Dockerfile.jenkins $PROJECT_ROOT

echo "[3/5] Pushing to Harbor..."
docker push harbor.tawksic.com/coral/api:latest
docker push harbor.tawksic.com/coral/jenkins:latest

echo "[4/5] Deploying to K8s namespace: $NAMESPACE..."
# Order matters here, use kustomization.yaml or helm charts for this later
kubectl apply -f $PROJECT_ROOT/k8s/secrets.yaml -n $NAMESPACE
kubectl apply -f $PROJECT_ROOT/k8s/service.yaml -n $NAMESPACE
kubectl apply -f $PROJECT_ROOT/k8s/deployment.yaml -n $NAMESPACE

echo "[5/5] Waiting for deployment..."
kubectl rollout status deployment coral -n $NAMESPACE --timeout=60s

echo "Production deployment complete"
echo ""

kubectl port-forward service/coral $LOCAL_PORT:80 -n $NAMESPACE > /dev/null 2>&1 &
PF_PID=$!
echo "Port-forward running in background (PID: $PF_PID)"
echo "Access at: http://localhost:$LOCAL_PORT"
echo "To stop: kill $PF_PID"

