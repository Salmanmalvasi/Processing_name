#!/usr/bin/env python3
"""
Test script for Vercel deployment
"""

import requests
import json

def test_local_app():
    """Test the Flask app locally"""
    base_url = "http://localhost:8080"
    
    print("🧪 Testing AI NPC Dialogue Generator...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test API status
    try:
        response = requests.get(f"{base_url}/api/status")
        print(f"✅ API status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ API status failed: {e}")
    
    # Test characters endpoint
    try:
        response = requests.get(f"{base_url}/api/characters")
        print(f"✅ Characters: {response.status_code}")
        characters = response.json()
        print(f"   Found {len(characters)} characters")
    except Exception as e:
        print(f"❌ Characters failed: {e}")
    
    # Test chat endpoint
    try:
        chat_data = {
            "message": "Hello",
            "character": "drogun",
            "model": "llama3-8b-8192"
        }
        response = requests.post(f"{base_url}/chat", json=chat_data)
        print(f"✅ Chat test: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Reply: {result.get('reply', 'No reply')[:100]}...")
        else:
            print(f"   Error: {response.json()}")
    except Exception as e:
        print(f"❌ Chat test failed: {e}")

if __name__ == "__main__":
    test_local_app() 