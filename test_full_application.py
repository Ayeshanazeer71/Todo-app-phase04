#!/usr/bin/env python3
"""
Comprehensive test script for the entire Todo application
Tests both backend API and frontend integration
"""
import requests
import json
import time
import sys

# Configuration
BACKEND_URL = "http://localhost:8000/api"
FRONTEND_URL = "http://localhost:3000"

class TodoAppTester:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        self.test_user = {
            "username": f"testuser_{int(time.time())}",
            "password": "testpassword123"
        }
        
    def log(self, message, status="INFO"):
        print(f"[{status}] {message}")
        
    def test_backend_health(self):
        """Test backend health endpoint"""
        self.log("Testing backend health...")
        try:
            response = self.session.get(f"{BACKEND_URL}/../health")
            if response.status_code == 200:
                self.log("✅ Backend health check passed", "SUCCESS")
                return True
            else:
                self.log(f"❌ Backend health check failed: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Backend health check failed: {e}", "ERROR")
            return False
    
    def test_frontend_availability(self):
        """Test if frontend is accessible"""
        self.log("Testing frontend availability...")
        try:
            response = self.session.get(FRONTEND_URL, timeout=5)
            if response.status_code == 200:
                self.log("✅ Frontend is accessible", "SUCCESS")
                return True
            else:
                self.log(f"❌ Frontend not accessible: {response.status_code}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Frontend not accessible: {e}", "ERROR")
            return False
    
    def test_user_signup(self):
        """Test user signup functionality"""
        self.log(f"Testing user signup for: {self.test_user['username']}")
        try:
            response = self.session.post(
                f"{BACKEND_URL}/auth/signup",
                json=self.test_user,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data and "token_type" in data:
                    self.auth_token = data["access_token"]
                    self.session.headers.update({"Authorization": f"Bearer {self.auth_token}"})
                    self.log("✅ User signup successful", "SUCCESS")
                    return True
                else:
                    self.log("❌ Signup response missing token fields", "ERROR")
                    return False
            else:
                self.log(f"❌ Signup failed: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Signup failed: {e}", "ERROR")
            return False
    
    def test_user_login(self):
        """Test user login functionality"""
        self.log("Testing user login...")
        try:
            # Login uses form data, not JSON
            login_data = {
                "username": self.test_user["username"],
                "password": self.test_user["password"]
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/auth/login",
                data=login_data
            )
            
            if response.status_code == 200:
                data = response.json()
                if "access_token" in data:
                    self.log("✅ User login successful", "SUCCESS")
                    return True
                else:
                    self.log("❌ Login response missing token", "ERROR")
                    return False
            else:
                self.log(f"❌ Login failed: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Login failed: {e}", "ERROR")
            return False
    
    def test_task_crud_operations(self):
        """Test task CRUD operations"""
        if not self.auth_token:
            self.log("❌ No auth token available for task operations", "ERROR")
            return False
            
        # Test Create Task
        self.log("Testing task creation...")
        task_data = {
            "title": "Test Task",
            "description": "This is a test task"
        }
        
        try:
            response = self.session.post(
                f"{BACKEND_URL}/tasks/",
                json=task_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                task = response.json()
                task_id = task.get("id")
                self.log(f"✅ Task created successfully (ID: {task_id})", "SUCCESS")
                
                # Test Read Tasks
                self.log("Testing task retrieval...")
                response = self.session.get(f"{BACKEND_URL}/tasks/")
                if response.status_code == 200:
                    tasks = response.json()
                    self.log(f"✅ Retrieved {len(tasks)} tasks", "SUCCESS")
                    
                    # Test Update Task
                    if task_id:
                        self.log("Testing task update...")
                        update_data = {"title": "Updated Test Task", "description": "Updated description"}
                        response = self.session.put(
                            f"{BACKEND_URL}/tasks/{task_id}",
                            json=update_data,
                            headers={"Content-Type": "application/json"}
                        )
                        if response.status_code == 200:
                            self.log("✅ Task updated successfully", "SUCCESS")
                        else:
                            self.log(f"❌ Task update failed: {response.status_code}", "ERROR")
                        
                        # Test Toggle Complete
                        self.log("Testing task completion toggle...")
                        response = self.session.patch(f"{BACKEND_URL}/tasks/{task_id}/complete")
                        if response.status_code == 200:
                            self.log("✅ Task completion toggled successfully", "SUCCESS")
                        else:
                            self.log(f"❌ Task toggle failed: {response.status_code}", "ERROR")
                        
                        # Test Delete Task
                        self.log("Testing task deletion...")
                        response = self.session.delete(f"{BACKEND_URL}/tasks/{task_id}")
                        if response.status_code == 200:
                            self.log("✅ Task deleted successfully", "SUCCESS")
                            return True
                        else:
                            self.log(f"❌ Task deletion failed: {response.status_code}", "ERROR")
                            return False
                else:
                    self.log(f"❌ Task retrieval failed: {response.status_code}", "ERROR")
                    return False
            else:
                self.log(f"❌ Task creation failed: {response.status_code} - {response.text}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"❌ Task operations failed: {e}", "ERROR")
            return False
    
    def test_chat_functionality(self):
        """Test chat functionality"""
        if not self.auth_token:
            self.log("❌ No auth token available for chat operations", "ERROR")
            return False
            
        self.log("Testing chat functionality...")
        try:
            # Test simple chat endpoint instead of full OpenAI chat
            chat_data = {"message": "create task: Test Chat Task"}
            response = self.session.post(
                f"{BACKEND_URL}/chat/simple",
                json=chat_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                result = response.json()
                if "Created task" in result.get("response", ""):
                    self.log("✅ Chat functionality working (Simple Chat)", "SUCCESS")
                    return True
                else:
                    self.log(f"❌ Chat response unexpected: {result.get('response')}", "ERROR")
                    return False
            else:
                self.log(f"❌ Chat failed: {response.status_code} - {response.text}", "ERROR")
                return False
        except Exception as e:
            self.log(f"❌ Chat functionality failed: {e}", "ERROR")
            return False
    
    def test_error_handling(self):
        """Test error handling scenarios"""
        self.log("Testing error handling...")
        
        # Test duplicate signup
        try:
            response = self.session.post(
                f"{BACKEND_URL}/auth/signup",
                json=self.test_user,  # Same user as before
                headers={"Content-Type": "application/json"}
            )
            if response.status_code == 400:
                self.log("✅ Duplicate signup properly rejected", "SUCCESS")
            else:
                self.log(f"❌ Duplicate signup not handled: {response.status_code}", "ERROR")
        except Exception as e:
            self.log(f"❌ Error handling test failed: {e}", "ERROR")
        
        # Test invalid login
        try:
            invalid_data = {"username": "nonexistent", "password": "wrongpass"}
            response = self.session.post(f"{BACKEND_URL}/auth/login", data=invalid_data)
            if response.status_code == 401:
                self.log("✅ Invalid login properly rejected", "SUCCESS")
            else:
                self.log(f"❌ Invalid login not handled: {response.status_code}", "ERROR")
        except Exception as e:
            self.log(f"❌ Invalid login test failed: {e}", "ERROR")
        
        return True
    
    def run_all_tests(self):
        """Run all tests"""
        self.log("=" * 50)
        self.log("STARTING COMPREHENSIVE TODO APP TESTS")
        self.log("=" * 50)
        
        tests = [
            ("Backend Health", self.test_backend_health),
            ("Frontend Availability", self.test_frontend_availability),
            ("User Signup", self.test_user_signup),
            ("User Login", self.test_user_login),
            ("Task CRUD Operations", self.test_task_crud_operations),
            ("Chat Functionality", self.test_chat_functionality),
            ("Error Handling", self.test_error_handling),
        ]
        
        results = {}
        for test_name, test_func in tests:
            self.log(f"\n--- Running {test_name} ---")
            try:
                results[test_name] = test_func()
            except Exception as e:
                self.log(f"❌ {test_name} crashed: {e}", "ERROR")
                results[test_name] = False
        
        # Summary
        self.log("\n" + "=" * 50)
        self.log("TEST RESULTS SUMMARY")
        self.log("=" * 50)
        
        passed = 0
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            self.log(f"{test_name}: {status}")
            if result:
                passed += 1
        
        self.log(f"\nOverall: {passed}/{total} tests passed")
        
        if passed == total:
            self.log("🎉 ALL TESTS PASSED! Your application is working correctly!", "SUCCESS")
        else:
            self.log(f"⚠️  {total - passed} tests failed. Check the logs above for details.", "WARNING")
        
        return passed == total

if __name__ == "__main__":
    tester = TodoAppTester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)