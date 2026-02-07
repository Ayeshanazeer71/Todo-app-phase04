# Quick Start Guide - Todo Chatbot with OpenRouter

## 🚀 Access Your Application

Your Todo Chatbot is now running in Minikube with OpenRouter AI integration!

### Access URLs

- **Frontend (Web UI):** http://localhost:3000
- **Backend API:** http://localhost:8000
- **Health Check:** http://localhost:8000/health

---

## 📋 Current Status

✅ **Minikube:** Running
✅ **Backend Pod:** 1/1 Running (with OpenRouter)
✅ **Frontend Pods:** 2/2 Running
✅ **Port Forwarding:** Active
✅ **OpenRouter API:** Configured & Working

---

## 🎯 How to Use

### 1. Open the Application
```
Open your browser and go to: http://localhost:3000
```

### 2. Sign Up / Login
- Click "Sign Up" to create a new account
- Or "Login" if you already have an account
- Username: any username you choose
- Password: any password you choose

### 3. Start Chatting
- Navigate to the Chat page
- Talk naturally to the AI assistant
- Examples:
  - "I need to buy groceries tomorrow"
  - "What tasks do I have?"
  - "Mark task 1 as complete"
  - "Show me all my tasks"

### 4. Manage Tasks
The AI can help you:
- ✅ Create new tasks
- ✅ List your tasks
- ✅ Update task details
- ✅ Mark tasks as complete
- ✅ Delete tasks

---

## 🔧 Management Commands

### Check Status
```powershell
# Check all resources
kubectl get all

# Check pods
kubectl get pods

# Check services
kubectl get services
```

### View Logs
```powershell
# Backend logs
kubectl logs -f deployment/todo-chatbot-backend

# Frontend logs
kubectl logs -f deployment/todo-chatbot-frontend
```

### Restart Services
```powershell
# Restart backend
kubectl rollout restart deployment todo-chatbot-backend

# Restart frontend
kubectl rollout restart deployment todo-chatbot-frontend
```

### Stop Port Forwarding
If you need to stop the port forwarding:
1. Find the PowerShell windows running port-forward
2. Press Ctrl+C in each window

### Restart Port Forwarding
```powershell
# Frontend
kubectl port-forward service/todo-chatbot-frontend 3000:80

# Backend (in another terminal)
kubectl port-forward service/todo-chatbot-backend 8000:8000
```

---

## 🛠️ Troubleshooting

### Application Not Loading
1. Check if port-forward is running
2. Verify pods are running: `kubectl get pods`
3. Check logs: `kubectl logs <pod-name>`

### Chat Not Responding
1. Check backend logs: `kubectl logs deployment/todo-chatbot-backend`
2. Verify OpenRouter API key is configured
3. Check network connectivity

### Pods Not Starting
```powershell
# Describe pod to see errors
kubectl describe pod <pod-name>

# Check events
kubectl get events --sort-by=.metadata.creationTimestamp
```

---

## 🔄 Update Application

### Update Backend Code
```powershell
# Set Docker environment
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# Rebuild image
cd backend
docker build -t todo-chatbot-backend:latest .

# Restart deployment
kubectl rollout restart deployment todo-chatbot-backend
```

### Update Frontend Code
```powershell
# Set Docker environment
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# Rebuild image
cd frontend
docker build -t todo-chatbot-frontend:latest .

# Restart deployment
kubectl rollout restart deployment todo-chatbot-frontend
```

---

## 🛑 Stop Everything

### Stop Port Forwarding
Press Ctrl+C in the terminal windows running port-forward

### Stop Minikube
```powershell
minikube stop
```

### Delete Everything
```powershell
# Delete Helm release
helm uninstall todo-chatbot

# Or delete minikube cluster
minikube delete
```

---

## 🔐 Configuration

### OpenRouter Settings
- **API Key:** Configured in Helm values
- **Model:** openai/gpt-4o-mini
- **Base URL:** https://openrouter.ai/api/v1

### Change OpenRouter Model
Edit `helm/todo-chatbot/values.yaml`:
```yaml
backend:
  openrouter:
    model: "openai/gpt-4o-mini"  # Change this
```

Then upgrade:
```powershell
helm upgrade todo-chatbot ./helm/todo-chatbot
kubectl rollout restart deployment todo-chatbot-backend
```

---

## 📊 Monitoring

### Check Resource Usage
```powershell
kubectl top pods
kubectl top nodes
```

### Watch Pods in Real-Time
```powershell
kubectl get pods -w
```

### Check Deployment Status
```powershell
kubectl rollout status deployment/todo-chatbot-backend
kubectl rollout status deployment/todo-chatbot-frontend
```

---

## 🎉 Features

### AI-Powered Chat
- Natural language understanding
- Context-aware responses
- Task management through conversation

### Task Management
- Create tasks via chat
- List and filter tasks
- Update task details
- Mark tasks complete
- Delete tasks

### Authentication
- Secure JWT-based auth
- User registration
- Login/logout

---

## 📝 Notes

- **Database:** Using SQLite (ephemeral, data lost on pod restart)
- **Images:** Built locally in Minikube
- **Network:** Port-forwarding required for access on Windows
- **AI Model:** Using OpenRouter's openai/gpt-4o-mini

---

## 🆘 Need Help?

### Check Logs
```powershell
# All backend logs
kubectl logs deployment/todo-chatbot-backend --tail=100

# Follow logs in real-time
kubectl logs -f deployment/todo-chatbot-backend
```

### Verify Configuration
```powershell
# Check environment variables
kubectl describe pod <backend-pod-name> | Select-String -Pattern "Environment"

# Check Helm values
helm get values todo-chatbot
```

### Test API Directly
```powershell
# Health check
curl http://localhost:8000/health

# API docs
# Open: http://localhost:8000/docs
```

---

## ✅ Success Checklist

- [ ] Minikube is running
- [ ] All pods are in "Running" status
- [ ] Port forwarding is active
- [ ] Frontend loads at http://localhost:3000
- [ ] Backend health check passes
- [ ] Can sign up / login
- [ ] Chat responds to messages
- [ ] Tasks can be created via chat

---

**Everything is ready! Start using your AI-powered Todo Chatbot! 🎉**
