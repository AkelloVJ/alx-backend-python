#!/bin/bash

# Cleanup script for Django Messaging App Kubernetes deployment

echo "=== Cleaning up Django Messaging App deployment ==="

echo "Deleting deployments..."
kubectl delete -f blue_deployment.yaml 2>/dev/null || true
kubectl delete -f green_deployment.yaml 2>/dev/null || true
kubectl delete -f deployment.yaml 2>/dev/null || true

echo "Deleting services..."
kubectl delete -f kubeservice.yaml 2>/dev/null || true
kubectl delete -f service.yaml 2>/dev/null || true

echo "Deleting ingress..."
kubectl delete -f ingress.yaml 2>/dev/null || true

echo "Deleting MySQL..."
kubectl delete -f mysql-deployment.yaml 2>/dev/null || true

echo "Deleting ingress controller..."
kubectl delete -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml 2>/dev/null || true

echo "Cleaning up any remaining resources..."
kubectl delete pods -l app=django-messaging-app 2>/dev/null || true
kubectl delete services -l app=django-messaging-app 2>/dev/null || true
kubectl delete services -l app=mysql 2>/dev/null || true

echo "=== Cleanup completed ==="
echo "Remaining resources:"
kubectl get pods
kubectl get services
kubectl get ingress

