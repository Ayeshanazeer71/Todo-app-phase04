#!/usr/bin/env python3
import os
import sys
sys.path.append('backend/src')

from openai import OpenAI

# Test OpenAI connection
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello, can you help me test this connection?"}],
        max_tokens=50
    )
    
    print("✅ OpenAI connection successful!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ OpenAI connection failed: {e}")