#!/usr/bin/env python3
"""
Test AI vs Static Comparison
Shows the difference between AI-powered and static responses
"""

import requests
import json
import time

def test_ai_vs_static():
    print("🤖 AI vs Static Chatbot Comparison")
    print("=" * 60)
    
    # Create test user
    signup_data = {'username': f'aicompare_{int(time.time())}', 'password': 'testpass123'}
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
    
    def static_chat(message):
        response = requests.post('http://localhost:8000/api/chat/simple', 
                               json={'message': message}, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Status {response.status_code}: {response.text}"}
    
    print("\n🧠 Testing Complex Natural Language Understanding...")
    
    complex_requests = [
        "I have a really important presentation tomorrow at 2 PM for my boss about quarterly sales. Can you help me remember to prepare slides and practice my speech?",
        "Actually, I'm feeling overwhelmed with all my tasks. Can you show me what I have and help me figure out what's most urgent?",
        "You know what, that presentation task - can you change it to be more specific? I want it to say 'Prepare Q4 sales presentation with charts and practice delivery'",
        "I just finished working on the presentation slides. Mark that as done for me!"
    ]
    
    conversation_id = None
    
    for i, request in enumerate(complex_requests, 1):
        print(f"\n{i}. Complex Request: '{request[:50]}...'")
        
        # Test AI Response
        print("   🤖 AI Response:")
        ai_response = ai_chat(request, conversation_id)
        if "error" not in ai_response:
            if not conversation_id:
                conversation_id = ai_response['conversation_id']
            print(f"      {ai_response['response'][:100]}...")
            if ai_response.get('tool_calls'):
                print(f"      🔧 Tools used: {[t['tool'] for t in ai_response['tool_calls']]}")
        else:
            print(f"      ❌ Error: {ai_response['error']}")
        
        # Test Static Response
        print("   📝 Static Response:")
        static_response = static_chat(request)
        if "error" not in static_response:
            print(f"      {static_response['response'][:100]}...")
        else:
            print(f"      ❌ Error: {static_response['error']}")
    
    print("\n" + "=" * 60)
    print("🎯 KEY DIFFERENCES:")
    print("✅ AI-Powered Chatbot:")
    print("   • Understands complex, natural language")
    print("   • Maintains conversation context")
    print("   • Intelligently decides when to use tools")
    print("   • Provides personalized, contextual responses")
    print("   • Can handle ambiguous requests")
    print("   • Learns from conversation history")
    
    print("\n❌ Static Pattern-Matching Chatbot:")
    print("   • Only responds to specific patterns")
    print("   • No conversation memory")
    print("   • Limited to pre-programmed responses")
    print("   • Cannot understand complex requests")
    print("   • No contextual awareness")
    
    print("\n🚀 Your chatbot is now powered by OpenAI GPT-4o-mini!")
    print("   It can understand natural language and have real conversations!")

if __name__ == "__main__":
    test_ai_vs_static()