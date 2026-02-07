---
id: 1
title: Update Kubernetes Deployment Constitution
stage: constitution
date: 2026-01-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: /sp.constitution
labels: [constitution, kubernetes, deployment, containerization]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
---

## Prompt

```text
# Project Constitution

This document defines the immutable principles, constraints, and rules that all AI agents (Claude Code, Gordon, kubectl-ai, kagent, etc.) **must** follow during implementation of Phase IV: Local Kubernetes Deployment of the Cloud Native Todo Chatbot.

Violating any rule requires explicit human approval and an update to this constitution.

## Core Principles
- **Agentic Development Only**: No manual coding or direct editing of generated files. All implementation must be done via AI agents (Claude Code for planning/tasks, Gordon for Docker operations, kubectl-ai and/or kagent for Kubernetes/Helm operations).
- **Spec-Driven**: All work must derive from approved specifications. Agents must reference this constitution and other spec files before generating or modifying code/infrastructure.
- **Local-Only Deployment**: Everything runs on a local Minikube cluster. No cloud providers, no remote registries unless explicitly for learning/demo purposes.
- **Zero Manual Intervention Preference**: Prefer AI-assisted tools (Gordon, kubectl-ai, kagent) over raw CLI commands. Fall back to standard Docker/kubectl/helm CLI only if the AI agent is unavailable.

## Required Technology Stack
-12 **Containerization**: Docker (via Docker Desktop)
  - Primary: Use Docker AI Agent (Gordon) for all Docker operations (Dockerfile generation, build, run, push if needed).
  - Fallback: Standard Docker CLI only if Gordon is unavailable.
- **Orchestration**: Kubernetes via Minikube
- **Packaging & Deployment**: Helm charts (must be generated and used for all deployments)
- **AI DevOps Tools**:
  - kubectl-ai (primary for simple Kubernetes operations)
  - kagent (for advanced analysis, optimization, health checks)
  - Gordon (for intelligent Docker operations)
- **Application Base**: Phase III Todo Chatbot (existing frontend and backend code must be containerized without modification unless specified)

## Architectural Rules
- The application consists of at least two components:
  - Frontend (web/UI for Todo Chatbot)
  - Backend (API/server for todo logic and chatbot functionality)
- Each component **must** have its own Docker image.
- Each component **must** be deployed as separate Kubernetes Deployments with appropriate Services.
- Use Helm chart(s) to manage:
  - Deployments
  - Services (ClusterIP for backend, NodePort/LoadBalancer for frontend access via Minikube)
  - ConfigMaps/Secrets if needed
  - Resource limits/requests (reasonable defaults for local development)
- Default replica count: 1 for backend, 2 for frontend (scalable via AI agents later)

## Constraints & Forbidden Practices
- Do not use raw kubectl apply/manifests without Helm.
- Do not push images to remote registries unless explicitly requested.
- Do not install additional Kubernetes operators or CRDs unless required for basic functionality.
- Do not modify Phase III application source code (only containerize it).
- All generated files (Dockerfiles, Helm charts, values.yaml) must include comments explaining AI agent decisions.

## Quality & Safety Rules
- Agents must validate every change:
  - Gordon: Verify images build and run locally.
  - kubectl-ai/kagent: Check pod status, logs, and cluster health after deployment.
- Prefer readable, minimal configurations suitable for local development and learning.
- Include basic readiness/liveness probes in deployments.

## Workflow Enforcement
- Start from spec files only.
- Generate plan → tasks → implementation via agents.
- After each major step, agent must summarize what was done and suggest verification commands (e.g., `minikube service`, `kubectl get pods`).

This constitution may only be updated by human review.
```

## Response snapshot

Created a new project constitution for the Phase IV: Local Kubernetes Deployment of the Cloud Native Todo Chatbot, replacing the previous constitution for a different project. The new constitution establishes 10 core principles covering agentic development, spec-driven approach, local deployment, containerization, Kubernetes orchestration, and quality validation.

## Outcome

- ✅ Impact: Successfully replaced the old constitution with a new one tailored for Kubernetes deployment project
- 🧪 Tests: No tests needed for constitution creation
- 📁 Files: Updated .specify/memory/constitution.md with new Kubernetes-focused principles
- 🔁 Next prompts: Plan and implement the Kubernetes deployment based on the new constitution
- 🧠 Reflection: The new constitution properly addresses all requirements for the Phase IV project including containerization, orchestration, and AI agent usage

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - Constitution properly created with all required principles
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin implementing the Kubernetes deployment plan