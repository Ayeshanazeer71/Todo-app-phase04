#!/usr/bin/env python3
"""
Test script to verify signup functionality
"""
import requests
import json
import sys

def test_signup():
    """Test the signup endpoint with various scenarios"""
    base_url = "http://localhost:8001/api"
    
    print("=== Testing Signup Functionality ===")
    
    # Test 1: Valid signup
    print("\n1. Testing valid signup...")
    test_user = {
        "username": "testuser123",
        "password": "testpassword123"
    }
    
    try:
        response = requests.post(
            f"{base_url}/auth/signup",
            json=test_user,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            print("✅ Valid signup test PASSED")
            data = response.json()
            if "access_token" in data and "token_type" in data:
                print("✅ Response format is correct")
            else:
                print("❌ Response format is incorrect")
        else:
            print("❌ Valid signup test FAILED")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Is the backend running on localhost:8000?")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    # Test 2: Duplicate username
    print("\n2. Testing duplicate username...")
    try:
        response = requests.post(
            f"{base_url}/auth/signup",
            json=test_user,  # Same user as before
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 400:
            print("✅ Duplicate username test PASSED")
        else:
            print("❌ Duplicate username test FAILED")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    # Test 3: Invalid data
    print("\n3. Testing invalid data (missing password)...")
    try:
        invalid_user = {"username": "testuser456"}  # Missing password
        response = requests.post(
            f"{base_url}/auth/signup",
            json=invalid_user,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 422:
            print("✅ Invalid data test PASSED")
        else:
            print("❌ Invalid data test FAILED")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    # Test 4: Empty username
    print("\n4. Testing empty username...")
    try:
        invalid_user = {"username": "", "password": "testpass"}
        response = requests.post(
            f"{base_url}/auth/signup",
            json=invalid_user,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code in [400, 422]:
            print("✅ Empty username test PASSED")
        else:
            print("❌ Empty username test FAILED")
            
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    return True

if __name__ == "__main__":
    success = test_signup()
    if success:
        print("\n=== Test completed ===")
    else:
        print("\n=== Test failed to run ===")
        sys.exit(1)