#!/usr/bin/env python3
"""
Test chat endpoint without OpenAI
"""
import requests
import json
import time

BACKEND_URL = "http://localhost:8000/api"

# Create a simple chat endpoint that doesn't use OpenAI
def test_simple_chat():
    # Create a test user and get auth token
    test_user = {
        "username": f"chattest_{int(time.time())}",
        "password": "testpass123"
    }

    print("1. Creating test user...")
    response = requests.post(f"{BACKEND_URL}/auth/signup", json=test_user)
    if response.status_code == 200:
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        print("✅ User created and authenticated")
        
        # Test the MCP tools directly via a simple endpoint
        print("2. Testing task creation via API...")
        task_data = {"title": "Chat Test Task", "description": "Created for chat testing"}
        response = requests.post(f"{BACKEND_URL}/tasks/", json=task_data, headers=headers)
        if response.status_code == 200:
            task = response.json()
            print(f"✅ Task created: {task['title']} (ID: {task['id']})")
            
            print("3. Testing task list via API...")
            response = requests.get(f"{BACKEND_URL}/tasks/", headers=headers)
            if response.status_code == 200:
                tasks = response.json()
                print(f"✅ Retrieved {len(tasks)} tasks")
                
                print("4. Testing conversation creation...")
                response = requests.get(f"{BACKEND_URL}/chat/conversations", headers=headers)
                if response.status_code == 200:
                    conversations = response.json()
                    print(f"✅ Conversations endpoint working: {conversations}")
                    
                    print("\n🎉 All chat-related APIs working except OpenAI integration!")
                    print("The issue is likely with the OpenAI API call or configuration.")
                    return True
                else:
                    print(f"❌ Conversations endpoint failed: {response.status_code}")
            else:
                print(f"❌ Task list failed: {response.status_code}")
        else:
            print(f"❌ Task creation failed: {response.status_code}")
    else:
        print(f"❌ User creation failed: {response.status_code}")
    
    return False

if __name__ == "__main__":
    success = test_simple_chat()
    if success:
        print("\n✅ Chat infrastructure is working! Issue is with OpenAI integration.")
    else:
        print("\n❌ Chat infrastructure has issues.")