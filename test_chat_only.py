#!/usr/bin/env python3
"""
Test just the chat functionality after the fix
"""
import requests
import json
import time

BACKEND_URL = "http://localhost:8000/api"

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
    
    print("2. Testing chat functionality...")
    chat_data = {"message": "Hello! Can you help me create a task called 'Test Task'?"}
    response = requests.post(f"{BACKEND_URL}/chat/", json=chat_data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        chat_response = response.json()
        print(f"✅ Chat response received: {chat_response.get('response', 'No response')}")
        
        if chat_response.get('tool_calls'):
            print(f"✅ Tool calls executed: {len(chat_response['tool_calls'])}")
            for tool_call in chat_response['tool_calls']:
                print(f"  - {tool_call['tool']}: {tool_call['result']}")
        
        print("3. Testing task list via chat...")
        chat_data2 = {"message": "Can you show me my tasks?"}
        response2 = requests.post(f"{BACKEND_URL}/chat/", json=chat_data2, headers=headers)
        if response2.status_code == 200:
            chat_response2 = response2.json()
            print(f"✅ Task list chat response: {chat_response2.get('response', 'No response')}")
            print("\n🎉 CHAT FUNCTIONALITY WORKING!")
        else:
            print(f"❌ Task list chat failed: {response2.status_code} - {response2.text}")
    else:
        print(f"❌ Chat failed: {response.status_code} - {response.text}")
else:
    print(f"❌ User creation failed: {response.status_code} - {response.text}")