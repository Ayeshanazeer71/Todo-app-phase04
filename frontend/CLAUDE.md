# Frontend Development Guidelines

## Next.js 16+ Application Structure

- **Framework**: Next.js 16+ with App Router
- **Authentication**: Better Auth integration
- **Styling**: Tailwind CSS
- **TypeScript**: Strict mode enabled

## Chat Interface Guidelines

### OpenAI ChatKit Integration

- **Component Library**: Use OpenAI ChatKit React components for consistent chat UI
- **Message Rendering**: Support markdown, code blocks, and interactive elements
- **Real-time Updates**: Implement streaming responses for better UX
- **Accessibility**: Ensure chat interface meets WCAG 2.1 AA standards

### Secure API Calls with JWT

- **Authentication**: Include JWT tokens in all chat API requests
- **Token Refresh**: Handle token expiration gracefully
- **Error Handling**: Provide clear feedback for authentication failures
- **User Context**: Maintain user session state throughout chat interactions

### Conversation Loading/Resume

- **Persistence**: Load previous conversations from backend API
- **State Management**: Use React state or context for active conversation
- **History Navigation**: Allow users to browse and resume past conversations
- **Performance**: Implement pagination for large conversation histories
- **Offline Support**: Cache recent conversations for offline viewing

### UI/UX Best Practices

- **Responsive Design**: Ensure chat works on mobile and desktop
- **Loading States**: Show appropriate spinners and skeleton screens
- **Message Status**: Display sent/delivered/error states for messages
- **Typing Indicators**: Show when AI is processing responses