#!/usr/bin/env python3
"""
Test the frontend chat functionality after the fix
"""
import requests
import json
import time

BACKEND_URL = "http://localhost:8000/api"

def test_frontend_chat():
    # Create a test user and get auth token
    test_user = {
        "username": f"frontendchat_{int(time.time())}",
        "password": "testpass123"
    }

    print("1. Creating test user...")
    response = requests.post(f"{BACKEND_URL}/auth/signup", json=test_user)
    if response.status_code == 200:
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        print("✅ User created and authenticated")
        
        # Test the simple chat endpoint that the frontend now uses
        print("2. Testing frontend chat endpoint...")
        chat_data = {"message": "create task: Frontend Test Task"}
        response = requests.post(f"{BACKEND_URL}/chat/simple", json=chat_data, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Chat response: {result['response']}")
            if result.get('tool_calls'):
                print(f"✅ Tool calls: {len(result['tool_calls'])}")
            
            print("3. Testing task list command...")
            chat_data2 = {"message": "list tasks"}
            response2 = requests.post(f"{BACKEND_URL}/chat/simple", json=chat_data2, headers=headers)
            if response2.status_code == 200:
                result2 = response2.json()
                print(f"✅ Task list response: {result2['response']}")
                print("\n🎉 FRONTEND CHAT FUNCTIONALITY WORKING!")
                return True
            else:
                print(f"❌ Task list failed: {response2.status_code}")
        else:
            print(f"❌ Chat failed: {response.status_code} - {response.text}")
    else:
        print(f"❌ User creation failed: {response.status_code}")
    
    return False

if __name__ == "__main__":
    success = test_frontend_chat()
    if success:
        print("\n✅ Frontend chat is now working!")
    else:
        print("\n❌ Frontend chat still has issues.")