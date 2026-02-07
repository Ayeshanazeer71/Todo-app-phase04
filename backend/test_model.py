#!/usr/bin/env python3
"""
Test the UserCreate model directly
"""
import sys
import os
sys.path.append('src')

from app.models.user import UserCreate
import json

def test_user_create_model():
    print("=== Testing UserCreate Model ===")
    
    # Test 1: Valid data
    print("\n1. Testing valid data...")
    try:
        valid_data = {"username": "testuser", "password": "testpass"}
        user = UserCreate(**valid_data)
        print(f"✅ Valid data test PASSED: {user}")
    except Exception as e:
        print(f"❌ Valid data test FAILED: {e}")
    
    # Test 2: JSON parsing (simulating FastAPI behavior)
    print("\n2. Testing JSON parsing...")
    try:
        json_data = '{"username": "testuser", "password": "testpass"}'
        parsed_data = json.loads(json_data)
        user = UserCreate(**parsed_data)
        print(f"✅ JSON parsing test PASSED: {user}")
    except Exception as e:
        print(f"❌ JSON parsing test FAILED: {e}")
    
    # Test 3: Missing field
    print("\n3. Testing missing field...")
    try:
        invalid_data = {"username": "testuser"}  # Missing password
        user = UserCreate(**invalid_data)
        print(f"❌ Missing field test FAILED: Should have raised an error")
    except Exception as e:
        print(f"✅ Missing field test PASSED: {e}")
    
    # Test 4: Empty values
    print("\n4. Testing empty values...")
    try:
        empty_data = {"username": "", "password": ""}
        user = UserCreate(**empty_data)
        print(f"✅ Empty values test: {user} (Note: No validation rules yet)")
    except Exception as e:
        print(f"❌ Empty values test FAILED: {e}")

if __name__ == "__main__":
    test_user_create_model()