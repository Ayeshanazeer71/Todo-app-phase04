#!/usr/bin/env python3
import requests
import json

# Test the enhanced chatbot
try:
    # Create a test user
    signup_data = {'username': 'testuser3', 'password': 'testpass123'}
    response = requests.post('http://localhost:8000/api/auth/signup', json=signup_data)
    
    if response.status_code == 200:
        token = response.json()['access_token']
        print('✅ User created successfully')
    else:
        # Try login instead
        response = requests.post('http://localhost:8000/api/auth/login', json=signup_data)
        if response.status_code == 200:
            token = response.json()['access_token']
            print('✅ User logged in successfully')
        else:
            print('❌ Failed to authenticate')
            exit(1)
    
    headers = {'Authorization': f'Bearer {token}'}
    
    # Test natural language patterns
    test_messages = [
        'hello',
        'I need to buy groceries',
        'What are my tasks?',
        'Show me what I need to do',
        'help'
    ]
    
    for msg in test_messages:
        response = requests.post('http://localhost:8000/api/chat/simple', 
                               json={'message': msg}, headers=headers)
        if response.status_code == 200:
            result = response.json()
            print(f'✅ "{msg}" -> {result["response"][:60]}...')
        else:
            print(f'❌ "{msg}" -> Error {response.status_code}')
        
except Exception as e:
    print(f'Error: {e}')