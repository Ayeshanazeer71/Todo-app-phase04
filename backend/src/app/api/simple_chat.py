"""
Simple Chat API endpoint for testing without OpenAI
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlmodel import Session
from app.api.deps import get_db
from app.services.auth import get_current_user_id
from app.services.mcp_tools import MCPTaskTools
import logging
import json
import re

logger = logging.getLogger(__name__)

router = APIRouter()

class SimpleChatRequest(BaseModel):
    """Request model for simple chat endpoint."""
    message: str = Field(..., min_length=1, max_length=2000, description="User's chat message")

class SimpleChatResponse(BaseModel):
    """Response model for simple chat endpoint."""
    response: str
    tool_calls: Optional[list] = None

@router.post("/simple", response_model=SimpleChatResponse)
def simple_chat(
    request: SimpleChatRequest,
    db: Session = Depends(get_db),
    current_user_id: str = Depends(get_current_user_id)
):
    """
    Simple chat endpoint that processes basic task commands without OpenAI.
    
    Supports commands like:
    - "create task: [title]"
    - "list tasks"
    - "complete task [id]"
    """
    try:
        message = request.message.lower().strip()
        mcp_tools = MCPTaskTools(db, current_user_id)
        
        # Enhanced command parsing with natural language understanding
        
        # Greeting responses - enhanced and more engaging
        if any(word in message for word in ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "howdy", "greetings", "what's up", "sup"]):
            return SimpleChatResponse(
                response="""👋 Hey there! I'm your AI task assistant, and I'm excited to help you stay organized!

I understand natural conversation, so just talk to me like you would a friend:

**Quick Examples:**
• "I need to buy groceries" → I'll create the task
• "What do I need to do today?" → I'll show your list  
• "I finished the shopping" → I'll mark it complete
• "How am I doing?" → I'll show your progress

No need for rigid commands - just tell me what's on your mind! What can I help you with today? 😊"""
            )
        
        # Natural language task listing - enhanced patterns (check BEFORE task creation)
        if any(phrase in message for phrase in ["what are my tasks", "show my tasks", "what do i need to do", "what's on my list", "my todo", "what tasks do i have", "what's next", "what should i do", "show me my list", "what's left to do", "what do i have to do", "show me what i need to do"]):
            result = mcp_tools.list_tasks()
            if result["success"]:
                tasks = result["data"]["tasks"]
                if not tasks:
                    response = "📝 Your task list is completely empty! You're either super organized or ready to add something new. What would you like to work on? 🌟"
                else:
                    completed_tasks = [t for t in tasks if t["completed"]]
                    incomplete_tasks = [t for t in tasks if not t["completed"]]
                    
                    if not incomplete_tasks:
                        response = f"🎉 Amazing! You've completed all {len(completed_tasks)} tasks! You're absolutely crushing it today! Ready to add something new to conquer? 💪"
                    else:
                        task_list = []
                        for task in incomplete_tasks:
                            task_list.append(f"⏳ {task['id']}: {task['title']}")
                        
                        if completed_tasks:
                            response = f"📝 Here's what's left on your plate:\n" + "\n".join(task_list) + f"\n\n🎯 You've already completed {len(completed_tasks)} task(s) - great progress!"
                        else:
                            response = f"📝 Here's what you need to tackle:\n" + "\n".join(task_list) + "\n\nYou've got this! Which one would you like to start with? 🚀"
                
                return SimpleChatResponse(
                    response=response,
                    tool_calls=[{"tool": "list_tasks", "result": result}]
                )
            else:
                return SimpleChatResponse(
                    response=f"❌ I couldn't get your tasks right now: {result['error']['message']}"
                )
        
        # Natural language task creation - enhanced patterns
        elif any(phrase in message for phrase in ["i need to", "i have to", "i should", "i want to", "i must", "remind me to", "add a task", "new task", "create a task", "make a task", "add to my list", "put on my list"]):
            # Extract the task from natural language
            task_title = ""
            
            patterns = [
                ("i need to", "i need to"),
                ("i have to", "i have to"),
                ("i should", "i should"),
                ("i want to", "i want to"),
                ("i must", "i must"),
                ("remind me to", "remind me to"),
                ("add a task to", "add a task to"),
                ("add a task", "add a task"),
                ("create a task to", "create a task to"),
                ("create a task", "create a task"),
                ("make a task to", "make a task to"),
                ("make a task", "make a task"),
                ("new task:", "new task:"),
                ("new task to", "new task to"),
                ("new task", "new task"),
                ("add to my list:", "add to my list:"),
                ("add to my list", "add to my list"),
                ("put on my list:", "put on my list:"),
                ("put on my list", "put on my list")
            ]
            
            for pattern, phrase in patterns:
                if pattern in message:
                    if ":" in message and pattern + ":" in message:
                        task_title = message.split(pattern + ":", 1)[1].strip()
                    elif " to " in message and pattern + " to" in message:
                        task_title = message.split(pattern + " to", 1)[1].strip()
                    else:
                        task_title = message.split(pattern, 1)[1].strip()
                    break
            
            # Clean up common prefixes/suffixes
            task_title = task_title.strip(".,!?")
            
            if task_title:
                result = mcp_tools.add_task(task_title)
                if result["success"]:
                    task_data = result["data"]
                    return SimpleChatResponse(
                        response=f"✅ Perfect! I've added '{task_data['title']}' to your task list (ID: {task_data['id']}). You're all set! 🎯",
                        tool_calls=[{"tool": "add_task", "result": result}]
                    )
                else:
                    return SimpleChatResponse(
                        response=f"❌ Sorry, I couldn't create that task: {result['error']['message']}"
                    )
            else:
                return SimpleChatResponse(
                    response="I'd love to help you add a task! What do you need to do? Try saying:\n• 'I need to buy groceries'\n• 'Remind me to call mom'\n• 'Add a task to finish the report'"
                )
        
        # Natural language task completion - enhanced patterns
        if any(phrase in message for phrase in ["i finished", "i completed", "i did", "i'm done with", "finished task", "completed task", "did task", "done with", "just finished", "just completed"]):
            try:
                numbers = re.findall(r'\d+', message)
                if numbers:
                    task_id = int(numbers[0])
                    result = mcp_tools.complete_task(task_id, True)
                    if result["success"]:
                        task_data = result["data"]
                        return SimpleChatResponse(
                            response=f"🎉 Awesome! You completed '{task_data['title']}'. Great job! Keep up the momentum! 💪",
                            tool_calls=[{"tool": "complete_task", "result": result}]
                        )
                    else:
                        return SimpleChatResponse(
                            response=f"❌ I couldn't mark that task as complete: {result['error']['message']}"
                        )
                else:
                    # Try to find task by partial title match
                    task_text = message.lower()
                    for phrase in ["i finished", "i completed", "i did", "i'm done with", "finished", "completed", "did", "done with", "just finished", "just completed"]:
                        if phrase in task_text:
                            task_text = task_text.replace(phrase, "").strip()
                            break
                    
                    if task_text:
                        # Get all tasks and try to find a match
                        result = mcp_tools.list_tasks()
                        if result["success"]:
                            tasks = result["data"]["tasks"]
                            incomplete_tasks = [t for t in tasks if not t["completed"]]
                            
                            # Look for partial matches in task titles
                            matches = []
                            for task in incomplete_tasks:
                                if task_text in task["title"].lower():
                                    matches.append(task)
                            
                            if len(matches) == 1:
                                # Found exactly one match
                                task = matches[0]
                                result = mcp_tools.complete_task(task["id"], True)
                                if result["success"]:
                                    return SimpleChatResponse(
                                        response=f"🎉 Perfect! I found and completed '{task['title']}' for you. Well done! 🌟",
                                        tool_calls=[{"tool": "complete_task", "result": result}]
                                    )
                            elif len(matches) > 1:
                                # Multiple matches - ask for clarification
                                match_list = "\n".join([f"• {t['id']}: {t['title']}" for t in matches])
                                return SimpleChatResponse(
                                    response=f"I found multiple tasks that might match. Which one did you complete?\n{match_list}\n\nYou can say 'I finished task [number]'"
                                )
                    
                    return SimpleChatResponse(
                        response="Which task did you finish? You can say:\n• 'I finished task 1'\n• 'Done with task 2'\n• Or describe the task: 'I finished the groceries'"
                    )
            except (IndexError, ValueError):
                return SimpleChatResponse(
                    response="Which task did you finish? You can say 'I finished task 1' or describe what you completed!"
                )
        
        # Natural language task updating - NEW FEATURE
        if any(phrase in message for phrase in ["update task", "change task", "rename task", "modify task", "edit task"]):
            try:
                # Parse different update patterns
                task_id = None
                new_title = None
                
                # Pattern 1: "update task [id] to [new_title]"
                if " to " in message:
                    parts = message.split(" to ", 1)
                    if len(parts) == 2:
                        left_part = parts[0].strip()
                        new_title = parts[1].strip()
                        
                        # Extract task ID from left part
                        numbers = re.findall(r'\d+', left_part)
                        if numbers:
                            task_id = int(numbers[0])
                        else:
                            # Try to find task by name in left part
                            for phrase in ["update task", "change task", "rename task", "modify task", "edit task"]:
                                if phrase in left_part:
                                    task_name = left_part.replace(phrase, "").strip()
                                    if task_name:
                                        # Find task by name
                                        result = mcp_tools.list_tasks()
                                        if result["success"]:
                                            tasks = result["data"]["tasks"]
                                            matches = [t for t in tasks if task_name.lower() in t["title"].lower()]
                                            if len(matches) == 1:
                                                task_id = matches[0]["id"]
                                            elif len(matches) > 1:
                                                match_list = "\n".join([f"• {t['id']}: {t['title']}" for t in matches])
                                                return SimpleChatResponse(
                                                    response=f"I found multiple tasks with that name. Which one do you want to update?\n{match_list}\n\nYou can say 'update task [number] to {new_title}'"
                                                )
                                    break
                
                # Pattern 2: "update [task_name] to [new_title]" 
                elif not task_id and " to " in message:
                    parts = message.split(" to ", 1)
                    if len(parts) == 2:
                        task_name_part = parts[0].strip()
                        new_title = parts[1].strip()
                        
                        # Remove "update" from the beginning
                        if task_name_part.startswith("update "):
                            task_name = task_name_part[7:].strip()
                            
                            # Find task by name
                            result = mcp_tools.list_tasks()
                            if result["success"]:
                                tasks = result["data"]["tasks"]
                                matches = [t for t in tasks if task_name.lower() == t["title"].lower()]
                                if len(matches) == 1:
                                    task_id = matches[0]["id"]
                                elif len(matches) == 0:
                                    # Try partial match
                                    matches = [t for t in tasks if task_name.lower() in t["title"].lower()]
                                    if len(matches) == 1:
                                        task_id = matches[0]["id"]
                                    elif len(matches) > 1:
                                        match_list = "\n".join([f"• {t['id']}: {t['title']}" for t in matches])
                                        return SimpleChatResponse(
                                            response=f"I found multiple tasks that might match '{task_name}'. Which one do you want to update?\n{match_list}\n\nYou can say 'update task [number] to {new_title}'"
                                        )
                                    else:
                                        return SimpleChatResponse(
                                            response=f"I couldn't find a task named '{task_name}'. You can say 'what are my tasks' to see all your tasks, then use 'update task [number] to {new_title}'"
                                        )
                
                if task_id and new_title:
                    result = mcp_tools.update_task(task_id, title=new_title)
                    if result["success"]:
                        task_data = result["data"]
                        return SimpleChatResponse(
                            response=f"✅ Perfect! I've updated the task to '{task_data['title']}' (ID: {task_data['id']}). All set! 🎯",
                            tool_calls=[{"tool": "update_task", "result": result}]
                        )
                    else:
                        return SimpleChatResponse(
                            response=f"❌ I couldn't update that task: {result['error']['message']}"
                        )
                else:
                    return SimpleChatResponse(
                        response="I'd be happy to help you update a task! You can say:\n• 'update task 1 to python'\n• 'change task ayesha to python'\n• 'rename task 2 to new name'\n\nWhat task would you like to update?"
                    )
                    
            except (IndexError, ValueError) as e:
                return SimpleChatResponse(
                    response="I'd be happy to help you update a task! You can say:\n• 'update task 1 to python'\n• 'change task ayesha to python'\n• 'rename task 2 to new name'"
                )
        
        # Natural language task listing - enhanced patterns
        if any(phrase in message for phrase in ["what are my tasks", "show my tasks", "what do i need to do", "what's on my list", "my todo", "what tasks do i have", "what's next", "what should i do", "show me my list", "what's left to do", "what do i have to do"]):
            result = mcp_tools.list_tasks()
            if result["success"]:
                tasks = result["data"]["tasks"]
                if not tasks:
                    response = "📝 Your task list is completely empty! You're either super organized or ready to add something new. What would you like to work on? 🌟"
                else:
                    completed_tasks = [t for t in tasks if t["completed"]]
                    incomplete_tasks = [t for t in tasks if not t["completed"]]
                    
                    if not incomplete_tasks:
                        response = f"🎉 Amazing! You've completed all {len(completed_tasks)} tasks! You're absolutely crushing it today! Ready to add something new to conquer? 💪"
                    else:
                        task_list = []
                        for task in incomplete_tasks:
                            task_list.append(f"⏳ {task['id']}: {task['title']}")
                        
                        if completed_tasks:
                            response = f"📝 Here's what's left on your plate:\n" + "\n".join(task_list) + f"\n\n🎯 You've already completed {len(completed_tasks)} task(s) - great progress!"
                        else:
                            response = f"📝 Here's what you need to tackle:\n" + "\n".join(task_list) + "\n\nYou've got this! Which one would you like to start with? 🚀"
                
                return SimpleChatResponse(
                    response=response,
                    tool_calls=[{"tool": "list_tasks", "result": result}]
                )
            else:
                return SimpleChatResponse(
                    response=f"❌ I couldn't get your tasks right now: {result['error']['message']}"
                )
        
        # Specific command parsing (keeping the original functionality)
        if message.startswith("create task:") or message.startswith("add task:") or message.startswith("create task ") or message.startswith("add task "):
            # Extract task title - handle both "create task:" and "create task " formats
            if ":" in message:
                title = message.split(":", 1)[1].strip()
            else:
                # Handle "create task title" format
                parts = message.split(" ", 2)
                if len(parts) >= 3:
                    title = parts[2].strip()
                else:
                    title = ""
            
            if not title:
                return SimpleChatResponse(
                    response="What task would you like me to add? You can say 'create task: Buy groceries' or just 'I need to buy groceries'"
                )
            
            result = mcp_tools.add_task(title)
            if result["success"]:
                task_data = result["data"]
                return SimpleChatResponse(
                    response=f"✅ Created task: '{task_data['title']}' (ID: {task_data['id']})",
                    tool_calls=[{"tool": "add_task", "result": result}]
                )
            else:
                return SimpleChatResponse(
                    response=f"❌ Failed to create task: {result['error']['message']}"
                )
        
        elif "list tasks" in message or "show tasks" in message:
            result = mcp_tools.list_tasks()
            if result["success"]:
                tasks = result["data"]["tasks"]
                if not tasks:
                    response = "📝 You have no tasks yet. Create one with 'create task: [title]'"
                else:
                    task_list = []
                    for task in tasks:
                        status = "✅" if task["completed"] else "⏳"
                        task_list.append(f"{status} {task['id']}: {task['title']}")
                    response = f"📝 Your tasks:\n" + "\n".join(task_list)
                
                return SimpleChatResponse(
                    response=response,
                    tool_calls=[{"tool": "list_tasks", "result": result}]
                )
            else:
                return SimpleChatResponse(
                    response=f"❌ Failed to list tasks: {result['error']['message']}"
                )
        
        elif "complete task" in message or "finish task" in message or "done task" in message or message.startswith("done "):
            # Extract task ID - handle various formats
            try:
                # Try to find a number in the message
                numbers = re.findall(r'\d+', message)
                if numbers:
                    task_id = int(numbers[0])
                else:
                    return SimpleChatResponse(
                        response="Please specify a task ID. Examples:\n• 'complete task 1'\n• 'finish task 2'\n• 'done 3'"
                    )
                
                result = mcp_tools.complete_task(task_id, True)
                if result["success"]:
                    task_data = result["data"]
                    return SimpleChatResponse(
                        response=f"✅ Completed task: '{task_data['title']}'",
                        tool_calls=[{"tool": "complete_task", "result": result}]
                    )
                else:
                    return SimpleChatResponse(
                        response=f"❌ Failed to complete task: {result['error']['message']}"
                    )
            except (IndexError, ValueError):
                return SimpleChatResponse(
                    response="Please specify a task ID. Examples:\n• 'complete task 1'\n• 'finish task 2'\n• 'done 3'"
                )
        
        # Help and general conversation
        elif any(word in message for word in ["help", "what can you do", "commands", "how do i"]):
            return SimpleChatResponse(
                response="""🤖 I'm your AI task assistant! I understand natural conversation. Here's what I can help with:

**Creating Tasks:**
• "I need to buy groceries"
• "Remind me to call mom"
• "Add a task to finish the report"

**Viewing Tasks:**
• "What are my tasks?"
• "Show me what I need to do"
• "What's on my list?"

**Updating Tasks:**
• "Update task ayesha to python"
• "Change task 1 to new name"
• "Rename task 2 to something else"

**Completing Tasks:**
• "I finished task 1"
• "I completed the groceries"
• "Done with task 2"

**Or use direct commands:**
• "create task: [title]"
• "list tasks"
• "update task [id] to [new title]"
• "complete task [id]"

Just talk to me naturally - I'll understand! 😊"""
            )
        
        # Thank you responses
        elif any(word in message for word in ["thank", "thanks", "appreciate"]):
            return SimpleChatResponse(
                response="You're very welcome! I'm here whenever you need help managing your tasks. Is there anything else I can do for you? 😊"
            )
        
        # Goodbye responses
        elif any(word in message for word in ["bye", "goodbye", "see you", "later", "exit"]):
            return SimpleChatResponse(
                response="Goodbye! Have a productive day, and remember - I'm here whenever you need help with your tasks! 👋"
            )
        
        # Motivational responses for task completion
        elif any(phrase in message for phrase in ["all done", "finished everything", "completed all"]):
            result = mcp_tools.list_tasks()
            if result["success"]:
                tasks = result["data"]["tasks"]
                incomplete_tasks = [t for t in tasks if not t["completed"]]
                if not incomplete_tasks:
                    return SimpleChatResponse(
                        response="🎉 Congratulations! You've completed all your tasks! You're absolutely crushing it today! Want to add something new to your list?"
                    )
                else:
                    return SimpleChatResponse(
                        response=f"Great progress! You still have {len(incomplete_tasks)} task(s) to go. You're doing amazing - keep it up! 💪"
                    )
        
        # Status check
        elif any(phrase in message for phrase in ["how am i doing", "my progress", "how many tasks"]):
            result = mcp_tools.list_tasks()
            if result["success"]:
                tasks = result["data"]["tasks"]
                if not tasks:
                    return SimpleChatResponse(
                        response="You don't have any tasks yet! Ready to add something to your list? 📝"
                    )
                
                completed = len([t for t in tasks if t["completed"]])
                total = len(tasks)
                incomplete = total - completed
                
                if completed == total:
                    return SimpleChatResponse(
                        response=f"🎉 Perfect! You've completed all {total} tasks! You're absolutely on fire today!"
                    )
                elif completed > 0:
                    return SimpleChatResponse(
                        response=f"📊 You're making great progress! {completed}/{total} tasks completed. {incomplete} to go - you've got this! 💪"
                    )
                else:
                    return SimpleChatResponse(
                        response=f"📝 You have {total} tasks waiting for you. Ready to tackle them? Let's get started! 🚀"
                    )
        
        else:
            # Enhanced default response with natural language examples
            return SimpleChatResponse(
                response="""🤖 I'm your AI task assistant! I understand natural conversation.

Try saying things like:
• "I need to buy groceries" (I'll create a task)
• "What do I need to do today?" (I'll show your tasks)
• "Update task ayesha to python" (I'll rename the task)
• "I finished task 1" (I'll mark it complete)
• "How am I doing?" (I'll show your progress)

Or just say "help" for more examples! 😊"""
            )
            
    except Exception as e:
        logger.error(f"Error in simple chat for user {current_user_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process your message"
        )