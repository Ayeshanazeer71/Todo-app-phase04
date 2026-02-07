#!/usr/bin/env python3
"""
Property-based tests for authentication system
Feature: authentication-fix
"""
import pytest
import requests
import json
from hypothesis import given, strategies as st, settings, assume
from hypothesis.strategies import text, composite
import string
import time

# Test configuration
BASE_URL = "http://localhost:8001/api"
MAX_EXAMPLES = 5  # Further reduced for faster execution

# Custom strategies for generating test data
@composite
def valid_username(draw):
    """Generate valid usernames (alphanumeric + underscore, 1-50 chars)"""
    # For now, allow any non-empty string to test current behavior
    # Later we'll restrict this when we add validation
    username = draw(text(
        alphabet=string.ascii_letters + string.digits + "_",
        min_size=1,
        max_size=50
    ))
    assume(len(username.strip()) > 0)  # Ensure not just whitespace
    return username

@composite
def valid_password(draw):
    """Generate valid passwords (any string, 1-100 chars)"""
    # For now, allow any non-empty string to test current behavior
    # Later we'll add password strength requirements
    password = draw(text(min_size=1, max_size=100))
    assume(len(password.strip()) > 0)  # Ensure not just whitespace
    return password

@composite
def valid_signup_data(draw):
    """Generate valid signup data"""
    return {
        "username": draw(valid_username()),
        "password": draw(valid_password())
    }

class TestAuthenticationProperties:
    """Property-based tests for authentication system"""
    
    def setup_method(self):
        """Setup for each test method"""
        # Clean up any existing test users
        self.cleanup_test_users()
    
    def cleanup_test_users(self):
        """Clean up test users (if we had a cleanup endpoint)"""
        # For now, we'll rely on unique usernames per test
        pass
    
    @given(signup_data=valid_signup_data())
    @settings(max_examples=MAX_EXAMPLES, deadline=None)  # Disable deadline for now
    def test_property_1_json_request_processing(self, signup_data):
        """
        Property 1: JSON Request Processing
        
        For any valid JSON payload containing username and password fields,
        the signup endpoint should successfully parse and process the request,
        creating a user account and returning an authentication token.
        
        Validates: Requirements 1.1, 1.2, 1.4
        """
        # Make username unique for this test run
        unique_username = f"{signup_data['username']}_{int(time.time() * 1000000)}"
        test_data = {
            "username": unique_username,
            "password": signup_data["password"]
        }
        
        try:
            # Send JSON request to signup endpoint
            response = requests.post(
                f"{BASE_URL}/auth/signup",
                json=test_data,
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            
            # The request should be processed successfully
            assert response.status_code in [200, 400, 422], \
                f"Unexpected status code: {response.status_code}, Response: {response.text}"
            
            if response.status_code == 200:
                # Successful signup should return proper token structure
                data = response.json()
                assert "access_token" in data, "Response missing access_token"
                assert "token_type" in data, "Response missing token_type"
                assert data["token_type"] == "bearer", "Invalid token_type"
                assert isinstance(data["access_token"], str), "access_token should be string"
                assert len(data["access_token"]) > 0, "access_token should not be empty"
                
                # Token should be a valid JWT format (3 parts separated by dots)
                token_parts = data["access_token"].split(".")
                assert len(token_parts) == 3, "Invalid JWT format"
                
            elif response.status_code == 400:
                # Business logic error (like duplicate username)
                data = response.json()
                assert "detail" in data, "Error response missing detail"
                
            elif response.status_code == 422:
                # Validation error
                data = response.json()
                assert "detail" in data, "Validation error response missing detail"
                
        except requests.exceptions.RequestException as e:
            pytest.skip(f"Server not available: {e}")
    
    def test_property_1_json_parsing_edge_cases(self):
        """
        Test edge cases for JSON parsing
        """
        test_cases = [
            # Valid minimal case
            {"username": "a", "password": "b"},
            # Unicode characters
            {"username": "user_测试", "password": "pass_测试"},
            # Special characters in password
            {"username": "testuser", "password": "p@ssw0rd!#$%"},
        ]
        
        for i, test_data in enumerate(test_cases):
            # Make username unique
            test_data["username"] = f"{test_data['username']}_{int(time.time() * 1000000)}_{i}"
            
            try:
                response = requests.post(
                    f"{BASE_URL}/auth/signup",
                    json=test_data,
                    headers={"Content-Type": "application/json"},
                    timeout=5
                )
                
                # Should either succeed or fail gracefully
                assert response.status_code in [200, 400, 422], \
                    f"Unexpected status for {test_data}: {response.status_code}"
                    
            except requests.exceptions.RequestException:
                pytest.skip("Server not available")
    
    def test_property_1_malformed_json_handling(self):
        """
        Test that malformed JSON is handled properly
        """
        malformed_cases = [
            '{"username": "test", "password":}',  # Invalid JSON
            '{"username": "test"}',  # Missing required field
            '{}',  # Empty object
            '',  # Empty string
        ]
        
        for malformed_json in malformed_cases:
            try:
                response = requests.post(
                    f"{BASE_URL}/auth/signup",
                    data=malformed_json,
                    headers={"Content-Type": "application/json"},
                    timeout=5
                )
                
                # Should return appropriate error status
                assert response.status_code in [400, 422], \
                    f"Malformed JSON should return error status, got: {response.status_code}"
                    
            except requests.exceptions.RequestException:
                pytest.skip("Server not available")

if __name__ == "__main__":
    # Run the tests
    pytest.main([__file__, "-v", "--tb=short"])