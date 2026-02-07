# Phase III: Todo AI Chatbot

A full-stack todo application with AI-powered natural language task management using OpenAI Agents SDK and Model Context Protocol (MCP) tools.

## Features

### Phase II (Existing)
- ✅ User authentication with Better Auth
- ✅ CRUD operations for tasks
- ✅ Task categories, priorities, and subtasks
- ✅ Drag-and-drop task reordering
- ✅ Responsive design with Tailwind CSS

### Phase III (New)
- 🤖 AI-powered chatbot for natural language task management
- 💬 Conversation persistence and history
- 🔧 MCP tools for task operations
- 🎨 OpenAI ChatKit integration for professional chat UI
- 🔒 Stateless design with JWT-based user isolation

## Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLModel** - Type-safe database operations
- **Neon PostgreSQL** - Serverless PostgreSQL database
- **OpenAI Agents SDK** - AI agent runtime
- **MCP SDK** - Model Context Protocol tools
- **Alembic** - Database migrations

### Frontend
- **Next.js 16+** - React framework with App Router
- **Better Auth** - Authentication system
- **OpenAI ChatKit** - Chat interface components
- **Tailwind CSS** - Utility-first styling
- **TypeScript** - Type safety

## Environment Variables

### Backend Configuration

Copy `backend/.env.example` to `backend/.env` and configure:

```bash
# Database (choose one)
DATABASE_URL=sqlite:///./test.db  # For local development
# DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db  # For production

# Authentication (MUST match frontend)
BETTER_AUTH_SECRET=your_strong_secret_here  # Generate with: openssl rand -hex 32

# OpenAI (Required for AI chatbot)
OPENAI_API_KEY=sk-your-openai-key-here  # Get from https://platform.openai.com/api-keys

# Optional
MCP_SERVER_PORT=8001
OPENAI_ORGANIZATION_ID=org-your-org-id
```

### Frontend Configuration

Copy `frontend/.env.local.example` to `frontend/.env.local` and configure:

```bash
# Backend API
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api

# Authentication (MUST match backend)
BETTER_AUTH_SECRET=your_strong_secret_here  # Same as backend

# Better Auth
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_TRUST_HOST=true
```

### Security Notes

1. **Generate Strong Secrets**: Use `openssl rand -hex 32` to generate secure secrets
2. **Match Secrets**: `BETTER_AUTH_SECRET` must be identical in backend and frontend
3. **Never Commit**: Add `.env` and `.env.local` to `.gitignore` (already configured)
4. **OpenAI API Key**: Required for Phase III AI chatbot functionality
5. **Database URL**: Use Neon PostgreSQL for production, SQLite for local development

## Quick Start

### Prerequisites
- Node.js 18+ and npm/yarn
- Python 3.8+ and pip
- OpenAI API key (for Phase III features)
- Neon PostgreSQL database (for production)

### 1. Clone and Setup
```bash
git clone <repository-url>
cd todo-phase3
```

### 2. Backend Setup
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your actual values

# Run database migrations
python migrate.py
# OR: alembic upgrade head

# Start development server
cd src
python -m uvicorn app.main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local with your actual values

# Start development server
npm run dev
```

### 4. Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Development Workflow

### Database Migrations
```bash
# Create new migration
cd backend
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Running Tests
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

### Phase III Chat Features

The AI chatbot supports natural language commands:
- **Create tasks**: "Add a task to buy groceries"
- **List tasks**: "What do I need to do today?"
- **Complete tasks**: "Mark the grocery task as done"
- **Update tasks**: "Change the title of task 1 to 'Buy organic groceries'"
- **Delete tasks**: "Remove the completed tasks"

## Project Structure

```
todo-phase3/
├── backend/                 # FastAPI backend
│   ├── src/app/
│   │   ├── api/            # API routes
│   │   ├── models/         # SQLModel classes
│   │   ├── services/       # Business logic
│   │   ├── agents/         # OpenAI Agents SDK (Phase III)
│   │   └── mcp_server/     # MCP tools (Phase III)
│   ├── alembic/            # Database migrations
│   └── requirements.txt
├── frontend/               # Next.js frontend
│   ├── src/
│   │   ├── app/           # App Router pages
│   │   ├── components/    # React components
│   │   └── services/      # API clients
│   └── package.json
└── specs/                 # Technical specifications
    ├── features/          # Feature requirements
    ├── api/              # API documentation
    ├── database/         # Database schema
    └── ui/               # UI specifications
```

## Contributing

1. Follow the spec-driven development workflow
2. Update specifications before implementation
3. Run tests before submitting changes
4. Use conventional commit messages

## License

MIT License - see LICENSE file for details