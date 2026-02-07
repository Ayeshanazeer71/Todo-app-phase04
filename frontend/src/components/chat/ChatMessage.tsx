/**
 * Chat message component for displaying user and assistant messages
 */
import { ChatMessage as ChatMessageType } from '@/lib/chat-api';

interface ChatMessageProps {
  message: ChatMessageType;
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const isUser = message.role === 'user';
  
  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'} mb-4`}>
      <div className={`max-w-[80%] rounded-2xl px-4 py-3 ${
        isUser 
          ? 'bg-blue-600 text-white ml-12' 
          : 'bg-gray-100 text-gray-800 mr-12'
      }`}>
        <div className="text-sm leading-relaxed whitespace-pre-wrap">
          {message.content}
        </div>
        
        {/* Show tool calls if present (for assistant messages) */}
        {!isUser && message.tool_calls && message.tool_calls.length > 0 && (
          <div className="mt-3 pt-3 border-t border-gray-200">
            <div className="text-xs text-gray-500 mb-2">Actions performed:</div>
            {message.tool_calls.map((toolCall, index) => (
              <div key={index} className="text-xs bg-gray-50 rounded-lg p-2 mb-1">
                <span className="font-medium text-blue-600">{toolCall.tool}</span>
                {toolCall.result?.success && (
                  <span className="ml-2 text-green-600">✓</span>
                )}
                {toolCall.result?.success === false && (
                  <span className="ml-2 text-red-600">✗</span>
                )}
              </div>
            ))}
          </div>
        )}
        
        <div className={`text-xs mt-2 ${
          isUser ? 'text-blue-200' : 'text-gray-400'
        }`}>
          {new Date(message.created_at).toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
          })}
        </div>
      </div>
    </div>
  );
}