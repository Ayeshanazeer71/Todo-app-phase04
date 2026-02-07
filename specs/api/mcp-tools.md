# MCP Tools Specification

## Introduction

The Model Context Protocol (MCP) server provides a standardized interface for the AI agent to interact with the task management system. These tools enable the chatbot to perform CRUD operations on tasks while maintaining strict user isolation and stateless operation principles.

All tools operate statelessly and enforce user ownership through the `user_id` parameter extracted from JWT tokens. The MCP server validates permissions and ensures users can only access their own data.

## Tool Specifications

| Tool Name | Purpose | Parameters | Returns | Example Input | Example Output |
|-----------|---------|------------|---------|---------------|----------------|
| **add_task** | Create a new task for the authenticated user | `user_id` (string, required): User identifier from JWT<br>`title` (string, required): Task title, max 200 chars<br>`description` (string, optional): Task description, max 1000 chars | Task object with id, title, description, completed status, user_id, timestamps | `{"user_id": "user_123", "title": "Buy groceries", "description": "Milk, eggs, bread"}` | `{"id": 1, "title": "Buy groceries", "description": "Milk, eggs, bread", "completed": false, "user_id": "user_123", "created_at": "2024-01-15T10:30:00Z"}` |
| **list_tasks** | Retrieve all tasks for the authenticated user with optional filtering | `user_id` (string, required): User identifier from JWT<br>`completed` (boolean, optional): Filter by completion status<br>`limit` (integer, optional): Max results, default 50<br>`offset` (integer, optional): Pagination offset, default 0 | Array of task objects matching filter criteria | `{"user_id": "user_123", "completed": false, "limit": 10}` | `{"tasks": [{"id": 1, "title": "Buy groceries", "completed": false, "user_id": "user_123"}, {"id": 2, "title": "Call dentist", "completed": false, "user_id": "user_123"}], "total": 2}` |
| **complete_task** | Mark a task as completed or incomplete | `user_id` (string, required): User identifier from JWT<br>`task_id` (integer, required): ID of task to update<br>`completed` (boolean, required): New completion status | Updated task object or error if not found/unauthorized | `{"user_id": "user_123", "task_id": 1, "completed": true}` | `{"id": 1, "title": "Buy groceries", "completed": true, "user_id": "user_123", "updated_at": "2024-01-15T11:00:00Z"}` |
| **update_task** | Update task title and/or description | `user_id` (string, required): User identifier from JWT<br>`task_id` (integer, required): ID of task to update<br>`title` (string, optional): New task title, max 200 chars<br>`description` (string, optional): New task description, max 1000 chars | Updated task object or error if not found/unauthorized | `{"user_id": "user_123", "task_id": 1, "title": "Buy organic groceries", "description": "Organic milk, free-range eggs, whole grain bread"}` | `{"id": 1, "title": "Buy organic groceries", "description": "Organic milk, free-range eggs, whole grain bread", "completed": false, "user_id": "user_123", "updated_at": "2024-01-15T11:15:00Z"}` |
| **delete_task** | Permanently delete a task | `user_id` (string, required): User identifier from JWT<br>`task_id` (integer, required): ID of task to delete | Success confirmation or error if not found/unauthorized | `{"user_id": "user_123", "task_id": 1}` | `{"success": true, "message": "Task deleted successfully", "deleted_task_id": 1}` |

## Implementation Requirements

### Stateless Operation
- Each tool call is independent and contains all necessary context
- No server-side session state is maintained between calls
- User identity is established fresh for each request via JWT validation

### User Ownership Enforcement
- All tools MUST validate that the `user_id` parameter matches the authenticated user from the JWT
- Tasks can only be accessed, modified, or deleted by their owner
- Attempting to access another user's tasks returns a permission error

### Error Handling
- **Authentication Errors**: Return 401 when JWT is invalid or missing
- **Authorization Errors**: Return 403 when user tries to access tasks they don't own
- **Not Found Errors**: Return 404 when task_id doesn't exist or doesn't belong to user
- **Validation Errors**: Return 422 for invalid parameters (empty title, invalid IDs, etc.)
- **Server Errors**: Return 500 for unexpected database or system errors

### Response Format
All tools return JSON responses with consistent structure:

#### Success Response
```json
{
  "success": true,
  "data": {
    // Tool-specific response data
  }
}
```

#### Error Response
```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {} // Optional additional context
  }
}
```

### Performance Considerations
- Database queries MUST include user_id in WHERE clauses for efficient filtering
- Implement appropriate indexes on user_id and task_id columns
- Use connection pooling for database connections
- Set reasonable limits on list_tasks results (default 50, max 100)

### Security Requirements
- Validate all input parameters against expected types and ranges
- Sanitize string inputs to prevent injection attacks
- Log all tool calls for audit purposes (excluding sensitive data)
- Rate limiting should be implemented at the API gateway level

## Integration with OpenAI Agents SDK

The MCP tools are registered with the OpenAI Agents SDK runner, which handles:
- Tool discovery and schema validation
- Parameter marshalling and validation
- Error handling and response formatting
- Integration with the conversation flow

The agent uses these tools to fulfill user requests while maintaining natural conversation flow and providing appropriate confirmations and error messages.