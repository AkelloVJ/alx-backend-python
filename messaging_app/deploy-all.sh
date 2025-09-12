#!/bin/bash

# Comprehensive deployment script for Django Messaging App on Kubernetes
# This script deploys all components and runs all required tasks

echo "=== Django Messaging App - Complete Kubernetes Deployment ==="

# Check if kubectl is available
if ! command -v kubectl &> /dev/null; then
    echo "Error: kubectl is not installed or not in PATH"
    exit 1
fi

# Check if cluster is accessible
if ! kubectl cluster-info &> /dev/null; then
    echo "Error: Cannot connect to Kubernetes cluster"
    exit 1
fi

echo "=== Step 1: Deploying MySQL Database ==="
kubectl apply -f mysql-deployment.yaml
echo "Waiting for MySQL to be ready..."
kubectl wait --for=condition=ready pod -l app=mysql --timeout=120s

echo "=== Step 2: Deploying Django Application ==="
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
echo "Waiting for Django app to be ready..."
kubectl wait --for=condition=ready pod -l app=django-messaging-app --timeout=120s

echo "=== Step 3: Running Scaling and Load Testing ==="
./kubctl-0x01

echo "=== Step 4: Setting up Ingress ==="
echo "Installing Nginx Ingress Controller..."
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml

echo "Waiting for ingress controller to be ready..."
kubectl wait --namespace ingress-nginx \
  --for=condition=ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=120s

kubectl apply -f ingress.yaml

echo "=== Step 5: Running Blue-Green Deployment ==="
./kubctl-0x02

echo "=== Step 6: Running Rolling Update ==="
./kubctl-0x03

echo "=== Deployment Summary ==="
echo "Pods:"
kubectl get pods

echo "Services:"
kubectl get services

echo "Ingress:"
kubectl get ingress

echo "=== All deployments completed successfully! ==="
echo "You can now access your application through the ingress or port-forward:"
echo "kubectl port-forward service/django-messaging-service 8000:8000"

