"""
Chat Service for OpenRouter Integration
Handles conversation management and AI agent interactions.
"""
import os
import json
import logging
import traceback
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from sqlmodel import Session, select
from openai import OpenAI
from app.models.chat import Conversation, Message, MessageRole, ConversationCreate, MessageCreate
from app.services.mcp_tools import MCPTaskTools
from app.core.config import settings
import uuid

logger = logging.getLogger(__name__)

class ChatService:
    """Service for managing chat conversations and AI interactions."""
    
    def __init__(self, db: Session, user_id: str):
        self.db = db
        self.user_id = user_id
        
        # Get OpenRouter API key from environment
        api_key = settings.OPENROUTER_API_KEY
        if not api_key:
            logger.error("OPENROUTER_API_KEY environment variable not set")
            raise ValueError("OpenRouter API key not configured")
        
        # Initialize OpenAI-compatible client for OpenRouter
        try:
            self.openai_client = OpenAI(
                api_key=api_key,
                base_url=settings.OPENROUTER_BASE_URL
            )
            self.model = settings.OPENROUTER_MODEL
            logger.info(f"OpenRouter client initialized successfully with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize OpenRouter client: {e}")
            raise
            
        self.mcp_tools = MCPTaskTools(db, user_id)
    
    def get_or_create_conversation(self, conversation_id: Optional[str] = None) -> Conversation:
        """Get existing conversation or create a new one."""
        if conversation_id:
            # Try to find existing conversation
            conversation = self.db.exec(
                select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == self.user_id
                )
            ).first()
            
            if conversation:
                return conversation
            else:
                logger.warning(f"Conversation {conversation_id} not found for user {self.user_id}")
        
        # Create new conversation
        conversation = Conversation(
            id=str(uuid.uuid4()),
            user_id=self.user_id
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        
        logger.info(f"Created new conversation {conversation.id} for user {self.user_id}")
        return conversation
    
    def get_conversation_history(self, conversation_id: str, limit: int = 50) -> List[Message]:
        """Get conversation message history."""
        messages = self.db.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        ).all()
        
        return list(messages)
    
    def save_message(self, conversation_id: str, role: MessageRole, content: str, tool_calls: Optional[Dict[str, Any]] = None) -> Message:
        """Save a message to the conversation."""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_calls=tool_calls
        )
        
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        
        return message
    
    def execute_tool_call(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Execute an MCP tool call."""
        try:
            if tool_name == "add_task":
                return self.mcp_tools.add_task(
                    title=parameters.get("title"),
                    description=parameters.get("description")
                )
            elif tool_name == "list_tasks":
                return self.mcp_tools.list_tasks(
                    completed=parameters.get("completed"),
                    limit=parameters.get("limit", 50),
                    offset=parameters.get("offset", 0)
                )
            elif tool_name == "complete_task":
                return self.mcp_tools.complete_task(
                    task_id=parameters.get("task_id"),
                    completed=parameters.get("completed", True)
                )
            elif tool_name == "update_task":
                return self.mcp_tools.update_task(
                    task_id=parameters.get("task_id"),
                    title=parameters.get("title"),
                    description=parameters.get("description")
                )
            elif tool_name == "delete_task":
                return self.mcp_tools.delete_task(
                    task_id=parameters.get("task_id")
                )
            else:
                return {
                    "success": False,
                    "error": {
                        "code": "UNKNOWN_TOOL",
                        "message": f"Unknown tool: {tool_name}"
                    }
                }
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": "TOOL_EXECUTION_ERROR",
                    "message": f"Failed to execute {tool_name}"
                }
            }
    
    def format_openai_messages(self, messages: List[Message]) -> List[Dict[str, Any]]:
        """Format messages for OpenAI API."""
        openai_messages = [
            {
                "role": "system",
                "content": """You are a helpful task management assistant. You can help users create, list, update, complete, and delete their tasks through natural conversation.

Available tools:
- add_task(title, description=None): Create a new task
- list_tasks(completed=None, limit=50, offset=0): List tasks (completed=True/False/None for all)
- complete_task(task_id, completed=True): Mark task as complete/incomplete
- update_task(task_id, title=None, description=None): Update task details
- delete_task(task_id): Delete a task

Guidelines:
- Always confirm actions taken on behalf of the user
- Be conversational and helpful
- Ask for clarification when requests are ambiguous
- Provide clear feedback about task operations
- When listing tasks, format them nicely for the user
- For task completion, ask for confirmation before deleting tasks
- Be encouraging and supportive about productivity"""
            }
        ]
        
        for msg in messages:
            openai_messages.append({
                "role": msg.role.value,
                "content": msg.content
            })
        
        return openai_messages
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get OpenAI function definitions for available tools."""
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Create a new task for the user",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "The task title (required, max 200 chars)"
                            },
                            "description": {
                                "type": "string",
                                "description": "Optional task description (max 1000 chars)"
                            }
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "List user's tasks with optional filtering",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "completed": {
                                "type": "boolean",
                                "description": "Filter by completion status (true=completed, false=active, null=all)"
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of tasks to return (default 50, max 100)"
                            },
                            "offset": {
                                "type": "integer",
                                "description": "Number of tasks to skip for pagination (default 0)"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as completed or incomplete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "The ID of the task to update"
                            },
                            "completed": {
                                "type": "boolean",
                                "description": "Whether the task should be marked as completed (default true)"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update task title and/or description",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "The ID of the task to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "New task title (max 200 chars)"
                            },
                            "description": {
                                "type": "string",
                                "description": "New task description (max 1000 chars)"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Permanently delete a task",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "The ID of the task to delete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]
    
    def process_message(self, message: str, conversation_id: Optional[str] = None) -> Dict[str, Any]:
        """Process a user message and return AI response."""
        logger.info(f"=== CHAT MESSAGE PROCESSING STARTED for user: {self.user_id} ===")
        logger.info(f"Message: {message}")
        logger.info(f"Conversation ID: {conversation_id}")
        
        try:
            # Get or create conversation
            logger.info("Step 1: Getting or creating conversation...")
            conversation = self.get_or_create_conversation(conversation_id)
            logger.info(f"Conversation ID: {conversation.id}")
            
            # Save user message
            logger.info("Step 2: Saving user message...")
            user_message = self.save_message(
                conversation_id=conversation.id,
                role=MessageRole.USER,
                content=message
            )
            logger.info(f"User message saved with ID: {user_message.id}")
            
            # Get conversation history
            logger.info("Step 3: Getting conversation history...")
            history = self.get_conversation_history(conversation.id)
            logger.info(f"Found {len(history)} messages in history")
            
            # Format messages for OpenAI
            logger.info("Step 4: Formatting messages for OpenAI...")
            openai_messages = self.format_openai_messages(history)
            logger.info(f"Formatted {len(openai_messages)} messages")
            
            # Get available tools
            logger.info("Step 5: Getting available tools...")
            tools = self.get_available_tools()
            logger.info(f"Available tools: {len(tools)}")
            
            # Call OpenRouter API
            logger.info("Step 6: Calling OpenRouter API...")
            try:
                response = self.openai_client.chat.completions.create(
                    model=self.model,
                    messages=openai_messages,
                    tools=tools,
                    tool_choice="auto",
                    temperature=0.7,
                    max_tokens=1000
                )
                logger.info("OpenRouter API call successful")
            except Exception as openai_error:
                logger.error(f"OpenRouter API call failed: {str(openai_error)}")
                return {
                    "error": {
                        "code": "OPENROUTER_ERROR",
                        "message": f"OpenRouter API error: {str(openai_error)}"
                    }
                }
            
            assistant_message = response.choices[0].message
            tool_calls_executed = []
            
            # Handle tool calls
            if assistant_message.tool_calls:
                logger.info(f"Step 7: Processing {len(assistant_message.tool_calls)} tool calls...")
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    try:
                        parameters = json.loads(tool_call.function.arguments)
                    except json.JSONDecodeError:
                        parameters = {}
                    
                    logger.info(f"Executing tool: {tool_name} with params: {parameters}")
                    
                    # Execute tool
                    tool_result = self.execute_tool_call(tool_name, parameters)
                    logger.info(f"Tool result: {tool_result}")
                    
                    tool_calls_executed.append({
                        "tool": tool_name,
                        "parameters": parameters,
                        "result": tool_result
                    })
                    
                    # Add tool result to conversation for context
                    openai_messages.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [{
                            "id": tool_call.id,
                            "type": "function",
                            "function": {
                                "name": tool_name,
                                "arguments": tool_call.function.arguments
                            }
                        }]
                    })
                    
                    openai_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(tool_result)
                    })
                
                # Get final response after tool execution
                logger.info("Step 8: Getting final response after tool execution...")
                try:
                    final_response = self.openai_client.chat.completions.create(
                        model=self.model,
                        messages=openai_messages,
                        temperature=0.7,
                        max_tokens=1000
                    )
                    assistant_content = final_response.choices[0].message.content
                    logger.info("Final response received from OpenRouter")
                except Exception as final_error:
                    logger.error(f"Final OpenRouter call failed: {str(final_error)}")
                    assistant_content = "I executed the requested actions, but had trouble generating a response."
            else:
                assistant_content = assistant_message.content
                logger.info("No tool calls, using direct response")
            
            # Save assistant message
            logger.info("Step 9: Saving assistant message...")
            assistant_msg = self.save_message(
                conversation_id=conversation.id,
                role=MessageRole.ASSISTANT,
                content=assistant_content,
                tool_calls=tool_calls_executed if tool_calls_executed else None
            )
            logger.info(f"Assistant message saved with ID: {assistant_msg.id}")
            
            result = {
                "conversation_id": conversation.id,
                "response": assistant_content,
                "tool_calls": tool_calls_executed,
                "created_at": assistant_msg.created_at.isoformat()
            }
            
            logger.info(f"=== CHAT MESSAGE PROCESSING SUCCESS ===")
            return result
            
        except Exception as e:
            logger.error(f"=== CHAT MESSAGE PROCESSING FAILED: {str(e)} ===")
            logger.error(f"Traceback: {traceback.format_exc()}")
            return {
                "error": {
                    "code": "PROCESSING_ERROR",
                    "message": "Failed to process your message. Please try again."
                }
            }