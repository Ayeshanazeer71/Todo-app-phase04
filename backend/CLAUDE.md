# Backend Development Guidelines

## FastAPI + SQLModel Architecture

- **Framework**: FastAPI with async/await patterns
- **ORM**: SQLModel for type-safe database operations
- **Database**: Neon PostgreSQL with connection pooling
- **Authentication**: JWT-based user authentication

## AI Chatbot Backend Guidelines

### MCP Server Tools

- **Protocol**: Implement Official MCP SDK for tool definitions
- **Tool Registration**: Register task CRUD operations as MCP tools
- **Schema Validation**: Use Pydantic models for tool input/output
- **Error Handling**: Provide clear error messages for tool failures
- **Security**: Validate user permissions for each tool operation

### OpenAI Agents SDK Runner

- **Agent Configuration**: Set up OpenAI agent with task management capabilities
- **Tool Integration**: Connect MCP tools to agent runtime
- **Context Management**: Maintain conversation context across requests
- **Response Streaming**: Support streaming responses for real-time chat
- **Rate Limiting**: Implement appropriate rate limits for API calls

### Stateless /api/chat Endpoint

- **Design Principle**: Each request is independent and stateless
- **JWT Authentication**: Extract user context from JWT tokens
- **Request Processing**: Handle chat messages without server-side session state
- **Response Format**: Return structured responses compatible with ChatKit
- **Error Responses**: Consistent error format across all endpoints

### DB Persistence for Conversations/Messages

- **Schema Design**: Separate tables for conversations and messages
- **User Isolation**: Ensure users can only access their own data
- **Message Storage**: Store both user messages and AI responses
- **Metadata Tracking**: Include timestamps, message types, and tool usage
- **Performance**: Index conversations by user_id and created_at
- **Data Retention**: Implement policies for conversation cleanup

### Security Considerations

- **Input Validation**: Sanitize all user inputs before processing
- **SQL Injection**: Use parameterized queries through SQLModel
- **Authorization**: Verify user permissions for each operation
- **Audit Logging**: Log all chat interactions for debugging and compliance