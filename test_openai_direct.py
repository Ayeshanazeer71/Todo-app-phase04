#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv('backend/.env')

print("Testing OpenAI connection directly...")
print(f"API Key present: {bool(os.getenv('OPENAI_API_KEY'))}")

try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    print("Making test request to OpenAI...")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello and confirm you can help with tasks."}
        ],
        max_tokens=50
    )
    
    print("✅ OpenAI connection successful!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ OpenAI connection failed: {e}")
    import traceback
    traceback.print_exc()