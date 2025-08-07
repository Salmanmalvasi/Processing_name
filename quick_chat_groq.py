#!/usr/bin/env python3
import requests

def quick_chat_groq():
    print("🎮 Quick NPC Chat (Groq Version)")
    print("=" * 40)
    print("Chatting with Drogun (Gruff Blacksmith)")
    print("Type 'quit' to exit")
    print("-" * 40)
    
    npc = {
        "name": "Drogun",
        "type": "Gruff Blacksmith", 
        "traits": "Gruff, impatient, values hard work, speaks in short sentences"
    }
    
    conversation_history = []
    
    while True:
        message = input("\n👤 You: ").strip()
        if message.lower() == 'quit':
            print("👋 Goodbye!")
            break
        
        # Skip empty messages
        if not message:
            continue
        
        # Basic input validation
        if len(message) > 500:
            print("❌ Message too long. Please keep it under 500 characters.")
            continue
        
        payload = {
            "character_name": npc["name"],
            "character_type": npc["type"],
            "traits": npc["traits"],
            "player_input": message,
            "conversation_history": conversation_history
        }
        
        try:
            response = requests.post("http://127.0.0.1:8002/generate", json=payload, timeout=30)
            if response.status_code == 200:
                result = response.json()
                reply = result.get("reply", "No response")
                print(f"\n{npc['name']}: {reply}")
                
                # Update conversation history
                conversation_history.append({"speaker": "Player", "text": message})
                conversation_history.append({"speaker": npc["name"], "text": reply})
                
                if len(conversation_history) > 20:
                    conversation_history = conversation_history[-20:]
            elif response.status_code == 422:
                print("❌ Invalid input. Please try a different message.")
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
        except requests.exceptions.Timeout:
            print("❌ Request timed out. Please try again.")
        except requests.exceptions.ConnectionError:
            print("❌ Connection error. Make sure the Groq server is running.")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    quick_chat_groq() 