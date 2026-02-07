---
id: 2
title: Create K8s Deployment Spec
stage: spec
date: 2026-01-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: k8s-deployment
branch: 1-k8s-deployment
user: user
command: /sp.specify
labels: [specification, kubernetes, deployment, containerization]
links:
  spec: specs/1-k8s-deployment/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-k8s-deployment/spec.md
 - specs/1-k8s-deployment/checklists/requirements.md
 - .specify/memory/constitution.md
tests:
---

## Prompt

```text
# Phase IV Specification: Local Kubernetes Deployment of Cloud Native Todo Chatbot

This specification details **what** must be built and delivered for Phase IV. All AI agents (Claude Code, Gordon, kubectl-ai, kagent) must derive their work exclusively from this document and the constitution.md. No assumptions outside these specs are allowed without human approval.

## Project Overview
Deploy the existing Phase III Todo Chatbot (frontend + backend) as a cloud-native application on a local Minikube Kubernetes cluster using Helm charts for packaging and deployment. All operations must be performed agentically using Gordon, kubectl-ai, and/or kagent. No manual coding or direct CLI usage unless the AI tool is unavailable.

## Core Components
The application consists of exactly two independently containerized and deployable components from Phase III:

1. **Frontend**
   - Web-based UI for the Todo Chatbot.
   - Serves the user interface (likely React/Vite/Next.js or similar static + client code).
   - Exposes a web port (default: 3000 or as in Phase III).
   - Must be accessible externally via Minikube (NodePort or LoadBalancer service).

2. **Backend**
   - API server handling todo logic, persistence, and chatbot functionality.
   - Exposes an API port (default: 5000/8000 or as in Phase III).
   - Communicates with frontend via HTTP/REST or WebSocket if required.
   - Internal access only (ClusterIP service).

No new features are to be added. Only containerization and orchestration of existing code.

## Functional Requirements

### 1. Containerization (via Gordon)
- Generate one Dockerfile per component (frontend and backend).
- Dockerfiles must:
  - Use minimal, secure base images (e.g., node:alpine for frontend, python:slim or node:alpine for backend).
  - Copy only necessary Phase III source files.
  - Install exact dependencies from Phase III (package.json, requirements.txt, etc.).
  - Expose the correct ports.
  - Define appropriate ENTRYPOINT/CMD to run the app (e.g., `npm start`, `python app.py`).
- Build two images locally:
  - `todo-chatbot-frontend:latest`
  - `todo-chatbot-backend:latest`
- Images must run successfully in Docker locally before Kubernetes deployment.
- No remote registry push required.

### 2. Helm Chart Creation (via kubectl-ai and/or kagent)
- Generate a single Helm chart (umbrella chart) named `todo-chatbot` that includes subcharts or templates for both components.
- Chart structure must include:
  - `Chart.yaml` with appropriate metadata (name, version 0.1.0, appVersion 1.0).
  - `values.yaml` with configurable defaults (replicas, image tags, ports, resource limits, etc.).
  - Templates:
    - Deployment for frontend (default 2 replicas).
    - Deployment for backend (default 1 replica).
    - Service for frontend (NodePort or LoadBalancer for Minikube access).
    - Service for backend (ClusterIP).
    - Optional: ConfigMap for environment variables, basic readiness/liveness probes.
- Resource requests/limits (reasonable for local dev):
  - CPU: 100m request / 500m limit
  - Memory: 128Mi request / 512Mi limit
- Probes: Simple HTTP GET on health/check endpoint if exists, or TCP socket probe on app port.

### 3. Deployment on Minikube
- Cluster: Running Minikube with default driver (Docker or Hyper-V as appropriate).
- Install Helm chart using AI-assisted commands.
- Post-deployment:
  - All pods must reach Running/Ready state.
  - Frontend must be accessible via `minikube service` URL.
  - Basic functionality (add/view todos, chatbot interaction) must work exactly as in Phase III.

## Non-Functional Requirements
- **Local Only**: No cloud resources, no external dependencies.
- **Observability**: Include basic labels and annotations for easy querying with kubectl-ai/kagent.
- **Scalability Demo Ready**: Configuration must allow easy scaling commands (e.g., `kubectl-ai "scale frontend to 4 replicas"`).
- **Reproducibility**: All generated artifacts (Dockerfiles, Helm files) must be committed to the repo.
- **Validation**: After deployment, agents must run health checks and provide verification commands.

## Acceptance Criteria
The phase is complete when an agent can confirm:
1. Both Docker images build and run locally (verified by Gordon).
2. Helm chart installs successfully on Minikube.
3. `kubectl get pods` shows all pods Ready.
4. Frontend URL (from `minikube service`) loads the Todo Chatbot UI.
5. All core Phase III features work end-to-end.
6. Commands for common operations are provided:
   - Scale frontend/backend
   - Check logs
   - View cluster health (via kagent)

## Out of Scope
- Persistent storage (PVCs) unless Phase III requires it.
- Ingress controller.
- Advanced monitoring (Prometheus, etc.).
- CI/CD pipelines.
- Any code changes to Phase III application.

Agents generating plans or implementations must quote relevant sections of this specification in their reasoning.
```

## Response snapshot

Successfully created a comprehensive specification for the Local Kubernetes Deployment of Cloud Native Todo Chatbot. The specification includes:
- Overview and business context
- Clear scope with inclusions and exclusions
- Key entities identification
- Three detailed user scenarios with testing flows
- Five functional requirements with acceptance criteria
- Three non-functional requirements
- Measurable success criteria
- Assumptions and dependencies sections

Also created a quality checklist to validate the specification completeness. Created a new git branch '1-k8s-deployment' and placed the spec in 'specs/1-k8s-deployment/spec.md'.

## Outcome

- ✅ Impact: Complete specification created for Kubernetes deployment project with all required sections
- 🧪 Tests: No functional tests needed for specification creation
- 📁 Files: Created specs/1-k8s-deployment/spec.md and specs/1-k8s-deployment/checklists/requirements.md
- 🔁 Next prompts: Ready to proceed with planning using /sp.plan
- 🧠 Reflection: Specification properly abstracts implementation details while maintaining clear requirements

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - Specification meets all required criteria
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin planning phase with /sp.plan