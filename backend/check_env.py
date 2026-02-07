#!/usr/bin/env python3
"""Environment validation script for Phase III Todo AI Chatbot."""

import os
import sys
from pathlib import Path

# Load .env file if it exists
def load_env_file():
    """Load environment variables from .env file."""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

def check_env_file():
    """Check if .env file exists and has required variables."""
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ .env file not found!")
        print("📝 Copy .env.example to .env and configure your values")
        return False
    
    print("✅ .env file found")
    return True

def check_required_vars():
    """Check if required environment variables are set."""
    required_vars = {
        "BETTER_AUTH_SECRET": "Authentication secret (must match frontend)",
        "OPENAI_API_KEY": "OpenAI API key for AI chatbot functionality"
    }
    
    optional_vars = {
        "DATABASE_URL": "Database connection string",
        "JWT_SECRET": "JWT signing secret",
        "OPENAI_ORGANIZATION_ID": "OpenAI organization ID",
        "MCP_SERVER_PORT": "MCP server port"
    }
    
    missing_required = []
    
    print("\n📋 Checking required environment variables:")
    for var, description in required_vars.items():
        value = os.getenv(var)
        if not value or value in ["", "your_strong_secret_here", "sk-your-openai-key-here"]:
            print(f"❌ {var}: {description}")
            missing_required.append(var)
        else:
            # Mask sensitive values
            if "SECRET" in var or "KEY" in var:
                masked_value = value[:8] + "..." if len(value) > 8 else "***"
                print(f"✅ {var}: {masked_value}")
            else:
                print(f"✅ {var}: {value}")
    
    print("\n📋 Checking optional environment variables:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            if "SECRET" in var or "KEY" in var:
                masked_value = value[:8] + "..." if len(value) > 8 else "***"
                print(f"✅ {var}: {masked_value}")
            else:
                print(f"✅ {var}: {value}")
        else:
            print(f"⚠️  {var}: Not set (using default)")
    
    return len(missing_required) == 0, missing_required

def validate_openai_key():
    """Validate OpenAI API key format."""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return False, "OpenAI API key not set"
    
    if not api_key.startswith("sk-"):
        return False, "OpenAI API key should start with 'sk-'"
    
    if len(api_key) < 20:
        return False, "OpenAI API key seems too short"
    
    return True, "OpenAI API key format looks valid"

def main():
    """Main validation function."""
    print("🔍 Phase III Environment Validation")
    print("=" * 40)
    
    # Load .env file first
    load_env_file()
    
    # Check .env file exists
    if not check_env_file():
        sys.exit(1)
    
    # Check required variables
    all_good, missing = check_required_vars()
    
    # Validate OpenAI key format
    print("\n🔑 Validating OpenAI API key:")
    key_valid, key_message = validate_openai_key()
    if key_valid:
        print(f"✅ {key_message}")
    else:
        print(f"❌ {key_message}")
        all_good = False
    
    # Final result
    print("\n" + "=" * 40)
    if all_good:
        print("🎉 Environment validation passed!")
        print("✅ Ready to run Phase III Todo AI Chatbot")
    else:
        print("❌ Environment validation failed!")
        if missing:
            print(f"📝 Missing required variables: {', '.join(missing)}")
        print("🔧 Please update your .env file and try again")
        sys.exit(1)

if __name__ == "__main__":
    main()