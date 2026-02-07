#!/usr/bin/env python3
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv('backend/.env')

print("Environment variables:")
print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')[:20]}..." if os.getenv('OPENAI_API_KEY') else "OPENAI_API_KEY: Not found")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')[:30]}..." if os.getenv('DATABASE_URL') else "DATABASE_URL: Not found")

# Test OpenAI
try:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Hello, test message"}],
        max_tokens=20
    )
    
    print("✅ OpenAI connection successful!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ OpenAI connection failed: {e}")