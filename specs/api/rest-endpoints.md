# API Specification: REST Endpoints

All API endpoints reside under `/api/`. JWT authentication is mandatory for all task-related endpoints.

## Authentication
Better Auth handles the issuance of JWTs. The backend validates the `Authorization: Bearer <token>` header.

## Endpoints

### Tasks
- **GET /api/tasks**: Fetch all tasks for the authenticated user.
- **POST /api/tasks**: Create a new task.
- **GET /api/tasks/{id}**: Fetch a single task by ID (must belong to user).
- **PUT /api/tasks/{id}**: Update task title/description.
- **DELETE /api/tasks/{id}**: Delete a task.
- **PATCH /api/tasks/{id}/complete**: Toggle completion status.

### Chat Endpoint
- **POST /api/chat**: Process chat messages and return AI responses with optional tool calls.

## Schemas

### TaskBase (input)
- `title`: String (required)
- `description`: String (optional)

### Task (output)
- `id`: Integer
- `title`: String
- `description`: String
- `completed`: Boolean
- `user_id`: String (owner)

## Chat Endpoint Specification

### POST /api/chat

**Description**: Stateless chat endpoint that processes user messages through the OpenAI Agents SDK and returns AI responses. Supports conversation continuity through conversation IDs and maintains user isolation via JWT authentication.

**Authentication**: JWT required via `Authorization: Bearer <token>` header.

**Stateless Flow**:
1. Extract user_id from JWT token
2. Load conversation history if conversation_id provided
3. Process message through OpenAI Agents SDK with MCP tools
4. Save new messages to database
5. Return response with conversation context

#### Request Body Schema
```json
{
  "conversation_id": "string (optional) - UUID of existing conversation, creates new if omitted",
  "message": "string (required) - User's chat message, max 2000 characters"
}
```

#### Response Schema
```json
{
  "conversation_id": "string - UUID of the conversation (new or existing)",
  "response": "string - AI assistant's response message",
  "tool_calls": [
    {
      "tool": "string - Name of MCP tool called",
      "parameters": "object - Parameters passed to tool",
      "result": "object - Tool execution result"
    }
  ],
  "created_at": "string - ISO timestamp of response"
}
```

#### Example Request
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "Add a task to buy groceries tomorrow"
}
```

#### Example Response
```json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "response": "I've created a new task for you: 'Buy groceries tomorrow'. Is there anything else you'd like me to help you with?",
  "tool_calls": [
    {
      "tool": "add_task",
      "parameters": {
        "user_id": "user_123",
        "title": "Buy groceries tomorrow",
        "description": null
      },
      "result": {
        "id": 42,
        "title": "Buy groceries tomorrow",
        "completed": false,
        "user_id": "user_123",
        "created_at": "2024-01-15T10:30:00Z"
      }
    }
  ],
  "created_at": "2024-01-15T10:30:01Z"
}
```

#### Error Responses
- `400 Bad Request`: Invalid request body or missing required fields
- `401 Unauthorized`: Missing or invalid JWT token
- `404 Not Found`: Conversation ID doesn't exist or doesn't belong to user
- `413 Payload Too Large`: Message exceeds maximum length
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: AI service or database error

## Error Handling
- `401 Unauthorized`: Missing or invalid JWT.
- `403 Forbidden`: Accessing a task not owned by the user.
- `404 Not Found`: Resource does not exist.
- `422 Unprocessable Entity`: Validation error.
