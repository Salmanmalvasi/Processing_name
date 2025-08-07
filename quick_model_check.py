#!/usr/bin/env python3
"""
Quick Model Checker for AI NPC Dialogue Generator
Fast status verification and testing for Groq API
"""

import requests
import time

def quick_check():
    print("🔍 Quick Model Checker (Groq)")
    print("=" * 40)
    
    # Check Groq
    print("\n🔍 Checking Groq API (Port 8002)...")
    try:
        response = requests.get("http://127.0.0.1:8002/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Groq API: Running")
            print(f"   Model: llama3-8b-8192")
            print(f"   Rate Limit: {data['rate_limit']['requests_this_minute']}/{data['rate_limit']['max_requests_per_minute']}")
            
            # Quick test
            print("\n🧪 Quick test...")
            test_payload = {
                "character_name": "Drogun",
                "character_type": "Gruff Blacksmith",
                "traits": "Gruff, impatient, values hard work",
                "player_input": "Hello"
            }
            
            start_time = time.time()
            test_response = requests.post("http://127.0.0.1:8002/generate", json=test_payload, timeout=10)
            end_time = time.time()
            
            if test_response.status_code == 200:
                result = test_response.json()
                print(f"✅ Test successful!")
                print(f"   Response time: {(end_time - start_time):.2f}s")
                print(f"   Response: {result.get('reply', 'No response')}")
            else:
                print(f"❌ Test failed: {test_response.status_code}")
        else:
            print(f"❌ Groq API: HTTP {response.status_code}")
    except Exception as e:
        print(f"❌ Groq API: {e}")
    
    print("\n💡 Ready to chat! Run 'python3 chat_fixed.py' or 'python3 quick_chat_groq.py'")

if __name__ == "__main__":
    quick_check() 