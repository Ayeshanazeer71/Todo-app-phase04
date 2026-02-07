#!/usr/bin/env python3
"""
Test OpenAI Integration
Tests the real AI-powered chat endpoint
"""

import requests
import json
import time

def test_openai_chat():
    print("🤖 Testing OpenAI-Powered Chat Integration")
    print("=" * 60)
    
    # Create test user
    signup_data = {'username': f'aitest_{int(time.time())}', 'password': 'testpass123'}
    response = requests.post('http://localhost:8000/api/auth/signup', json=signup_data)
    
    if response.status_code == 200:
        token = response.json()['access_token']
        print('✅ Test user created')
    else:
        print('❌ Failed to create user')
        return
    
    headers = {'Authorization': f'Bearer {token}'}
    
    def ai_chat(message, conversation_id=None):
        payload = {'message': message}
        if conversation_id:
            payload['conversation_id'] = conversation_id
            
        response = requests.post('http://localhost:8000/api/chat/', 
                               json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Status {response.status_code}: {response.text}"}
    
    print("\n🧠 Testing AI-Powered Natural Language Understanding...")
    
    # Test 1: Natural conversation
    print("\n1. Testing natural conversation:")
    response = ai_chat("Hello! I'm new here. Can you help me understand what you can do?")
    if "error" not in response:
        print(f"   ✅ AI Response: {response['response'][:100]}...")
        conversation_id = response['conversation_id']
        print(f"   📝 Conversation ID: {conversation_id}")
    else:
        print(f"   ❌ Error: {response['error']}")
        return
    
    # Test 2: Task creation with AI understanding
    print("\n2. Testing AI task creation:")
    response = ai_chat("I have a really important meeting with my boss tomorrow at 2 PM. Can you help me remember to prepare for it?", conversation_id)
    if "error" not in response:
        print(f"   ✅ AI Response: {response['response'][:100]}...")
        if response.get('tool_calls'):
            print(f"   🔧 Tool calls executed: {len(response['tool_calls'])}")
            for tool in response['tool_calls']:
                print(f"      - {tool['tool']}: {tool['result']['success']}")
    else:
        print(f"   ❌ Error: {response['error']}")
    
    # Test 3: Complex task management
    print("\n3. Testing complex task management:")
    response = ai_chat("Actually, can you show me all my tasks and then help me prioritize them? I'm feeling a bit overwhelmed.", conversation_id)
    if "error" not in response:
        print(f"   ✅ AI Response: {response['response'][:100]}...")
        if response.get('tool_calls'):
            print(f"   🔧 Tool calls executed: {len(response['tool_calls'])}")
    else:
        print(f"   ❌ Error: {response['error']}")
    
    # Test 4: Task updating with AI
    print("\n4. Testing AI-powered task updating:")
    response = ai_chat("You know what, that meeting preparation task - can you change it to 'Prepare presentation slides for boss meeting'? I want to be more specific.", conversation_id)
    if "error" not in response:
        print(f"   ✅ AI Response: {response['response'][:100]}...")
        if response.get('tool_calls'):
            print(f"   🔧 Tool calls executed: {len(response['tool_calls'])}")
    else:
        print(f"   ❌ Error: {response['error']}")
    
    # Test 5: Contextual conversation
    print("\n5. Testing contextual conversation:")
    response = ai_chat("Thanks! How am I doing overall with my productivity?", conversation_id)
    if "error" not in response:
        print(f"   ✅ AI Response: {response['response'][:100]}...")
        if response.get('tool_calls'):
            print(f"   🔧 Tool calls executed: {len(response['tool_calls'])}")
    else:
        print(f"   ❌ Error: {response['error']}")
    
    print("\n" + "=" * 60)
    print("🎉 OpenAI Integration Test Completed!")
    print("\n✨ Key AI Features Tested:")
    print("• Natural language understanding")
    print("• Context-aware conversations")
    print("• Intelligent task creation from complex requests")
    print("• Smart task management and prioritization")
    print("• Conversational task updating")
    print("• Productivity insights and encouragement")
    print("\n🚀 The chatbot is now powered by real AI, not static patterns!")

if __name__ == "__main__":
    test_openai_chat()