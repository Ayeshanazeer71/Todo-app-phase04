#!/usr/bin/env python3
"""
Test chat service components individually
"""
import sys
sys.path.append('backend/src')

from app.services.chat_service import ChatService
from app.api.deps import get_db
from app.models.user import User
from sqlmodel import select

def test_chat_service():
    print("Testing ChatService components...")
    
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Get a user
        users = db.exec(select(User)).all()
        if not users:
            print("❌ No users found in database")
            return
        
        user = users[0]
        print(f"Using user: {user.username}")
        
        # Test ChatService initialization
        print("1. Testing ChatService initialization...")
        try:
            chat_service = ChatService(db, user.username)
            print("✅ ChatService initialized")
        except Exception as e:
            print(f"❌ ChatService initialization failed: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Test conversation creation
        print("2. Testing conversation creation...")
        try:
            conversation = chat_service.get_or_create_conversation()
            print(f"✅ Conversation created: {conversation.id}")
        except Exception as e:
            print(f"❌ Conversation creation failed: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Test message saving
        print("3. Testing message saving...")
        try:
            from app.models.chat import MessageRole
            message = chat_service.save_message(
                conversation_id=conversation.id,
                role=MessageRole.USER,
                content="Test message"
            )
            print(f"✅ Message saved: {message.id}")
        except Exception as e:
            print(f"❌ Message saving failed: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Test MCP tools
        print("4. Testing MCP tools...")
        try:
            result = chat_service.execute_tool_call("add_task", {"title": "Test Task"})
            print(f"✅ MCP tool call result: {result}")
        except Exception as e:
            print(f"❌ MCP tool call failed: {e}")
            import traceback
            traceback.print_exc()
            return
        
        print("\n🎉 All ChatService components working!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_chat_service()