#!/usr/bin/env python3
import requests
import json

def test_api():
    url = "http://127.0.0.1:8001/generate"
    payload = {
        "character_name": "Drogun",
        "character_type": "Gruff Blacksmith", 
        "traits": "Gruff, impatient, values hard work",
        "player_input": "hey"
    }
    
    print("Testing API call...")
    print(f"URL: {url}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api() 