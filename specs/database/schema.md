# Database Schema: Phase II & III

Using Neon PostgreSQL with SQLModel.

## Tables

### Users (managed by Better Auth)
Extends or interfaces with the default Better Auth schema.

### Tasks
- `id`: Integer (Primary Key, Auto-increment)
- `title`: String (VARCHAR, NOT NULL)
- `description`: String (TEXT, NULLABLE)
- `completed`: Boolean (Default: FALSE)
- `user_id`: String (Foreign Key to User, Indexed)

### Conversations (Phase III)
- `id`: UUID (Primary Key, Default: gen_random_uuid())
- `user_id`: String (Foreign Key to User, NOT NULL, Indexed)
- `created_at`: Timestamp (Default: NOW())
- `updated_at`: Timestamp (Default: NOW(), Updated on modification)

### Messages (Phase III)
- `id`: Integer (Primary Key, Auto-increment)
- `conversation_id`: UUID (Foreign Key to Conversations, NOT NULL, Indexed)
- `role`: Enum ('user', 'assistant') (NOT NULL)
- `content`: Text (NOT NULL)
- `tool_calls`: JSONB (NULLABLE) - Stores tool call details for assistant messages
- `created_at`: Timestamp (Default: NOW())

## Relationships

### Phase II
- `Tasks.user_id` → `Users.id` (Many-to-One)

### Phase III
- `Conversations.user_id` → `Users.id` (Many-to-One)
- `Messages.conversation_id` → `Conversations.id` (Many-to-One, CASCADE DELETE)

## Indexes

### Existing (Phase II)
- `idx_tasks_user_id` ON `Tasks(user_id)` - Efficient user task filtering

### New (Phase III)
- `idx_conversations_user_id` ON `Conversations(user_id)` - Efficient user conversation filtering
- `idx_conversations_updated_at` ON `Conversations(updated_at)` - Recent conversations sorting
- `idx_messages_conversation_id` ON `Messages(conversation_id)` - Efficient message retrieval
- `idx_messages_created_at` ON `Messages(created_at)` - Chronological message ordering

## Ownership Enforcement

### Phase II Rules
- Every query MUST filter by `user_id`.
- Indexes: `idx_tasks_user_id` for efficient filtering.

### Phase III Rules
- **Conversations**: Users can only access conversations where `user_id` matches their JWT identity
- **Messages**: Access controlled through conversation ownership (users can only see messages from their conversations)
- **Cascade Deletion**: When a conversation is deleted, all associated messages are automatically removed
- **Data Isolation**: All queries MUST include user_id filtering at the conversation level

## Data Retention Policies

### Conversations
- No automatic deletion (user-controlled)
- Consider implementing optional auto-cleanup for conversations older than X months
- Soft delete option for conversation recovery

### Messages
- Retained as long as parent conversation exists
- Consider implementing message count limits per conversation (e.g., 1000 messages)
- Tool call data stored in JSONB for efficient querying and analysis

## Performance Considerations

### Query Optimization
- Always use indexes when filtering by user_id
- Limit message retrieval with pagination (default 50 messages per request)
- Use conversation.updated_at for efficient "recent conversations" queries

### Storage Optimization
- Consider partitioning Messages table by created_at for large datasets
- Monitor JSONB tool_calls column size and consider compression if needed
- Regular VACUUM and ANALYZE operations for optimal performance
