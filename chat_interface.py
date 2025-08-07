#!/usr/bin/env python3
"""
Interactive Chat Interface for AI NPC Dialogue Generator
Allows real-time conversations with NPCs via terminal
"""

import requests
import json
import time
import sys
import os
from typing import Dict, List, Optional

# API URLs
PHASE1_URL = "http://127.0.0.1:8000/generate"
PHASE2_URL = "http://127.0.0.1:8001/generate"
PHASE2_SAMPLES_URL = "http://127.0.0.1:8001/sample-npcs"

# Pre-defined NPCs for quick selection
PREDEFINED_NPCS = {
    "1": {
        "name": "Drogun",
        "type": "Gruff Blacksmith",
        "traits": "Gruff, impatient, values hard work, speaks in short sentences",
        "description": "A grumpy blacksmith who values hard work and speaks in short sentences"
    },
    "2": {
        "name": "Lira",
        "type": "Enthusiastic Potion Seller",
        "traits": "Cheerful, talkative, always tries to upsell, uses lots of exclamations",
        "description": "A cheerful potion seller who loves to upsell and uses lots of exclamations"
    },
    "3": {
        "name": "Eldrin",
        "type": "Mysterious Forest Hermit",
        "traits": "Cryptic, wise, speaks in riddles, calm demeanor",
        "description": "A mysterious hermit who speaks in riddles and cryptic wisdom"
    },
    "4": {
        "name": "Garrick",
        "type": "Cynical City Guard",
        "traits": "Suspicious, direct, doesn't trust easily, speaks with authority",
        "description": "A cynical city guard who's suspicious of everyone and speaks with authority"
    },
    "5": {
        "name": "Elara",
        "type": "Cheerful Shopkeeper",
        "traits": "Friendly, helpful, loves to chat, always positive",
        "description": "A friendly shopkeeper who loves to chat and is always positive"
    }
}

def print_banner():
    """Print the application banner"""
    print("🎮" + "="*60 + "🎮")
    print("           AI NPC DIALOGUE GENERATOR - CHAT INTERFACE")
    print("🎮" + "="*60 + "🎮")
    print()

def print_npc_list():
    """Print available NPCs"""
    print("📋 Available NPCs:")
    print("-" * 50)
    for key, npc in PREDEFINED_NPCS.items():
        print(f"{key}. {npc['name']} - {npc['type']}")
        print(f"   {npc['description']}")
        print()
    print("0. Custom NPC")
    print("q. Quit")
    print("-" * 50)

def get_npc_choice() -> Optional[Dict]:
    """Get user's NPC choice"""
    while True:
        choice = input("Select an NPC (1-5, 0 for custom, q to quit): ").strip().lower()
        
        if choice == 'q':
            return None
        elif choice == '0':
            return get_custom_npc()
        elif choice in PREDEFINED_NPCS:
            return PREDEFINED_NPCS[choice]
        else:
            print("❌ Invalid choice. Please try again.")

def get_custom_npc() -> Dict:
    """Get custom NPC details from user"""
    print("\n🎭 Create Custom NPC")
    print("-" * 30)
    
    name = input("NPC Name: ").strip()
    npc_type = input("NPC Type (e.g., 'Wizard', 'Merchant'): ").strip()
    traits = input("NPC Traits (e.g., 'Wise, mysterious, speaks in riddles'): ").strip()
    
    return {
        "name": name,
        "type": npc_type,
        "traits": traits,
        "description": f"Custom NPC: {name} - {npc_type}"
    }

def send_message_phase1(npc: Dict, message: str) -> Optional[str]:
    """Send message to Phase 1 API"""
    try:
        payload = {
            "name": npc["name"],
            "type": npc["type"],
            "traits": npc["traits"],
            "message": message
        }
        
        response = requests.post(PHASE1_URL, json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            return result.get("reply", "No response")
        else:
            return f"❌ Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ Connection error: {e}"

def send_message_phase2(npc: Dict, message: str, conversation_history: List[Dict]) -> Optional[str]:
    """Send message to Phase 2 API"""
    try:
        payload = {
            "character_name": npc["name"],
            "character_type": npc["type"],
            "traits": npc["traits"],
            "player_input": message,
            "conversation_history": conversation_history
        }
        
        response = requests.post(PHASE2_URL, json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            return result.get("reply", "No response")
        else:
            return f"❌ Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ Connection error: {e}"

def chat_session(npc: Dict, use_phase2: bool = True):
    """Start a chat session with the selected NPC"""
    print(f"\n🎭 Starting chat with {npc['name']} ({npc['type']})")
    print(f"💬 {npc['description']}")
    print("💡 Type 'quit' to end the conversation")
    print("💡 Type 'clear' to clear conversation history")
    print("-" * 60)
    
    conversation_history = []
    
    while True:
        try:
            # Get user input
            user_input = input(f"\n👤 You: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'clear':
                conversation_history = []
                print("🗑️  Conversation history cleared!")
                continue
            elif not user_input:
                continue
            
            # Send message and get response
            if use_phase2:
                response = send_message_phase2(npc, user_input, conversation_history)
            else:
                response = send_message_phase1(npc, user_input)
            
            if response:
                print(f"\n{npc['name']}: {response}")
                
                # Update conversation history for Phase 2
                if use_phase2:
                    conversation_history.append({"speaker": "Player", "text": user_input})
                    conversation_history.append({"speaker": npc["name"], "text": response})
                    
                    # Keep only last 10 exchanges to avoid token limits
                    if len(conversation_history) > 20:
                        conversation_history = conversation_history[-20:]
            else:
                print("❌ No response received")
                
        except KeyboardInterrupt:
            print("\n👋 Chat interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

def check_api_status():
    """Check if APIs are running"""
    try:
        # Check Phase 1
        response = requests.get("http://127.0.0.1:8000/docs", timeout=2)
        phase1_status = response.status_code == 200
    except:
        phase1_status = False
    
    try:
        # Check Phase 2
        response = requests.get("http://127.0.0.1:8001/health", timeout=2)
        phase2_status = response.status_code == 200
    except:
        phase2_status = False
    
    return phase1_status, phase2_status

def main():
    """Main application loop"""
    print_banner()
    
    # Check API status
    phase1_status, phase2_status = check_api_status()
    
    if not phase1_status and not phase2_status:
        print("❌ Error: No APIs are running!")
        print("Please start the servers:")
        print("  Phase 1: python3 -m uvicorn main:app --reload --port 8000")
        print("  Phase 2: python3 -m uvicorn main_v2:app --reload --port 8001")
        return
    
    print("🔌 API Status:")
    print(f"  Phase 1 (Basic): {'✅ Running' if phase1_status else '❌ Not running'}")
    print(f"  Phase 2 (Advanced): {'✅ Running' if phase2_status else '❌ Not running'}")
    print()
    
    # Choose API version
    if phase1_status and phase2_status:
        while True:
            choice = input("Choose API version (1 for Basic, 2 for Advanced): ").strip()
            if choice == "1":
                use_phase2 = False
                break
            elif choice == "2":
                use_phase2 = True
                break
            else:
                print("❌ Invalid choice. Please enter 1 or 2.")
    elif phase2_status:
        use_phase2 = True
        print("✅ Using Phase 2 (Advanced) API")
    else:
        use_phase2 = False
        print("✅ Using Phase 1 (Basic) API")
    
    print()
    
    while True:
        print_npc_list()
        npc = get_npc_choice()
        
        if npc is None:
            print("👋 Goodbye!")
            break
        
        chat_session(npc, use_phase2)
        
        # Ask if user wants to chat with another NPC
        again = input("\n🤔 Chat with another NPC? (y/n): ").strip().lower()
        if again != 'y':
            print("👋 Goodbye!")
            break

if __name__ == "__main__":
    main() 