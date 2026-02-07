"""
Test script for OpenRouter chat integration
"""
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_signup():
    """Test user signup"""
    print("\n=== Testing Signup ===")
    response = requests.post(
        f"{BASE_URL}/auth/signup",
        json={
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Token: {data.get('access_token', 'N/A')[:20]}...")
        return data.get('access_token')
    else:
        print(f"Error: {response.text}")
        return None

def test_login():
    """Test user login"""
    print("\n=== Testing Login ===")
    response = requests.post(
        f"{BASE_URL}/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword123"
        }
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Token: {data.get('access_token', 'N/A')[:20]}...")
        return data.get('access_token')
    else:
        print(f"Error: {response.text}")
        return None

def test_chat(token, message):
    """Test chat with OpenRouter"""
    print(f"\n=== Testing Chat: '{message}' ===")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        f"{BASE_URL}/chat/",
        headers=headers,
        json={
            "message": message
        }
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data.get('response', 'N/A')}")
        print(f"Conversation ID: {data.get('conversation_id', 'N/A')}")
        if data.get('tool_calls'):
            print(f"Tool Calls: {len(data['tool_calls'])}")
            for tool_call in data['tool_calls']:
                print(f"  - {tool_call['tool']}: {tool_call['result']}")
        return data
    else:
        print(f"Error: {response.text}")
        return None

def main():
    print("=" * 60)
    print("OpenRouter Chat Integration Test")
    print("=" * 60)
    
    # Try to login first, if fails then signup
    token = test_login()
    if not token:
        token = test_signup()
    
    if not token:
        print("\n❌ Failed to authenticate")
        return
    
    print("\n✅ Authentication successful")
    
    # Test 1: Simple greeting
    test_chat(token, "Hello! Can you help me manage my tasks?")
    
    # Test 2: Add a task
    test_chat(token, "I need to buy groceries tomorrow")
    
    # Test 3: List tasks
    test_chat(token, "What tasks do I have?")
    
    # Test 4: Complete a task
    test_chat(token, "Mark task 1 as complete")
    
    # Test 5: List tasks again
    test_chat(token, "Show me my tasks")
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)

if __name__ == "__main__":
    main()
