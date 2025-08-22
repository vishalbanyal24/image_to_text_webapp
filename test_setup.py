#!/usr/bin/env python3
"""
Test script to verify the Image to Text Generator setup
"""

import os
import sys
import requests
from PIL import Image
from io import BytesIO

def test_environment():
    """Test environment variables and dependencies"""
    print("🔍 Testing Environment Setup...")
    
    # Check Python version
    print(f"✅ Python version: {sys.version}")
    
    # Check required packages
    try:
        import django
        print(f"✅ Django version: {django.get_version()}")
    except ImportError:
        print("❌ Django not installed")
        return False
    
    try:
        import langchain_google_genai
        print("✅ LangChain Google GenAI installed")
    except ImportError:
        print("❌ LangChain Google GenAI not installed")
        return False
    
    try:
        import PIL
        print(f"✅ Pillow version: {PIL.__version__}")
    except ImportError:
        print("❌ Pillow not installed")
        return False
    
    # Check environment variables
    api_key = os.environ.get('GOOGLE_API_KEY')
    if api_key:
        print("✅ GOOGLE_API_KEY is set")
        print(f"   Key starts with: {api_key[:10]}...")
    else:
        print("❌ GOOGLE_API_KEY not set")
        print("   Set it with: $env:GOOGLE_API_KEY='your-key-here' (PowerShell)")
        print("   or: export GOOGLE_API_KEY='your-key-here' (Linux/Mac)")
        return False
    
    return True

def test_image_download():
    """Test downloading a sample image"""
    print("\n🖼️  Testing Image Download...")
    
    test_url = "https://picsum.photos/400/300"
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; ImageToTextBot/1.0)"}
        response = requests.get(test_url, timeout=10, headers=headers)
        response.raise_for_status()
        
        # Try to open as image
        image = Image.open(BytesIO(response.content))
        print(f"✅ Successfully downloaded and opened image: {image.size}")
        return True
    except Exception as e:
        print(f"❌ Failed to download test image: {e}")
        return False

def test_google_api():
    """Test Google API connectivity"""
    print("\n🤖 Testing Google API...")
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_core.messages import HumanMessage
        
        api_key = os.environ.get('GOOGLE_API_KEY')
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)
        
        message = HumanMessage(content="Say 'Hello, API is working!'")
        response = llm.invoke([message])
        
        print(f"✅ Google API is working!")
        print(f"   Response: {response.content}")
        return True
    except Exception as e:
        print(f"❌ Google API test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Image to Text Generator - Setup Test")
    print("=" * 50)
    
    # Test environment
    env_ok = test_environment()
    if not env_ok:
        print("\n❌ Environment setup failed. Please fix the issues above.")
        return
    
    # Test image download
    download_ok = test_image_download()
    if not download_ok:
        print("\n❌ Image download test failed.")
        return
    
    # Test Google API
    api_ok = test_google_api()
    if not api_ok:
        print("\n❌ Google API test failed.")
        return
    
    print("\n🎉 All tests passed! Your setup is ready.")
    print("\nNext steps:")
    print("1. Start Django server: python manage.py runserver")
    print("2. Open: http://localhost:8000")
    print("3. Try uploading an image or using a URL")

if __name__ == "__main__":
    main()
