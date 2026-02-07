from typing import Optional, List, Dict, Any
from sqlmodel import Field, SQLModel, JSON, Column, Relationship
from datetime import datetime
from enum import Enum
import uuid

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class ConversationBase(SQLModel):
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Conversation(ConversationBase, table=True):
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True
    )
    
    # Relationship to messages (will be populated when queried with relationships)
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        cascade_delete=True
    )

class ConversationCreate(ConversationBase):
    pass

class ConversationRead(ConversationBase):
    id: str
    messages: List["MessageRead"] = []

class MessageBase(SQLModel):
    conversation_id: str = Field(foreign_key="conversation.id", index=True)
    role: MessageRole
    content: str
    tool_calls: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Message(MessageBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationship to conversation
    conversation: Optional[Conversation] = Relationship(back_populates="messages")

class MessageCreate(MessageBase):
    pass

class MessageRead(MessageBase):
    id: int

# Update forward references for proper type resolution
ConversationRead.model_rebuild()