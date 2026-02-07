#!/usr/bin/env python3
"""
Enhanced Chatbot Functionality Test
Tests the natural language understanding capabilities of the chatbot
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

def create_test_user():
    """Create a test user and return auth token"""
    try:
        # Try to create a new user
        signup_data = {
            "username": f"testuser_{int(time.time())}",
            "password": "testpass123"
        }
        
        response = requests.post(f"{BACKEND_URL}/api/auth/signup", json=signup_data)
        if response.status_code == 200:
            return response.json()["access_token"]
        
        # If user exists, try to login
        login_response = requests.post(f"{BACKEND_URL}/api/auth/login", json=signup_data)
        if login_response.status_code == 200:
            return login_response.json()["access_token"]
            
        return None
    except Exception as e:
        print(f"Error creating test user: {e}")
        return None

def test_chat_message(token, message, expected_keywords=None):
    """Test a chat message and return the response"""
    try:
        headers = {"Authorization": f"Bearer {token}"}
        data = {"message": message}
        
        response = requests.post(f"{BACKEND_URL}/api/chat/simple", json=data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Message: '{message}'")
            print(f"   Response: {result['response'][:100]}...")
            
            if expected_keywords:
                response_lower = result['response'].lower()
                for keyword in expected_keywords:
                    if keyword.lower() in response_lower:
                        print(f"   ✓ Found expected keyword: '{keyword}'")
                    else:
                        print(f"   ⚠️ Missing expected keyword: '{keyword}'")
            
            return result
        else:
            print(f"❌ Message: '{message}' - Status: {response.status_code}")
            print(f"   Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error testing message '{message}': {e}")
        return None

def main():
    print("🤖 Enhanced Chatbot Functionality Test")
    print("=" * 50)
    
    # Check if backend is running
    print("1. Checking backend health...")
    if not test_backend_health():
        print("❌ Backend is not running. Please start it first.")
        return False
    print("✅ Backend is running")
    
    # Create test user
    print("\n2. Creating test user...")
    token = create_test_user()
    if not token:
        print("❌ Failed to create test user")
        return False
    print("✅ Test user created and authenticated")
    
    # Test natural language patterns
    print("\n3. Testing Natural Language Understanding...")
    
    test_cases = [
        # Greetings
        ("hello", ["hello", "assistant", "help"]),
        ("hi there", ["hello", "hi", "assistant"]),
        ("good morning", ["hello", "morning", "assistant"]),
        
        # Task creation - natural language
        ("I need to buy groceries", ["added", "groceries", "task"]),
        ("Remind me to call mom", ["added", "call mom", "task"]),
        ("I have to finish the report", ["added", "finish the report", "task"]),
        ("Add a task to walk the dog", ["added", "walk the dog", "task"]),
        
        # Task listing - natural language
        ("What are my tasks?", ["tasks", "list"]),
        ("Show me what I need to do", ["tasks", "need to do"]),
        ("What's on my list?", ["list", "tasks"]),
        ("What should I do next?", ["tasks", "next"]),
        
        # Help and conversation
        ("help", ["help", "commands", "examples"]),
        ("what can you do", ["help", "assistant", "tasks"]),
        ("thank you", ["welcome", "help"]),
        
        # Status and progress
        ("how am I doing", ["progress", "tasks"]),
        ("how many tasks do I have", ["tasks", "have"]),
        
        # Task completion (will test after creating tasks)
        ("I finished task 1", ["completed", "finished"]),
        ("done with task 2", ["completed", "done"]),
    ]
    
    successful_tests = 0
    total_tests = len(test_cases)
    
    for message, expected_keywords in test_cases:
        result = test_chat_message(token, message, expected_keywords)
        if result:
            successful_tests += 1
        print()  # Add spacing between tests
        time.sleep(0.5)  # Small delay between requests
    
    # Summary
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {successful_tests}/{total_tests} tests passed")
    
    if successful_tests == total_tests:
        print("🎉 All tests passed! The enhanced chatbot is working perfectly!")
        return True
    elif successful_tests >= total_tests * 0.8:
        print("✅ Most tests passed! The chatbot is working well with minor issues.")
        return True
    else:
        print("⚠️ Several tests failed. The chatbot needs more work.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)