# Django Messaging App - Kubernetes Deployment

This document provides instructions for deploying the Django Messaging App on Kubernetes.

## Prerequisites

- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl configured to access your cluster
- Docker image built and available in your cluster

## Files Overview

### Core Deployment Files
- `deployment.yaml` - Initial deployment configuration
- `service.yaml` - ClusterIP service for internal access
- `ingress.yaml` - Ingress configuration for external access
- `commands.txt` - Commands for setting up ingress controller

### Blue-Green Deployment Files
- `blue_deployment.yaml` - Blue version deployment (version 2.0)
- `green_deployment.yaml` - Green version deployment (version 1.1)
- `kubeservice.yaml` - Service configuration for blue-green switching

### Scripts
- `kubctl-0x01` - Scaling and load testing script
- `kubctl-0x02` - Blue-green deployment script
- `kubctl-0x03` - Rolling update script

## Deployment Steps

### 1. Basic Deployment

```bash
# Deploy the application
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

# Verify deployment
kubectl get pods
kubectl get services
```

### 2. Scaling and Load Testing

```bash
# Run the scaling and load testing script
./kubctl-0x01
```

This script will:
- Scale the deployment to 3 replicas
- Perform load testing with wrk
- Monitor resource usage
- Check pod logs

### 3. Ingress Setup

```bash
# Install Nginx Ingress Controller
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml

# Apply ingress configuration
kubectl apply -f ingress.yaml

# Verify ingress
kubectl get ingress
```

### 4. Blue-Green Deployment

```bash
# Run blue-green deployment script
./kubctl-0x02
```

This script will:
- Deploy both blue and green versions
- Check logs for errors
- Switch traffic from blue to green
- Verify the deployment

### 5. Rolling Updates

```bash
# Run rolling update script
./kubctl-0x03
```

This script will:
- Apply the updated deployment (version 2.0)
- Monitor the rolling update process
- Perform continuous testing during update
- Verify completion

## Configuration Details

### Environment Variables
The deployment uses the following environment variables:
- `DEBUG`: Set to "False" for production
- `ALLOWED_HOSTS`: Set to "*" for flexibility
- `MYSQL_HOST`: Database host (mysql-service)
- `MYSQL_DATABASE`: Database name (messaging_db)
- `MYSQL_USER`: Database user (messaging_user)
- `MYSQL_PASSWORD`: Database password (messaging_password)
- `MYSQL_PORT`: Database port (3306)
- `SECRET_KEY`: Django secret key

### Resource Limits
- Memory: 256Mi request, 512Mi limit
- CPU: 250m request, 500m limit

### Health Checks
- Liveness probe: HTTP GET /api/ every 10 seconds
- Readiness probe: HTTP GET /api/ every 5 seconds

## Monitoring and Troubleshooting

### Check Pod Status
```bash
kubectl get pods -l app=django-messaging-app
```

### View Logs
```bash
kubectl logs <pod-name>
```

### Check Service Status
```bash
kubectl get services -l app=django-messaging-app
```

### Monitor Resource Usage
```bash
kubectl top pods
kubectl top nodes
```

## Notes

- All scripts are executable and include error handling
- The deployment assumes a MySQL database is available
- Ingress is configured for both localhost and django-messaging.local
- Blue-green deployment allows for zero-downtime updates
- Rolling updates ensure minimal disruption during version changes

