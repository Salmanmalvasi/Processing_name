#!/usr/bin/env python3
"""
Character and Model Switcher for AI NPC Dialogue Generator
Allows switching between different characters and models
"""

import requests
import time
import json

class CharacterModelSwitcher:
    def __init__(self):
        self.available_models = {
            "1": {
                "name": "llama3-8b-8192",
                "description": "Fast, good for dialogue",
                "speed": "Very Fast",
                "quality": "Good"
            },
            "2": {
                "name": "llama3-70b-8192", 
                "description": "More powerful, better responses",
                "speed": "Fast",
                "quality": "Excellent"
            },
            "3": {
                "name": "mixtral-8x7b-32768",
                "description": "Balanced performance",
                "speed": "Fast",
                "quality": "Very Good"
            },
            "4": {
                "name": "gemma2-9b-it",
                "description": "Efficient and reliable",
                "speed": "Very Fast",
                "quality": "Good"
            }
        }
        
        self.available_characters = {
            "1": {
                "name": "Drogun",
                "type": "Gruff Blacksmith",
                "traits": "Gruff, impatient, values hard work, speaks in short sentences",
                "description": "A grumpy blacksmith who values hard work"
            },
            "2": {
                "name": "Lira",
                "type": "Enthusiastic Potion Seller",
                "traits": "Cheerful, talkative, always tries to upsell, uses lots of exclamations",
                "description": "A cheerful potion seller who loves to upsell"
            },
            "3": {
                "name": "Eldrin",
                "type": "Mysterious Forest Hermit",
                "traits": "Cryptic, wise, speaks in riddles, calm demeanor",
                "description": "A mysterious hermit who speaks in riddles"
            },
            "4": {
                "name": "Garrick",
                "type": "Cynical City Guard",
                "traits": "Suspicious, direct, doesn't trust easily, speaks with authority",
                "description": "A cynical city guard who's suspicious of everyone"
            },
            "5": {
                "name": "Elara",
                "type": "Cheerful Shopkeeper",
                "traits": "Friendly, helpful, loves to chat, always positive",
                "description": "A friendly shopkeeper who loves to chat"
            }
        }
        
        self.current_character = "1"  # Drogun
        self.current_model = "llama3-8b-8192"
        self.api_url = "http://127.0.0.1:8002"
    
    def show_characters(self):
        """Display available characters"""
        print("🎭 Available Characters:")
        print("=" * 50)
        for key, character in self.available_characters.items():
            print(f"{key}. {character['name']} - {character['type']}")
            print(f"   {character['description']}")
            if key == self.current_character:
                print(f"   Status: ✅ Currently Selected")
            print()
    
    def show_models(self):
        """Display available models"""
        print("🤖 Available Models:")
        print("=" * 50)
        for key, model in self.available_models.items():
            print(f"{key}. {model['name']}")
            print(f"   Description: {model['description']}")
            print(f"   Speed: {model['speed']}")
            print(f"   Quality: {model['quality']}")
            if model['name'] == self.current_model:
                print(f"   Status: ✅ Currently Active")
            print()
    
    def switch_character(self, character_choice: str):
        """Switch to a different character"""
        if character_choice not in self.available_characters:
            print("❌ Invalid character choice!")
            return False
        
        new_character = self.available_characters[character_choice]
        print(f"🔄 Switching to {new_character['name']} ({new_character['type']})...")
        
        # Test the new character
        test_response = self.test_character_model(character_choice, self.current_model)
        if test_response:
            self.current_character = character_choice
            print(f"✅ Successfully switched to {new_character['name']}")
            return True
        else:
            print(f"❌ Failed to switch to {new_character['name']}")
            return False
    
    def switch_model(self, model_choice: str):
        """Switch to a different model"""
        if model_choice not in self.available_models:
            print("❌ Invalid model choice!")
            return False
        
        new_model = self.available_models[model_choice]['name']
        print(f"🔄 Switching from {self.current_model} to {new_model}...")
        
        # Test the new model
        test_response = self.test_character_model(self.current_character, new_model)
        if test_response:
            self.current_model = new_model
            print(f"✅ Successfully switched to {new_model}")
            return True
        else:
            print(f"❌ Failed to switch to {new_model}")
            return False
    
    def test_character_model(self, character_choice: str, model_name: str) -> bool:
        """Test a specific character with a specific model"""
        try:
            character = self.available_characters[character_choice]
            payload = {
                "character_name": character["name"],
                "character_type": character["type"],
                "traits": character["traits"],
                "player_input": "Hello",
                "model": model_name
            }
            
            response = requests.post(f"{self.api_url}/generate", json=payload, timeout=30)
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ Error testing character/model: {e}")
            return False
    
    def chat_with_character_model(self):
        """Chat with the current character and model"""
        character = self.available_characters[self.current_character]
        print(f"🎭 Chatting with {character['name']} using {self.current_model}")
        print(f"💬 {character['description']}")
        print("Type 'quit' to exit, 'switch' to change character/model")
        print("-" * 50)
        
        while True:
            message = input("\n👤 You: ").strip()
            if message.lower() == 'quit':
                print("👋 Goodbye!")
                break
            elif message.lower() == 'switch':
                self.show_switch_menu()
                continue
            
            if not message:
                continue
            
            try:
                payload = {
                    "character_name": character["name"],
                    "character_type": character["type"],
                    "traits": character["traits"],
                    "player_input": message,
                    "model": self.current_model
                }
                
                start_time = time.time()
                response = requests.post(f"{self.api_url}/generate", json=payload, timeout=30)
                end_time = time.time()
                
                if response.status_code == 200:
                    result = response.json()
                    reply = result.get("reply", "No response")
                    print(f"\n{character['name']} ({self.current_model}): {reply}")
                    print(f"⏱️ Response time: {(end_time - start_time):.2f}s")
                else:
                    print(f"❌ Error: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def show_switch_menu(self):
        """Show menu for switching character or model"""
        print("\n🔄 Switch Menu:")
        print("1. 🎭 Switch character")
        print("2. 🤖 Switch model")
        print("3. 🔄 Switch both")
        print("0. ❌ Cancel")
        
        choice = input("\nSelect option (0-3): ").strip()
        
        if choice == "1":
            self.show_characters()
            char_choice = input("Select character (1-5): ").strip()
            self.switch_character(char_choice)
        elif choice == "2":
            self.show_models()
            model_choice = input("Select model (1-4): ").strip()
            self.switch_model(model_choice)
        elif choice == "3":
            self.show_characters()
            char_choice = input("Select character (1-5): ").strip()
            self.show_models()
            model_choice = input("Select model (1-4): ").strip()
            self.switch_character(char_choice)
            self.switch_model(model_choice)
        elif choice == "0":
            print("Cancelled.")
        else:
            print("❌ Invalid choice!")
    
    def compare_characters(self):
        """Compare different characters with the same model"""
        print("📊 Character Comparison Test")
        print("=" * 50)
        
        test_message = "Hello, how are you today?"
        results = {}
        
        for key, character in self.available_characters.items():
            print(f"\n🔄 Testing {character['name']}...")
            
            try:
                payload = {
                    "character_name": character["name"],
                    "character_type": character["type"],
                    "traits": character["traits"],
                    "player_input": test_message,
                    "model": self.current_model
                }
                
                start_time = time.time()
                response = requests.post(f"{self.api_url}/generate", json=payload, timeout=30)
                end_time = time.time()
                
                if response.status_code == 200:
                    result = response.json()
                    reply = result.get("reply", "No response")
                    response_time = end_time - start_time
                    
                    results[character['name']] = {
                        "response": reply,
                        "time": response_time,
                        "status": "✅ Working"
                    }
                    
                    print(f"✅ Response: {reply[:50]}...")
                    print(f"⏱️ Time: {response_time:.2f}s")
                else:
                    results[character['name']] = {
                        "response": "Error",
                        "time": 0,
                        "status": "❌ Failed"
                    }
                    print(f"❌ Failed: {response.status_code}")
                    
            except Exception as e:
                results[character['name']] = {
                    "response": "Error",
                    "time": 0,
                    "status": "❌ Error"
                }
                print(f"❌ Error: {e}")
        
        # Display comparison table
        print(f"\n📋 Character Comparison Results (Model: {self.current_model})")
        print("-" * 80)
        print(f"{'Character':<15} {'Type':<20} {'Status':<12} {'Time':<10} {'Response'}")
        print("-" * 80)
        
        for char_name, result in results.items():
            character = next(c for c in self.available_characters.values() if c['name'] == char_name)
            response_preview = result['response'][:30] + "..." if len(result['response']) > 30 else result['response']
            time_str = f"{result['time']:.2f}s" if result['time'] > 0 else "N/A"
            print(f"{char_name:<15} {character['type']:<20} {result['status']:<12} {time_str:<10} {response_preview}")
    
    def run(self):
        """Run the character and model switcher"""
        print("🎭 Character & Model Switcher for AI NPC Dialogue Generator")
        print("=" * 70)
        
        while True:
            character = self.available_characters[self.current_character]
            print(f"\n🎮 Current Setup:")
            print(f"   Character: {character['name']} ({character['type']})")
            print(f"   Model: {self.current_model}")
            print("=" * 40)
            print("1. 📊 Show available characters")
            print("2. 🤖 Show available models")
            print("3. 🎭 Switch character")
            print("4. 🤖 Switch model")
            print("5. 💬 Chat with current setup")
            print("6. ⚖️ Compare all characters")
            print("7. 🧪 Test character/model")
            print("0. ❌ Exit")
            print("-" * 40)
            
            choice = input("\n🎯 Enter your choice (0-7): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                self.show_characters()
            elif choice == "2":
                self.show_models()
            elif choice == "3":
                self.show_characters()
                char_choice = input("Select character (1-5): ").strip()
                self.switch_character(char_choice)
            elif choice == "4":
                self.show_models()
                model_choice = input("Select model (1-4): ").strip()
                self.switch_model(model_choice)
            elif choice == "5":
                self.chat_with_character_model()
            elif choice == "6":
                self.compare_characters()
            elif choice == "7":
                self.show_characters()
                char_choice = input("Select character to test (1-5): ").strip()
                self.show_models()
                model_choice = input("Select model to test (1-4): ").strip()
                if char_choice in self.available_characters and model_choice in self.available_models:
                    model_name = self.available_models[model_choice]['name']
                    if self.test_character_model(char_choice, model_name):
                        print(f"✅ {self.available_characters[char_choice]['name']} with {model_name} is working!")
                    else:
                        print(f"❌ {self.available_characters[char_choice]['name']} with {model_name} failed!")
                else:
                    print("❌ Invalid choice!")
            else:
                print("❌ Invalid choice! Please enter 0-7.")

if __name__ == "__main__":
    switcher = CharacterModelSwitcher()
    switcher.run() 