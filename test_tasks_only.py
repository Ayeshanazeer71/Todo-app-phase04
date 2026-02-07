#!/usr/bin/env python3
"""
Test just the task functionality after the fix
"""
import requests
import json
import time

BACKEND_URL = "http://localhost:8000/api"

# Create a test user and get auth token
test_user = {
    "username": f"tasktest_{int(time.time())}",
    "password": "testpass123"
}

print("1. Creating test user...")
response = requests.post(f"{BACKEND_URL}/auth/signup", json=test_user)
if response.status_code == 200:
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    print("✅ User created and authenticated")
    
    print("2. Testing task creation...")
    task_data = {"title": "Test Task", "description": "Test Description"}
    response = requests.post(f"{BACKEND_URL}/tasks/", json=task_data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        task = response.json()
        task_id = task["id"]
        print(f"✅ Task created with ID: {task_id}")
        
        print("3. Testing task retrieval...")
        response = requests.get(f"{BACKEND_URL}/tasks/", headers=headers)
        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ Retrieved {len(tasks)} tasks")
            
            print("4. Testing task update...")
            update_data = {"title": "Updated Task"}
            response = requests.put(f"{BACKEND_URL}/tasks/{task_id}", json=update_data, headers=headers)
            if response.status_code == 200:
                print("✅ Task updated successfully")
                
                print("5. Testing task completion toggle...")
                response = requests.patch(f"{BACKEND_URL}/tasks/{task_id}/complete", headers=headers)
                if response.status_code == 200:
                    print("✅ Task completion toggled")
                    
                    print("6. Testing task deletion...")
                    response = requests.delete(f"{BACKEND_URL}/tasks/{task_id}", headers=headers)
                    if response.status_code == 200:
                        print("✅ Task deleted successfully")
                        print("\n🎉 ALL TASK OPERATIONS WORKING!")
                    else:
                        print(f"❌ Delete failed: {response.status_code} - {response.text}")
                else:
                    print(f"❌ Toggle failed: {response.status_code} - {response.text}")
            else:
                print(f"❌ Update failed: {response.status_code} - {response.text}")
        else:
            print(f"❌ Retrieval failed: {response.status_code} - {response.text}")
    else:
        print(f"❌ Task creation failed: {response.status_code} - {response.text}")
else:
    print(f"❌ User creation failed: {response.status_code} - {response.text}")