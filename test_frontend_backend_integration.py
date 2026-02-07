#!/usr/bin/env python3
"""
Test frontend-backend integration by simulating frontend API calls
"""
import requests
import time

def test_frontend_api_integration():
    """Test the API calls that the frontend would make"""
    print("=== Testing Frontend-Backend Integration ===")
    
    # Test 1: Frontend signup flow
    print("\n1. Testing frontend signup API call...")
    test_user = {
        "username": f"frontend_test_{int(time.time())}",
        "password": "testpass123"
    }
    
    try:
        # This is exactly how the frontend calls the API
        response = requests.post(
            "http://localhost:8000/api/auth/signup",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data["access_token"]
            print("✅ Frontend signup API call successful")
            
            # Test 2: Frontend task creation
            print("\n2. Testing frontend task creation API call...")
            task_data = {"title": "Frontend Test Task", "description": "Created via frontend API"}
            
            response = requests.post(
                "http://localhost:8000/api/tasks/",
                json=task_data,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {token}"
                }
            )
            
            if response.status_code == 200:
                task = response.json()
                print(f"✅ Frontend task creation successful: {task['title']}")
                
                # Test 3: Frontend task list
                print("\n3. Testing frontend task list API call...")
                response = requests.get(
                    "http://localhost:8000/api/tasks/",
                    headers={"Authorization": f"Bearer {token}"}
                )
                
                if response.status_code == 200:
                    tasks = response.json()
                    print(f"✅ Frontend task list successful: {len(tasks)} tasks")
                    
                    print("\n🎉 Frontend-Backend Integration Working!")
                    return True
                else:
                    print(f"❌ Task list failed: {response.status_code}")
            else:
                print(f"❌ Task creation failed: {response.status_code}")
        else:
            print(f"❌ Signup failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
    
    return False

if __name__ == "__main__":
    success = test_frontend_api_integration()
    if success:
        print("\n✅ All frontend-backend integration tests passed!")
    else:
        print("\n❌ Some integration tests failed.")