#!/usr/bin/env python3
"""
Test script for AI NPC Dialogue Generator
Tests both Phase 1 and Phase 2 APIs
"""

import requests
import json
import time

# API URLs
PHASE1_URL = "http://127.0.0.1:8000/generate"
PHASE2_URL = "http://127.0.0.1:8001/generate"
PHASE2_SAMPLES_URL = "http://127.0.0.1:8001/sample-npcs"

def test_phase1():
    """Test Phase 1 API"""
    print("🧪 Testing Phase 1 (Basic)")
    print("=" * 50)
    
    test_cases = [
        {
            "name": "Gorak",
            "type": "Orc Blacksmith",
            "traits": "Gruff, loyal, speaks in short sentences",
            "message": "Can you repair my sword?"
        },
        {
            "name": "Lira",
            "type": "Potion Seller",
            "traits": "Cheerful, talkative, always tries to upsell",
            "message": "I need a healing potion"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['name']} ({test_case['type']})")
        print(f"Player: {test_case['message']}")
        
        try:
            response = requests.post(PHASE1_URL, json=test_case)
            if response.status_code == 200:
                result = response.json()
                print(f"NPC: {result['reply']}")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Exception: {e}")

def test_phase2():
    """Test Phase 2 API"""
    print("\n🧪 Testing Phase 2 (Advanced)")
    print("=" * 50)
    
    # Test basic generation
    test_case = {
        "character_name": "Drogun",
        "character_type": "Gruff Blacksmith",
        "traits": "Gruff, impatient, values hard work, speaks in short sentences",
        "player_input": "Can you repair my sword?"
    }
    
    print(f"\nTest 1: {test_case['character_name']} ({test_case['character_type']})")
    print(f"Player: {test_case['player_input']}")
    
    try:
        response = requests.post(PHASE2_URL, json=test_case)
        if response.status_code == 200:
            result = response.json()
            print(f"NPC: {result['reply']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    # Test with conversation history
    test_case_with_history = {
        "character_name": "Lira",
        "character_type": "Enthusiastic Potion Seller",
        "traits": "Cheerful, talkative, always tries to upsell, uses lots of exclamations",
        "player_input": "Do you have anything stronger?",
        "conversation_history": [
            {"speaker": "Player", "text": "I need a healing potion"},
            {"speaker": "Lira", "text": "Oh, you are in luck! I have the finest healing elixirs in the realm! Only 25 gold for the premium blend!"}
        ]
    }
    
    print(f"\nTest 2: {test_case_with_history['character_name']} with conversation history")
    print(f"Player: {test_case_with_history['player_input']}")
    
    try:
        response = requests.post(PHASE2_URL, json=test_case_with_history)
        if response.status_code == 200:
            result = response.json()
            print(f"NPC: {result['reply']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

def test_sample_npcs():
    """Test sample NPCs endpoint"""
    print("\n🧪 Testing Sample NPCs")
    print("=" * 50)
    
    try:
        response = requests.get(PHASE2_SAMPLES_URL)
        if response.status_code == 200:
            result = response.json()
            print(f"Found {len(result['npcs'])} sample NPCs:")
            for npc in result['npcs']:
                print(f"  - {npc['name']}: {npc['role']}")
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Exception: {e}")

def main():
    """Run all tests"""
    print("🎮 AI NPC Dialogue Generator - Test Suite")
    print("=" * 60)
    
    # Test Phase 1
    test_phase1()
    
    # Test Phase 2
    test_phase2()
    
    # Test sample NPCs
    test_sample_npcs()
    
    print("\n✅ Testing complete!")
    print("\n💡 Tips:")
    print("  - Use Swagger UI: http://127.0.0.1:8000/docs (Phase 1)")
    print("  - Use Swagger UI: http://127.0.0.1:8001/docs (Phase 2)")
    print("  - Check README.md for more examples")

if __name__ == "__main__":
    main() 