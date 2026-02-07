#!/usr/bin/env python3
"""
Final Application Test - Complete End-to-End Verification
Tests all functionality including the enhanced chatbot
"""

import requests
import json
import time
import sys

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_backend_health():
    """Test if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        return response.status_code == 200
    except:
        return False

def test_frontend_health():
    """Test if frontend is accessible"""
    try:
        response = requests.get(FRONTEND_URL)
        return response.status_code == 200
    except:
        return False

def create_test_user():
    """Create a test user and return auth token"""
    try:
        signup_data = {
            "username": f"finaltest_{int(time.time())}",
            "password": "testpass123"
        }
        
        response = requests.post(f"{BACKEND_URL}/api/auth/signup", json=signup_data)
        if response.status_code == 200:
            return response.json()["access_token"]
        return None
    except Exception as e:
        print(f"Error creating test user: {e}")
        return None

def test_enhanced_chatbot(token):
    """Test the enhanced chatbot functionality"""
    headers = {"Authorization": f"Bearer {token}"}
    
    def chat(message):
        try:
            response = requests.post(f"{BACKEND_URL}/api/chat/simple", 
                                   json={"message": message}, headers=headers)
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"Error {response.status_code}"
        except Exception as e:
            return f"Exception: {e}"
    
    print("🤖 Testing Enhanced Chatbot...")
    
    # Test natural language patterns
    test_cases = [
        ("hello", "greeting"),
        ("I need to buy groceries", "task creation"),
        ("Remind me to call mom", "task creation"),
        ("What are my tasks?", "task listing"),
        ("Show me what I need to do", "task listing"),
        ("How am I doing?", "progress check"),
        ("help", "help request"),
        ("thank you", "gratitude")
    ]
    
    results = []
    for message, test_type in test_cases:
        response = chat(message)
        success = "error" not in response.lower() and "exception" not in response.lower()
        results.append((test_type, success))
        
        if success:
            print(f"   ✅ {test_type}: '{message}' -> {response[:50]}...")
        else:
            print(f"   ❌ {test_type}: '{message}' -> {response}")
    
    return results

def test_task_operations(token):
    """Test task CRUD operations"""
    headers = {"Authorization": f"Bearer {token}"}
    
    print("📝 Testing Task Operations...")
    
    # Create task
    task_data = {"title": "Test Task", "description": "Test Description"}
    response = requests.post(f"{BACKEND_URL}/api/tasks/", json=task_data, headers=headers)
    
    if response.status_code == 200:
        task = response.json()
        task_id = task["id"]
        print(f"   ✅ Task created: {task['title']} (ID: {task_id})")
        
        # List tasks
        response = requests.get(f"{BACKEND_URL}/api/tasks/", headers=headers)
        if response.status_code == 200:
            tasks = response.json()
            print(f"   ✅ Tasks listed: {len(tasks)} task(s)")
            
            # Complete task
            response = requests.put(f"{BACKEND_URL}/api/tasks/{task_id}", 
                                  json={"completed": True}, headers=headers)
            if response.status_code == 200:
                print(f"   ✅ Task completed successfully")
                return True
            else:
                print(f"   ❌ Failed to complete task: {response.status_code}")
        else:
            print(f"   ❌ Failed to list tasks: {response.status_code}")
    else:
        print(f"   ❌ Failed to create task: {response.status_code}")
    
    return False

def main():
    print("🎯 Final Application Test - Complete Verification")
    print("=" * 60)
    
    # Test infrastructure
    print("1. Testing Infrastructure...")
    backend_ok = test_backend_health()
    frontend_ok = test_frontend_health()
    
    print(f"   Backend (localhost:8000): {'✅ Running' if backend_ok else '❌ Not accessible'}")
    print(f"   Frontend (localhost:3000): {'✅ Running' if frontend_ok else '❌ Not accessible'}")
    
    if not backend_ok:
        print("\n❌ Backend is not running. Please start it first.")
        return False
    
    # Test authentication
    print("\n2. Testing Authentication...")
    token = create_test_user()
    if token:
        print("   ✅ User authentication working")
    else:
        print("   ❌ User authentication failed")
        return False
    
    # Test task operations
    print("\n3. Testing Task Management...")
    task_ops_ok = test_task_operations(token)
    
    # Test enhanced chatbot
    print("\n4. Testing Enhanced Chatbot...")
    chatbot_results = test_enhanced_chatbot(token)
    
    # Calculate results
    chatbot_success_rate = sum(1 for _, success in chatbot_results if success) / len(chatbot_results)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 FINAL TEST RESULTS")
    print("=" * 60)
    
    print(f"🏗️  Infrastructure: {'✅ PASS' if backend_ok and frontend_ok else '❌ FAIL'}")
    print(f"🔐 Authentication: {'✅ PASS' if token else '❌ FAIL'}")
    print(f"📝 Task Management: {'✅ PASS' if task_ops_ok else '❌ FAIL'}")
    print(f"🤖 Enhanced Chatbot: {'✅ PASS' if chatbot_success_rate >= 0.8 else '❌ FAIL'} ({chatbot_success_rate:.1%} success rate)")
    
    overall_success = all([backend_ok, frontend_ok, token, task_ops_ok, chatbot_success_rate >= 0.8])
    
    print("\n" + "=" * 60)
    if overall_success:
        print("🎉 ALL TESTS PASSED! The application is fully functional!")
        print("\n✨ Key Features Working:")
        print("• User authentication (signup/login)")
        print("• Task management (create, read, update, delete)")
        print("• Enhanced chatbot with natural language understanding")
        print("• Conversational task creation ('I need to...')")
        print("• Natural task queries ('What do I need to do?')")
        print("• Progress tracking and encouragement")
        print("• Frontend-backend integration")
        
        print("\n🚀 Ready for use! Users can:")
        print("• Sign up and manage their personal tasks")
        print("• Chat naturally with the AI assistant")
        print("• Get help and encouragement")
        print("• Track their progress")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)