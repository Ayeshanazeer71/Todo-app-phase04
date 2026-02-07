# Minikube Quick Start (OpenRouter + Neon)

The app uses **OpenRouter** (not OpenAI) for the AI chatbot. These values are already set in `helm/todo-chatbot/values.yaml`:

- `OPENROUTER_API_KEY=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`
- `OPENROUTER_MODEL=openai/gpt-4o-mini`
- `OPENROUTER_BASE_URL=https://openrouter.ai/api/v1`

## 1. Start Docker Desktop

Minikube needs Docker. **Start Docker Desktop** and wait until it is fully running.

## 2. Start Minikube and deploy

In PowerShell from the project root:

```powershell
# Start cluster
minikube start

# Use Minikube's Docker so images are built inside the cluster
& minikube -p minikube docker-env --shell powershell | Invoke-Expression

# Build backend
cd backend
docker build -t todo-chatbot-backend:latest .
cd ..

# Build frontend (API URL for port-forward access)
cd frontend
docker build -t todo-chatbot-frontend:latest --build-arg NEXT_PUBLIC_API_URL=http://localhost:8000 --build-arg NEXT_PUBLIC_API_BASE_URL=http://localhost:8000 .
cd ..

# Deploy with Helm (Neon DB + OpenRouter from values.yaml)
helm upgrade --install todo-chatbot ./helm/todo-chatbot --wait --timeout 5m
```

## 3. Access the app

In **two separate terminals** run:

```powershell
# Terminal 1 – frontend
kubectl port-forward service/todo-chatbot-frontend 3000:80

# Terminal 2 – backend
kubectl port-forward service/todo-chatbot-backend 8000:8000
```

Then open:

- **Frontend:** http://localhost:3000  
- **Backend API:** http://localhost:8000  

Backend uses **Neon PostgreSQL**; tables are created automatically on first start. The chatbot uses **OpenRouter** with the credentials above.

## One-line script (after Docker is running)

```powershell
.\scripts\deploy-minikube.ps1
```

Then run the two `kubectl port-forward` commands above.
