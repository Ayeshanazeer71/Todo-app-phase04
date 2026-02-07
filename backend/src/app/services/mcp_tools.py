"""
MCP Tools for Task Management
Provides standardized tools for the AI agent to interact with tasks.
"""
from typing import List, Optional, Dict, Any
from sqlmodel import Session, select
from app.api.deps import get_db
from app.models.task import Task, TaskCreate, TaskUpdate
from app.services.auth import get_current_user_id
import logging

logger = logging.getLogger(__name__)

class MCPTaskTools:
    """MCP Tools for task management operations."""
    
    def __init__(self, db: Session, user_id: str):
        self.db = db
        self.user_id = user_id
    
    def add_task(self, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Create a new task for the authenticated user."""
        try:
            if not title or len(title.strip()) == 0:
                return {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "Task title is required and cannot be empty"
                    }
                }
            
            if len(title) > 200:
                return {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "Task title cannot exceed 200 characters"
                    }
                }
            
            if description and len(description) > 1000:
                return {
                    "success": False,
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "Task description cannot exceed 1000 characters"
                    }
                }
            
            # Create task
            task_data = {
                "title": title.strip(),
                "description": description.strip() if description else None,
                "user_id": self.user_id,
                "completed": False,
                "position": 0  # Will be updated if needed
            }
            
            db_task = Task(**task_data)
            self.db.add(db_task)
            self.db.commit()
            self.db.refresh(db_task)
            
            logger.info(f"Created task {db_task.id} for user {self.user_id}")
            
            return {
                "success": True,
                "data": {
                    "id": db_task.id,
                    "title": db_task.title,
                    "description": db_task.description,
                    "completed": db_task.completed,
                    "user_id": db_task.user_id,
                    "created_at": db_task.created_at.isoformat() if db_task.created_at else None
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating task for user {self.user_id}: {str(e)}")
            self.db.rollback()
            return {
                "success": False,
                "error": {
                    "code": "SERVER_ERROR",
                    "message": "Failed to create task"
                }
            }
    
    def list_tasks(self, completed: Optional[bool] = None, limit: int = 50, offset: int = 0) -> Dict[str, Any]:
        """Retrieve all tasks for the authenticated user with optional filtering."""
        try:
            # Validate parameters
            if limit > 100:
                limit = 100
            if limit < 1:
                limit = 1
            if offset < 0:
                offset = 0
            
            # Build query
            query = select(Task).where(Task.user_id == self.user_id)
            
            if completed is not None:
                query = query.where(Task.completed == completed)
            
            # Order by position and creation date
            query = query.order_by(Task.position.asc(), Task.created_at.desc())
            
            # Apply pagination
            query = query.offset(offset).limit(limit)
            
            tasks = self.db.exec(query).all()
            
            # Get total count for pagination info
            count_query = select(Task).where(Task.user_id == self.user_id)
            if completed is not None:
                count_query = count_query.where(Task.completed == completed)
            
            total = len(self.db.exec(count_query).all())
            
            task_list = []
            for task in tasks:
                task_list.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "user_id": task.user_id,
                    "created_at": task.created_at.isoformat() if task.created_at else None,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                })
            
            logger.info(f"Listed {len(task_list)} tasks for user {self.user_id}")
            
            return {
                "success": True,
                "data": {
                    "tasks": task_list,
                    "total": total,
                    "limit": limit,
                    "offset": offset
                }
            }
            
        except Exception as e:
            logger.error(f"Error listing tasks for user {self.user_id}: {str(e)}")
            return {
                "success": False,
                "error": {
                    "code": "SERVER_ERROR",
                    "message": "Failed to retrieve tasks"
                }
            }
    
    def complete_task(self, task_id: int, completed: bool) -> Dict[str, Any]:
        """Mark a task as completed or incomplete."""
        try:
            # Find task
            task = self.db.get(Task, task_id)
            
            if not task:
                return {
                    "success": False,
                    "error": {
                        "code": "NOT_FOUND",
                        "message": f"Task with ID {task_id} not found"
                    }
                }
            
            if task.user_id != self.user_id:
                return {
                    "success": False,
                    "error": {
                        "code": "FORBIDDEN",
                        "message": "You don't have permission to modify this task"
                    }
                }
            
            # Update completion status
            task.completed = completed
            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)
            
            logger.info(f"Updated task {task_id} completion status to {completed} for user {self.user_id}")
            
            return {
                "success": True,
                "data": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "user_id": task.user_id,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                }
            }
            
        except Exception as e:
            logger.error(f"Error updating task {task_id} for user {self.user_id}: {str(e)}")
            self.db.rollback()
            return {
                "success": False,
                "error": {
                    "code": "SERVER_ERROR",
                    "message": "Failed to update task"
                }
            }
    
    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """Update task title and/or description."""
        try:
            # Find task
            task = self.db.get(Task, task_id)
            
            if not task:
                return {
                    "success": False,
                    "error": {
                        "code": "NOT_FOUND",
                        "message": f"Task with ID {task_id} not found"
                    }
                }
            
            if task.user_id != self.user_id:
                return {
                    "success": False,
                    "error": {
                        "code": "FORBIDDEN",
                        "message": "You don't have permission to modify this task"
                    }
                }
            
            # Validate inputs
            if title is not None:
                if not title or len(title.strip()) == 0:
                    return {
                        "success": False,
                        "error": {
                            "code": "VALIDATION_ERROR",
                            "message": "Task title cannot be empty"
                        }
                    }
                if len(title) > 200:
                    return {
                        "success": False,
                        "error": {
                            "code": "VALIDATION_ERROR",
                            "message": "Task title cannot exceed 200 characters"
                        }
                    }
                task.title = title.strip()
            
            if description is not None:
                if len(description) > 1000:
                    return {
                        "success": False,
                        "error": {
                            "code": "VALIDATION_ERROR",
                            "message": "Task description cannot exceed 1000 characters"
                        }
                    }
                task.description = description.strip() if description else None
            
            self.db.add(task)
            self.db.commit()
            self.db.refresh(task)
            
            logger.info(f"Updated task {task_id} for user {self.user_id}")
            
            return {
                "success": True,
                "data": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "user_id": task.user_id,
                    "updated_at": task.updated_at.isoformat() if task.updated_at else None
                }
            }
            
        except Exception as e:
            logger.error(f"Error updating task {task_id} for user {self.user_id}: {str(e)}")
            self.db.rollback()
            return {
                "success": False,
                "error": {
                    "code": "SERVER_ERROR",
                    "message": "Failed to update task"
                }
            }
    
    def delete_task(self, task_id: int) -> Dict[str, Any]:
        """Permanently delete a task."""
        try:
            # Find task
            task = self.db.get(Task, task_id)
            
            if not task:
                return {
                    "success": False,
                    "error": {
                        "code": "NOT_FOUND",
                        "message": f"Task with ID {task_id} not found"
                    }
                }
            
            if task.user_id != self.user_id:
                return {
                    "success": False,
                    "error": {
                        "code": "FORBIDDEN",
                        "message": "You don't have permission to delete this task"
                    }
                }
            
            # Delete task
            self.db.delete(task)
            self.db.commit()
            
            logger.info(f"Deleted task {task_id} for user {self.user_id}")
            
            return {
                "success": True,
                "data": {
                    "message": "Task deleted successfully",
                    "deleted_task_id": task_id
                }
            }
            
        except Exception as e:
            logger.error(f"Error deleting task {task_id} for user {self.user_id}: {str(e)}")
            self.db.rollback()
            return {
                "success": False,
                "error": {
                    "code": "SERVER_ERROR",
                    "message": "Failed to delete task"
                }
            }