#!/usr/bin/env python3
"""
Debug task creation issue
"""
import sys
sys.path.append('backend/src')

from app.models.task import Task, TaskCreate
from app.models.user import User
from app.api.deps import get_db
from sqlmodel import Session, select

def test_task_creation():
    print("Testing task creation directly...")
    
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Check if we have any users
        users = db.exec(select(User)).all()
        print(f"Found {len(users)} users in database")
        
        if users:
            user = users[0]
            print(f"Using user: {user.username} (ID: {user.id})")
            
            # Try to create a task
            task_data = TaskCreate(
                title="Debug Test Task",
                description="Testing task creation"
            )
            
            print("Creating task object...")
            task = Task(
                title=task_data.title,
                description=task_data.description,
                completed=task_data.completed,
                deadline=task_data.deadline,
                priority=task_data.priority,
                category=task_data.category,
                subtasks=task_data.subtasks,
                position=task_data.position,
                user_id=str(user.id)  # Convert to string as expected
            )
            
            print("Adding to database...")
            db.add(task)
            db.commit()
            db.refresh(task)
            
            print(f"✅ Task created successfully: ID={task.id}, Title={task.title}")
            
        else:
            print("❌ No users found in database")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_task_creation()