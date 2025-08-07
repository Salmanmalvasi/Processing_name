#!/usr/bin/env python3
import requests
import json

def chat_with_npc():
    print("🎮 AI NPC Chat Interface")
    print("=" * 40)
    
    # NPC selection
    npcs = {
        "1": {"name": "Drogun", "type": "Gruff Blacksmith", "traits": "Gruff, impatient, values hard work, speaks in short sentences"},
        "2": {"name": "Lira", "type": "Enthusiastic Potion Seller", "traits": "Cheerful, talkative, always tries to upsell, uses lots of exclamations"},
        "3": {"name": "Eldrin", "type": "Mysterious Forest Hermit", "traits": "Cryptic, wise, speaks in riddles, calm demeanor"}
    }
    
    print("Choose an NPC:")
    for key, npc in npcs.items():
        print(f"{key}. {npc['name']} - {npc['type']}")
    
    choice = input("\nSelect NPC (1-3): ").strip()
    if choice not in npcs:
        print("Invalid choice!")
        return
    
    npc = npcs[choice]
    print(f"\n🎭 Chatting with {npc['name']} ({npc['type']})")
    print("Type 'quit' to exit")
    print("-" * 40)
    
    conversation_history = []
    
    while True:
        message = input("\n👤 You: ").strip()
        if message.lower() == 'quit':
            break
        
        # Send to Phase 2 API
        payload = {
            "character_name": npc["name"],
            "character_type": npc["type"],
            "traits": npc["traits"],
            "player_input": message,
            "conversation_history": conversation_history
        }
        
        try:
            response = requests.post("http://127.0.0.1:8001/generate", json=payload)
            if response.status_code == 200:
                result = response.json()
                reply = result.get("reply", "No response")
                print(f"\n{npc['name']}: {reply}")
                
                # Update conversation history
                conversation_history.append({"speaker": "Player", "text": message})
                conversation_history.append({"speaker": npc["name"], "text": reply})
                
                # Keep only last 10 exchanges
                if len(conversation_history) > 20:
                    conversation_history = conversation_history[-20:]
            else:
                print(f"❌ Error: {response.status_code}")
        except Exception as e:
            print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    chat_with_npc() 