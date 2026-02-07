# Minikube Deployment Commands

This document contains all the commands used to deploy the Todo Chatbot application to Minikube.

## Prerequisites

- Minikube installed
- kubectl installed
- Docker installed
- Helm installed (optional, for Helm deployments)

## 1. Start Minikube

```powershell
minikube start
```

## 2. Verify Minikube Status

```powershell
minikube status
kubectl cluster-info
```

## 3. Build Docker Images in Minikube's Docker Environment

### Set Docker Environment to Minikube

```powershell
minikube docker-env
# Apply the environment variables
& minikube -p minikube docker-env --shell powershell | Invoke-Expression
```

### Build Backend Image

```powershell
cd backend
docker build -t todo-chatbot-backend:latest .
cd ..
```

### Build Frontend Image

```powershell
cd frontend
docker build -t todo-chatbot-frontend:latest .
cd ..
```

## 4. Verify Images in Minikube

```powershell
minikube image ls | Select-String "todo-chatbot"
```

## 5. Deploy Using Helm

### Install/Upgrade Helm Chart

```powershell
helm upgrade --install todo-chatbot ./helm/todo-chatbot
```

### Verify Helm Release

```powershell
helm list
helm status todo-chatbot
```

## 6. Verify Deployments and Pods

### Check Deployments

```powershell
kubectl get deployments
```

### Check Pods

```powershell
kubectl get pods
kubectl get pods -o wide
```

### Check Pod Logs

```powershell
# Backend logs
kubectl logs <backend-pod-name>

# Frontend logs
kubectl logs <frontend-pod-name>

# Follow logs in real-time
kubectl logs -f <pod-name>

# Get last 50 lines
kubectl logs <pod-name> --tail=50
```

## 7. Verify Services

```powershell
kubectl get services
kubectl get svc
```

## 8. Access the Application

### Option 1: Port Forwarding (Recommended for Windows Docker Driver)

```powershell
# Forward frontend service
kubectl port-forward service/todo-chatbot-frontend 3000:80

# Forward backend service (in another terminal)
kubectl port-forward service/todo-chatbot-backend 8000:8000
```

Then access:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

### Option 2: Minikube Service (Creates Tunnel)

```powershell
# Get frontend URL
minikube service todo-chatbot-frontend --url

# Get backend URL
minikube service todo-chatbot-backend --url
```

Note: On Windows with Docker driver, this requires keeping the terminal open.

### Option 3: NodePort Access

```powershell
# Get minikube IP
minikube ip

# Access via NodePort
# Frontend: http://<minikube-ip>:31196
# Backend: http://<minikube-ip>:<backend-nodeport>
```

## 9. Test the Application

### Test Backend Health

```powershell
curl http://localhost:8000/health -UseBasicParsing
```

### Test Frontend

```powershell
curl http://localhost:3000 -UseBasicParsing
```

## 10. Troubleshooting Commands

### Describe Pod (for debugging)

```powershell
kubectl describe pod <pod-name>
```

### Check Pod Events

```powershell
kubectl get events --sort-by=.metadata.creationTimestamp
```

### Restart Deployment

```powershell
kubectl rollout restart deployment todo-chatbot-backend
kubectl rollout restart deployment todo-chatbot-frontend
```

### Check Rollout Status

```powershell
kubectl rollout status deployment/todo-chatbot-backend
kubectl rollout status deployment/todo-chatbot-frontend
```

### Delete and Recreate Deployment

```powershell
kubectl delete deployment todo-chatbot-frontend
helm upgrade todo-chatbot ./helm/todo-chatbot
```

### Remove Old Images from Minikube

```powershell
# List images
minikube image ls

# Remove specific image
minikube image rm todo-chatbot-frontend:latest
```

### Load Image into Minikube

```powershell
minikube image load todo-chatbot-frontend:latest
```

## 11. Update Application

### Rebuild and Redeploy

```powershell
# Set Docker environment
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# Rebuild image
cd frontend
docker build -t todo-chatbot-frontend:latest .
cd ..

# Restart deployment to use new image
kubectl rollout restart deployment todo-chatbot-frontend
```

## 12. Clean Up

### Delete Helm Release

```powershell
helm uninstall todo-chatbot
```

### Delete All Resources

```powershell
kubectl delete deployment todo-chatbot-backend
kubectl delete deployment todo-chatbot-frontend
kubectl delete service todo-chatbot-backend
kubectl delete service todo-chatbot-frontend
```

### Stop Minikube

```powershell
minikube stop
```

### Delete Minikube Cluster

```powershell
minikube delete
```

## 13. Useful Monitoring Commands

### Watch Pods in Real-Time

```powershell
kubectl get pods -w
```

### Get Resource Usage

```powershell
kubectl top pods
kubectl top nodes
```

### Get All Resources

```powershell
kubectl get all
```

## 14. Configuration Files

### Helm Values File

Location: `helm/todo-chatbot/values.yaml`

Key configurations:
- Image repository and tags
- Image pull policy (set to `Never` for local images)
- Service types (ClusterIP, NodePort, LoadBalancer)
- Resource limits and requests
- Environment variables

### Deployment Templates

- Backend: `helm/todo-chatbot/templates/backend-deployment.yaml`
- Frontend: `helm/todo-chatbot/templates/frontend-deployment.yaml`

### Service Templates

- Backend: `helm/todo-chatbot/templates/backend-service.yaml`
- Frontend: `helm/todo-chatbot/templates/frontend-service.yaml`

## 15. Common Issues and Solutions

### Issue: Pods in CrashLoopBackOff

**Solution:**
1. Check logs: `kubectl logs <pod-name>`
2. Check events: `kubectl describe pod <pod-name>`
3. Verify image exists: `minikube image ls`
4. Check readiness/liveness probes timeouts

### Issue: ImagePullBackOff

**Solution:**
1. Ensure `imagePullPolicy: Never` in deployment
2. Verify image is built in minikube's Docker: `minikube image ls`
3. Rebuild image in minikube's Docker environment

### Issue: Port Forward Not Working

**Solution:**
1. Verify service exists: `kubectl get svc`
2. Check pod is running: `kubectl get pods`
3. Use correct service name and port
4. Try direct pod port-forward: `kubectl port-forward pod/<pod-name> 3000:3000`

### Issue: Cannot Access via Minikube IP

**Solution:**
On Windows with Docker driver, use port-forwarding instead:
```powershell
kubectl port-forward service/todo-chatbot-frontend 3000:80
```

## 16. Environment Variables

### Backend Environment Variables

Set in `helm/todo-chatbot/templates/backend-deployment.yaml`:
- `DATABASE_URL`: Database connection string
- `OPENAI_API_KEY`: OpenAI API key (from secret)
- `JWT_SECRET`: JWT secret for authentication

### Frontend Environment Variables

Set in `helm/todo-chatbot/templates/frontend-deployment.yaml`:
- `BACKEND_URL`: Backend service URL (e.g., `http://todo-chatbot-backend:8000`)
- `NEXT_PUBLIC_API_BASE_URL`: Public API base URL

## 17. Quick Start Commands

```powershell
# Start minikube
minikube start

# Set Docker environment
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# Build images
cd backend
docker build -t todo-chatbot-backend:latest .
cd ../frontend
docker build -t todo-chatbot-frontend:latest .
cd ..

# Deploy with Helm
helm upgrade --install todo-chatbot ./helm/todo-chatbot

# Wait for pods to be ready
kubectl get pods -w

# Port forward (in separate terminals)
kubectl port-forward service/todo-chatbot-frontend 3000:80
kubectl port-forward service/todo-chatbot-backend 8000:8000

# Access application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

## 18. Production Considerations

For production deployments, consider:

1. **Use proper image registry** (Docker Hub, ECR, GCR)
2. **Set resource limits** appropriately
3. **Configure persistent volumes** for database
4. **Use secrets** for sensitive data
5. **Set up ingress** for external access
6. **Configure horizontal pod autoscaling**
7. **Set up monitoring** (Prometheus, Grafana)
8. **Configure logging** (ELK stack, Loki)
9. **Use production-grade database** (PostgreSQL, MySQL)
10. **Set up CI/CD pipeline** for automated deployments

## Notes

- All commands assume you're running PowerShell on Windows
- Replace `<pod-name>`, `<service-name>`, etc. with actual names from your cluster
- Port-forward processes need to stay running to maintain access
- Images built in minikube's Docker are only available within minikube
