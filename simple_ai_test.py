#!/usr/bin/env python3
import requests
import json
import time

# Create test user
signup_data = {'username': f'aitest_{int(time.time())}', 'password': 'testpass123'}
response = requests.post('http://localhost:8000/api/auth/signup', json=signup_data)

if response.status_code == 200:
    token = response.json()['access_token']
    print('✅ Test user created')
else:
    print('❌ Failed to create user')
    exit(1)

headers = {'Authorization': f'Bearer {token}'}

# Test AI chat
print("\n🤖 Testing AI Chat...")
response = requests.post('http://localhost:8000/api/chat/', 
                       json={'message': 'Hello! Can you help me create a task to buy groceries?'}, 
                       headers=headers)

print(f"Status: {response.status_code}")
if response.status_code == 200:
    result = response.json()
    print(f"✅ AI Response: {result['response']}")
    if result.get('tool_calls'):
        print(f"🔧 Tool calls: {len(result['tool_calls'])}")
        for tool in result['tool_calls']:
            print(f"   - {tool['tool']}: {tool['result']['success']}")
else:
    print(f"❌ Error: {response.text}")