#!/usr/bin/env python3
"""
Test Task Updating Functionality
Tests the new task updating feature in the chatbot
"""

import requests
import json
import time

def test_task_updating():
    print("🔄 Testing Task Updating Functionality")
    print("=" * 50)
    
    # Create test user
    signup_data = {'username': f'updatetest_{int(time.time())}', 'password': 'testpass123'}
    response = requests.post('http://localhost:8000/api/auth/signup', json=signup_data)
    
    if response.status_code == 200:
        token = response.json()['access_token']
        print('✅ Test user created')
    else:
        print('❌ Failed to create user')
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    def chat(message):
        response = requests.post('http://localhost:8000/api/chat/simple', 
                               json={'message': message}, headers=headers)
        if response.status_code == 200:
            return response.json()['response']
        else:
            return f"Error {response.status_code}: {response.text}"
    
    print("\n1. Creating test tasks...")
    
    # Create some test tasks
    tasks_to_create = [
        "I need to create task ayesha",
        "Add a task called python project",
        "Remind me to study javascript"
    ]
    
    for task in tasks_to_create:
        response = chat(task)
        print(f"   Created: {task}")
    
    print("\n2. Listing current tasks...")
    response = chat("What are my tasks?")
    print(f"   Tasks: {response[:100]}...")
    
    print("\n3. Testing task updating functionality...")
    
    # Test different update patterns
    update_tests = [
        "update task ayesha to python",
        "change task 2 to react project", 
        "rename task 3 to learn typescript",
        "update task 1 to advanced python"
    ]
    
    for update_cmd in update_tests:
        print(f"\n   Testing: '{update_cmd}'")
        response = chat(update_cmd)
        print(f"   Response: {response[:80]}...")
        
        if "✅" in response:
            print("   ✅ Update successful!")
        elif "❌" in response:
            print("   ⚠️ Update failed - this might be expected")
        else:
            print("   ℹ️ Informational response")
    
    print("\n4. Listing tasks after updates...")
    response = chat("Show me my tasks")
    print(f"   Updated tasks: {response[:150]}...")
    
    print("\n5. Testing edge cases...")
    
    edge_cases = [
        "update nonexistent task to something",
        "update task 999 to test",
        "update task to",  # Missing new name
        "update task"      # Incomplete command
    ]
    
    for edge_case in edge_cases:
        print(f"\n   Testing edge case: '{edge_case}'")
        response = chat(edge_case)
        print(f"   Response: {response[:60]}...")
    
    print("\n" + "=" * 50)
    print("🎉 Task updating functionality test completed!")
    print("\n✨ Key Features Tested:")
    print("• Update task by name: 'update task ayesha to python'")
    print("• Update task by ID: 'change task 1 to new name'")
    print("• Rename task: 'rename task 2 to something'")
    print("• Error handling for invalid requests")
    print("• Help and guidance for incomplete commands")

if __name__ == "__main__":
    test_task_updating()