# UI: Components

## Design System
- **Tailwind CSS**: Utility-first styling.
- **Lucide React**: Iconography.
- **OpenAI ChatKit**: Chat interface components (Phase III).

## Component List
- **Navbar**: Auth status, Navigation links.
- **TaskItem**: Display task, Edit/Delete/Toggle controls.
- **TaskForm**: Reusable form for Create and Edit.
- **EmptyState**: View when no tasks exist.
- **AuthLayout**: Centered layout for Login/Signup.
- **ChatInterface**: AI-powered chat for task management (Phase III).

## Chat Interface Component (Phase III)

### Overview
The ChatInterface component integrates OpenAI ChatKit with the todo application, providing a natural language interface for task management. It maintains conversation history and provides real-time interaction with the AI assistant.

### OpenAI ChatKit Integration

#### Core Components
- **ChatContainer**: Main wrapper component with full-height layout
- **MessageList**: Scrollable container for conversation history
- **MessageBubble**: Individual message display (user vs assistant styling)
- **InputArea**: Message composition with send button and loading states
- **TypingIndicator**: Shows when AI is processing responses

#### Component Structure
```jsx
<ChatInterface>
  <ChatHeader />
  <MessageList>
    {messages.map(message => (
      <MessageBubble 
        key={message.id}
        role={message.role}
        content={message.content}
        timestamp={message.created_at}
        toolCalls={message.tool_calls}
      />
    ))}
    <TypingIndicator visible={isLoading} />
  </MessageList>
  <InputArea 
    onSendMessage={handleSendMessage}
    disabled={isLoading}
    placeholder="Ask me to help with your tasks..."
  />
</ChatInterface>
```

### Layout Requirements

#### Message Bubbles
- **User Messages**: Right-aligned, blue background (`bg-blue-500`), white text
- **Assistant Messages**: Left-aligned, gray background (`bg-gray-100`), dark text
- **Timestamps**: Small, muted text below each message
- **Tool Call Indicators**: Subtle badges showing when actions were performed

#### Input Box
- **Positioning**: Fixed at bottom of chat container
- **Styling**: Rounded input with send button, consistent with app theme
- **States**: Normal, focused, disabled (during AI processing)
- **Accessibility**: Proper ARIA labels and keyboard navigation

#### Loading States
- **Typing Indicator**: Animated dots when AI is responding
- **Message Sending**: Temporary "sending" state for user messages
- **Error States**: Clear error messages with retry options

### Conversation Loading/Resume Behavior

#### Initial Load
1. Check for existing conversations via `/api/conversations` endpoint
2. Display conversation list or start new conversation
3. Load recent messages for selected conversation (last 50 messages)
4. Scroll to bottom of message history

#### Resume Conversation
1. Fetch conversation by ID with authentication
2. Load message history with pagination support
3. Restore scroll position to bottom
4. Maintain conversation context for new messages

#### New Conversation
1. Generate new conversation ID on first message
2. Store conversation metadata locally until first message sent
3. Create conversation record on backend with first message

### Integration with /api/chat Endpoint

#### Message Sending Flow
```javascript
const sendMessage = async (message) => {
  // Add user message to UI immediately
  addMessage({ role: 'user', content: message, timestamp: new Date() });
  
  // Show typing indicator
  setIsLoading(true);
  
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${jwt}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        conversation_id: currentConversationId,
        message: message
      })
    });
    
    const data = await response.json();
    
    // Add assistant response to UI
    addMessage({
      role: 'assistant',
      content: data.response,
      timestamp: data.created_at,
      tool_calls: data.tool_calls
    });
    
    // Update conversation ID if new conversation
    if (!currentConversationId) {
      setCurrentConversationId(data.conversation_id);
    }
    
  } catch (error) {
    // Handle error state
    showErrorMessage('Failed to send message. Please try again.');
  } finally {
    setIsLoading(false);
  }
};
```

#### JWT Authentication
- Include JWT token in all API requests
- Handle token expiration gracefully with refresh
- Redirect to login if authentication fails
- Show appropriate error messages for auth issues

### Responsive Design

#### Desktop Layout (≥768px)
- Full-height sidebar or dedicated chat page
- Wide message bubbles with comfortable padding
- Side-by-side layout with task list (optional)

#### Mobile Layout (<768px)
- Full-screen chat interface
- Compact message bubbles
- Sticky input area at bottom
- Swipe gestures for navigation (optional)

#### Tablet Layout (768px-1024px)
- Hybrid approach with collapsible sidebar
- Medium-width message bubbles
- Touch-friendly input controls

### Tailwind Theme Integration

#### Color Scheme
- **Primary**: Use existing app primary colors for user messages
- **Secondary**: Gray tones for assistant messages and UI elements
- **Accent**: Success green for completed tasks, warning colors for errors
- **Background**: Consistent with app background (`bg-gray-50` or `bg-white`)

#### Typography
- **Message Text**: `text-sm` or `text-base` for readability
- **Timestamps**: `text-xs text-gray-500`
- **Tool Indicators**: `text-xs` with appropriate color coding

#### Spacing
- **Message Padding**: `p-3` or `p-4` for comfortable reading
- **Message Margins**: `mb-2` or `mb-3` between messages
- **Container Padding**: `p-4` for overall chat container

### Accessibility Features

#### Keyboard Navigation
- Tab navigation through all interactive elements
- Enter key to send messages
- Escape key to clear input or close modals

#### Screen Reader Support
- Proper ARIA labels for all components
- Live regions for new messages and status updates
- Semantic HTML structure with proper headings

#### Visual Accessibility
- High contrast ratios for all text
- Focus indicators for keyboard users
- Scalable text that works with browser zoom
- Color-blind friendly design (don't rely solely on color)

### Performance Considerations

#### Message Virtualization
- Implement virtual scrolling for conversations with >100 messages
- Lazy load older messages on scroll up
- Efficient re-rendering with React.memo and proper keys

#### State Management
- Use React Context or state management library for chat state
- Debounce typing indicators and input validation
- Optimize re-renders with proper dependency arrays

#### Caching Strategy
- Cache recent conversations in localStorage
- Implement optimistic updates for better UX
- Background sync for offline message queue
