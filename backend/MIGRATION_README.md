# Database Migration Guide - Phase III

This document explains how to set up and run database migrations for the Phase III chat functionality.

## Overview

Phase III adds two new tables to support the AI chatbot feature:
- `conversations`: Stores conversation metadata with user isolation
- `messages`: Stores individual chat messages with tool call data

## Migration Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install Alembic along with other dependencies.

### 2. Environment Variables

Ensure your `DATABASE_URL` environment variable is set:

```bash
export DATABASE_URL="postgresql://username:password@host:port/database"
```

### 3. Run Migrations

#### Option A: Using the migration script (Recommended)
```bash
cd backend
python migrate.py
```

#### Option B: Using Alembic directly
```bash
cd backend
alembic upgrade head
```

#### Option C: For development/testing only
```bash
# This will create all tables including new chat tables
# Use only for local development
python -c "from src.app.core.database import create_all_tables; create_all_tables()"
```

## Migration Details

### New Tables Created

#### conversations
- `id`: UUID primary key (auto-generated)
- `user_id`: String, foreign key to users, indexed
- `created_at`: Timestamp with default NOW()
- `updated_at`: Timestamp with default NOW(), updated on modification

#### messages
- `id`: Integer primary key (auto-increment)
- `conversation_id`: UUID, foreign key to conversations.id, indexed
- `role`: Enum ('user', 'assistant')
- `content`: Text (message content)
- `tool_calls`: JSONB (nullable, stores tool call details)
- `created_at`: Timestamp with default NOW()

### Indexes Created

For optimal performance:
- `ix_conversation_user_id`: On conversations.user_id
- `ix_conversation_updated_at`: On conversations.updated_at  
- `ix_message_conversation_id`: On messages.conversation_id
- `ix_message_created_at`: On messages.created_at

### Relationships

- `conversations.user_id` → `users.id` (Many-to-One)
- `messages.conversation_id` → `conversations.id` (Many-to-One, CASCADE DELETE)

## User Isolation

All queries MUST filter by user_id at the conversation level to ensure proper data isolation:

```python
# Correct: Filter conversations by user_id
conversations = session.exec(
    select(Conversation).where(Conversation.user_id == current_user_id)
).all()

# Messages are automatically isolated through conversation ownership
messages = session.exec(
    select(Message)
    .join(Conversation)
    .where(Conversation.user_id == current_user_id)
).all()
```

## Rollback

To rollback the migration:

```bash
cd backend
alembic downgrade base
```

**Warning**: This will delete all conversation and message data!

## Troubleshooting

### Migration Fails
1. Check DATABASE_URL is correct
2. Ensure database exists and is accessible
3. Verify user has CREATE TABLE permissions

### Import Errors
1. Ensure you're running from the backend directory
2. Check that all model imports are working
3. Verify Python path includes src directory

### Performance Issues
1. Verify indexes were created properly
2. Check query plans include user_id filtering
3. Monitor JSONB column size for tool_calls data