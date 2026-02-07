"""
Chat API endpoints for AI-powered task management.
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlmodel import Session
from app.api.deps import get_db
from app.services.auth import get_current_user_id
from app.services.chat_service import ChatService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    conversation_id: Optional[str] = Field(None, description="UUID of existing conversation, creates new if omitted")
    message: str = Field(..., min_length=1, max_length=2000, description="User's chat message")

class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    conversation_id: str
    response: str
    tool_calls: Optional[list] = None
    created_at: str

@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Process chat messages and return AI responses.
    
    This endpoint:
    1. Validates the user's JWT token
    2. Gets or creates a conversation
    3. Processes the message through OpenAI with MCP tools
    4. Returns the AI response with any tool call results
    """
    try:
        # Create chat service
        chat_service = ChatService(db, current_user_id)
        
        # Process the message
        result = chat_service.process_message(
            message=request.message,
            conversation_id=request.conversation_id
        )
        
        # Check for errors
        if "error" in result:
            error = result["error"]
            if error["code"] == "PROCESSING_ERROR":
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=error["message"]
                )
            else:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error["message"]
                )
        
        return ChatResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in chat endpoint for user {current_user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while processing your message"
        )

@router.get("/conversations")
async def list_conversations(
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """List user's conversations."""
    try:
        from sqlmodel import select
        from app.models.chat import Conversation
        
        conversations = db.exec(
            select(Conversation)
            .where(Conversation.user_id == current_user_id)
            .order_by(Conversation.updated_at.desc())
            .limit(50)
        ).all()
        
        return {
            "conversations": [
                {
                    "id": conv.id,
                    "created_at": conv.created_at.isoformat(),
                    "updated_at": conv.updated_at.isoformat()
                }
                for conv in conversations
            ]
        }
        
    except Exception as e:
        logger.error(f"Error listing conversations for user {current_user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversations"
        )

@router.get("/conversations/{conversation_id}/messages")
async def get_conversation_messages(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """Get messages from a specific conversation."""
    try:
        from sqlmodel import select
        from app.models.chat import Conversation, Message
        
        # Verify conversation belongs to user
        conversation = db.exec(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == current_user_id
            )
        ).first()
        
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        
        # Get messages
        messages = db.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        ).all()
        
        return {
            "conversation_id": conversation_id,
            "messages": [
                {
                    "id": msg.id,
                    "role": msg.role.value,
                    "content": msg.content,
                    "tool_calls": msg.tool_calls,
                    "created_at": msg.created_at.isoformat()
                }
                for msg in messages
            ]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting messages for conversation {conversation_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversation messages"
        )