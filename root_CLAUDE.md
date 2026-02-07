# Phase II Todo Web App - Monorepo

## Project Structure

- `backend/`: FastAPI + SQLModel (Neon PostgreSQL)
- `frontend/`: Next.js 16+ + Better Auth + Tailwind
- `specs/`: Service and Feature specifications
  - `specs/overview.md`: Project summary
  - `specs/api/`: REST API documentation
  - `specs/database/`: Database schema
  - `specs/ui/`: UI components and page structure
  - `specs/features/`: Functional requirements

## Phase III: Todo AI Chatbot

### Overview
Integration of OpenAI Agents SDK, Official MCP SDK for tools, OpenAI ChatKit for UI, stateless chat endpoint, conversation persistence in Neon DB.

### Key Components
- **OpenAI Agents SDK**: AI agent runner for natural language task management
- **MCP SDK**: Model Context Protocol tools for task operations
- **OpenAI ChatKit**: React UI components for chat interface
- **Stateless Design**: JWT-based user isolation and session management
- **Conversation Persistence**: Chat history stored in Neon PostgreSQL

### Workflow Note
All Phase III work must reference new specs in `/specs/features/chatbot.md`, `/specs/api/mcp-tools.md`, and related files. Emphasize stateless design, user isolation via JWT, and natural language task management.

## Workflows

1. **Spec-Driven Development**: Always update/read specs in `specs/` before implementation.
2. **PHR Tracking**: Every prompt interaction is recorded in `history/prompts/`.
3. **ADR Usage**: Significant architectural decisions are documented in `history/adr/`.

## Reference Commands

- `/sp.spec`: Update specifications
- `/sp.plan`: Create implementation plans
- `/sp.tasks`: Generate tasks from plans
- `/sp.implement`: Execute tasks
