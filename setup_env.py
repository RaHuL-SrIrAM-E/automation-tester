#!/usr/bin/env python3
"""
Helper script to set up the .env file with Gemini API credentials
"""

import os

def create_env_file():
    """Create .env file with the provided Gemini credentials"""
    
    env_content = """# Gemini API Configuration
GEMINI_API_URL=https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent
GEMINI_API_KEY=AIzaSyAAy8qvRuJavw6h7Se2weyQSkHFRKu3dow

# Flask Configuration (optional)
FLASK_ENV=development
FLASK_DEBUG=True
"""
    
    try:
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ .env file created successfully!")
        print("📝 File contents:")
        print("-" * 50)
        print(env_content)
        print("-" * 50)
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {str(e)}")
        return False

def main():
    """Main function"""
    print("🔧 Setting up environment variables...")
    
    if os.path.exists('.env'):
        print("⚠️  .env file already exists. Do you want to overwrite it? (y/n): ", end="")
        response = input().lower().strip()
        if response != 'y':
            print("❌ Setup cancelled.")
            return
    
    if create_env_file():
        print("\n🎉 Environment setup complete!")
        print("🚀 You can now run the application with LLM integration:")
        print("   python3 app.py")
    else:
        print("\n❌ Setup failed. Please create the .env file manually.")

if __name__ == "__main__":
    main() 