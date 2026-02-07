# Phase IV Execution Plan

## Overview

This plan outlines the step-by-step execution for deploying the existing Phase III Todo Chatbot application to a local Kubernetes cluster using Minikube, Helm charts, and Docker containers. The implementation will follow agentic development practices using AI agents (Gordon, kubectl-ai, kagent) as specified in the constitution.

## Technical Context

- **Application Components**: Frontend (UI) and Backend (API server) from Phase III
- **Target Platform**: Local Minikube Kubernetes cluster
- **Containerization Tool**: Gordon (Docker AI Agent)
- **Orchestration Tool**: Helm charts for deployment management
- **Required Images**: `todo-chatbot-frontend:latest` and `todo-chatbot-backend:latest`
- **Service Configuration**: ClusterIP for backend, NodePort/LoadBalancer for frontend
- **Resource Requirements**: CPU 100m request/500m limit, Memory 128Mi request/512Mi limit

## Constitution Check

This plan adheres to all constitutional principles:
- ✅ Agentic Development Only: All steps use AI agents (Gordon, kubectl-ai, kagent)
- ✅ Spec-Driven Development: Derived exclusively from constitution.md and spec.md
- ✅ Local-Only Deployment: Target is local Minikube cluster
- ✅ Zero Manual Intervention: Prefer AI-assisted tools over raw CLI
- ✅ Containerization with Docker: Use Gordon for all Docker operations
- ✅ Kubernetes Orchestration: Via Minikube with Helm charts mandatory
- ✅ Application Component Separation: Frontend and backend as separate deployments
- ✅ Helm Chart Mandatory: All deployments use Helm charts
- ✅ Quality & Safety Validation: Agents validate changes at each step
- ✅ Minimal Configuration: For local development and learning

## Phases

### Phase 0: Environment Preparation and Research

#### Task 0.1: Verify Prerequisites
- **Agent**: Bash
- **Action**: Check if Minikube, Docker, and Helm are installed and running
- **Expected Output**: Confirmation that prerequisites are met
- **Verification**: Validate Minikube cluster is accessible

#### Task 0.2: Research Application Structure
- **Agent**: Claude Code (Explore)
- **Action**: Examine Phase III application structure to understand frontend/backend separation, ports, and dependencies
- **Expected Output**: `research.md` with findings on application architecture
- **Verification**: Clear understanding of both components' requirements

### Phase 1: Containerization

#### Task 1.1: Generate Frontend Dockerfile
- **Agent**: Gordon (Docker AI Agent)
- **Prompt**: "Create a Dockerfile for the frontend component of the Todo Chatbot application using minimal, secure base images (node:alpine). Copy necessary Phase III source files, install dependencies from package.json, expose the correct port (likely 3000), and define appropriate ENTRYPOINT/CMD to run the app"
- **Expected Output**: `frontend/Dockerfile`
- **Verification**: Gordon confirms Dockerfile is created with appropriate content

#### Task 1.2: Generate Backend Dockerfile
- **Agent**: Gordon (Docker AI Agent)
- **Prompt**: "Create a Dockerfile for the backend component of the Todo Chatbot application using minimal, secure base images (python:slim or node:alpine). Copy necessary Phase III source files, install dependencies from requirements.txt/package.json, expose the correct port (likely 5000/8000), and define appropriate ENTRYPOINT/CMD to run the app"
- **Expected Output**: `backend/Dockerfile`
- **Verification**: Gordon confirms Dockerfile is created with appropriate content

#### Task 1.3: Build Frontend Image
- **Agent**: Gordon (Docker AI Agent)
- **Prompt**: "Build the frontend Docker image with tag todo-chatbot-frontend:latest using the Dockerfile in the frontend directory"
- **Expected Output**: Successfully built `todo-chatbot-frontend:latest` image
- **Verification**: Gordon verifies the image exists and can run

#### Task 1.4: Build Backend Image
- **Agent**: Gordon (Docker AI Agent)
- **Prompt**: "Build the backend Docker image with tag todo-chatbot-backend:latest using the Dockerfile in the backend directory"
- **Expected Output**: Successfully built `todo-chatbot-backend:latest` image
- **Verification**: Gordon verifies the image exists and can run

#### Task 1.5: Test Local Container Operation
- **Agent**: Gordon (Docker AI Agent)
- **Prompt**: "Run both frontend and backend containers locally to verify they start correctly and are accessible"
- **Expected Output**: Both containers running and accessible locally
- **Verification**: Confirm containers start without errors and respond to requests

### Phase 2: Helm Chart Creation

#### Task 2.1: Create Helm Chart Structure
- **Agent**: kubectl-ai or kagent
- **Prompt**: "Create a Helm chart named 'todo-chatbot' with version 0.1.0 and appVersion 1.0. Include proper Chart.yaml metadata"
- **Expected Output**: `helm/todo-chatbot/` directory with Chart.yaml
- **Verification**: Valid Helm chart structure created

#### Task 2.2: Create Frontend Deployment Template
- **Agent**: kubectl-ai or kagent
- **Prompt**: "Create a Kubernetes Deployment template for the frontend component in the Helm chart templates directory. Configure with 2 replicas by default, use the todo-chatbot-frontend:latest image, set resource requests/limits (CPU: 100m request/500m limit, Memory: 128Mi request/512Mi limit), and include readiness/liveness probes"
- **Expected Output**: `helm/todo-chatbot/templates/frontend-deployment.yaml`
- **Verification**: Template is valid and follows Kubernetes best practices

#### Task 2.3: Create Backend Deployment Template
- **Agent**: kubectl-ai or kagent
- **Prompt**: "Create a Kubernetes Deployment template for the backend component in the Helm chart templates directory. Configure with 1 replica by default, use the todo-chatbot-backend:latest image, set resource requests/limits (CPU: 100m request/500m limit, Memory: 128Mi request/512Mi limit), and include readiness/liveness probes"
- **Expected Output**: `helm/todo-chatbot/templates/backend-deployment.yaml`
- **Verification**: Template is valid and follows Kubernetes best practices

#### Task 2.4: Create Frontend Service Template
- **Agent**: kubectl-ai or kagent
- **Prompt**: "Create a Kubernetes Service template for the frontend component in the Helm chart templates directory. Use NodePort or LoadBalancer type for external access via Minikube, mapping appropriate ports"
- **Expected Output**: `helm/todo-chatbot/templates/frontend-service.yaml`
- **Verification**: Service template allows external access to frontend

#### Task 2.5: Create Backend Service Template
- **Agent**: kubectl-ai or kagent
- **Prompt**: "Create a Kubernetes Service template for the backend component in the Helm chart templates directory. Use ClusterIP type for internal access only, mapping appropriate ports"
- **Expected Output**: `helm/todo-chatbot/templates/backend-service.yaml`
- **Verification**: Service template allows internal access to backend

#### Task 2.6: Create Default Values File
- **Agent**: kubectl-ai or kagent
- **Prompt**: "Create a values.yaml file for the Helm chart with configurable defaults: frontend replica count (2), backend replica count (1), image tags (todo-chatbot-frontend:latest, todo-chatbot-backend:latest), ports, and resource limits"
- **Expected Output**: `helm/todo-chatbot/values.yaml`
- **Verification**: Values file contains appropriate defaults and is well-structured

### Phase 3: Deployment and Validation

#### Task 3.1: Install Helm Chart to Minikube
- **Agent**: kubectl-ai or kagent
- **Prompt**: "Install the todo-chatbot Helm chart to the local Minikube cluster"
- **Expected Output**: Successful installation with release name
- **Verification**: Helm release is created and active

#### Task 3.2: Verify Pod Status
- **Agent**: kubectl-ai
- **Prompt**: "Check the status of all pods in the current namespace"
- **Expected Output**: All pods in Running/Ready state
- **Verification**: All frontend and backend pods show Ready status

#### Task 3.3: Verify Service Accessibility
- **Agent**: kubectl-ai
- **Prompt**: "Get the frontend service URL using minikube service command"
- **Expected Output**: Accessible URL for the frontend service
- **Verification**: Frontend is accessible via the provided URL

#### Task 3.4: Validate Application Functionality
- **Agent**: kubectl-ai or kagent
- **Prompt**: "Check that all core Phase III features work end-to-end by examining pod logs and verifying functionality"
- **Expected Output**: Confirmation that all core features work as expected
- **Verification**: Application behaves identically to Phase III

#### Task 3.5: Test Scaling Operations
- **Agent**: kubectl-ai
- **Prompt**: "Scale the frontend deployment to 4 replicas to verify scalability"
- **Expected Output**: Frontend deployment scaled to 4 replicas
- **Verification**: 4 frontend pods running and accessible

### Phase 4: Final Verification and Documentation

#### Task 4.1: Generate Common Operation Commands
- **Agent**: kubectl-ai or kagent
- **Prompt**: "Provide commands for common operations: scaling frontend/backend, checking logs, viewing cluster health"
- **Expected Output**: List of operational commands for managing the deployment
- **Verification**: Commands are functional and well-documented

#### Task 4.2: Final Health Check
- **Agent**: kagent
- **Prompt**: "Perform a comprehensive health check of the entire deployment including resource usage, pod status, and service connectivity"
- **Expected Output**: Full health report of the deployed application
- **Verification**: All components are healthy and within resource limits

## Verification

The following acceptance criteria from the specification must be verified:

- [ ] Both Docker images build and run locally (verified by Gordon)
- [ ] Helm chart installs successfully on Minikube
- [ ] `kubectl get pods` shows all pods Ready
- [ ] Frontend URL (from `minikube service`) loads the Todo Chatbot UI
- [ ] All core Phase III features work end-to-end
- [ ] Commands for common operations are provided:
  - [ ] Scale frontend/backend
  - [ ] Check logs
  - [ ] View cluster health (via kagent)

## Next Steps

Following this plan, the implementation should proceed with creating detailed tasks in `tasks.md` that break down each phase into specific, executable steps. The tasks should include specific prompts for each AI agent and clear acceptance criteria for each deliverable.