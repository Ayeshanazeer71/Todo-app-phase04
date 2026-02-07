#!/usr/bin/env python3
"""
Test the simple chat functionality
"""
import requests
import json
import time

BACKEND_URL = "http://localhost:8000/api"

def test_simple_chat():
    # Create a test user and get auth token
    test_user = {
        "username": f"simplechat_{int(time.time())}",
        "password": "testpass123"
    }

    print("1. Creating test user...")
    response = requests.post(f"{BACKEND_URL}/auth/signup", json=test_user)
    if response.status_code == 200:
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        print("✅ User created and authenticated")
        
        # Test simple chat commands
        commands = [
            "hello",
            "create task: Buy groceries",
            "create task: Walk the dog", 
            "list tasks",
            "complete task 2",
            "list tasks"
        ]
        
        for i, command in enumerate(commands, 1):
            print(f"\n{i}. Testing command: '{command}'")
            chat_data = {"message": command}
            response = requests.post(f"{BACKEND_URL}/chat/simple", json=chat_data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Response: {result['response']}")
                if result.get('tool_calls'):
                    print(f"   Tool calls: {len(result['tool_calls'])}")
            else:
                print(f"❌ Command failed: {response.status_code} - {response.text}")
        
        print("\n🎉 SIMPLE CHAT FUNCTIONALITY WORKING!")
        return True
    else:
        print(f"❌ User creation failed: {response.status_code} - {response.text}")
        return False

if __name__ == "__main__":
    success = test_simple_chat()
    if success:
        print("\n✅ Simple chat is working perfectly!")
    else:
        print("\n❌ Simple chat has issues.")