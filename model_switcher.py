#!/usr/bin/env python3
"""
Model Switcher for AI NPC Dialogue Generator
Allows easy switching between different Groq models
"""

import requests
import time
import json

class ModelSwitcher:
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
        
        self.current_model = "llama3-8b-8192"
        self.api_url = "http://127.0.0.1:8002"
    
    def show_models(self):
        """Display available models"""
        print("🤖 Available Groq Models:")
        print("=" * 50)
        for key, model in self.available_models.items():
            print(f"{key}. {model['name']}")
            print(f"   Description: {model['description']}")
            print(f"   Speed: {model['speed']}")
            print(f"   Quality: {model['quality']}")
            if model['name'] == self.current_model:
                print(f"   Status: ✅ Currently Active")
            print()
    
    def switch_model(self, model_choice: str):
        """Switch to a different model"""
        if model_choice not in self.available_models:
            print("❌ Invalid model choice!")
            return False
        
        new_model = self.available_models[model_choice]['name']
        print(f"🔄 Switching from {self.current_model} to {new_model}...")
        
        # Test the new model
        test_response = self.test_model(new_model)
        if test_response:
            self.current_model = new_model
            print(f"✅ Successfully switched to {new_model}")
            return True
        else:
            print(f"❌ Failed to switch to {new_model}")
            return False
    
    def test_model(self, model_name: str) -> bool:
        """Test a specific model"""
        try:
            payload = {
                "character_name": "Drogun",
                "character_type": "Gruff Blacksmith",
                "traits": "Gruff, impatient, values hard work",
                "player_input": "Hello",
                "model": model_name  # Add model parameter
            }
            
            response = requests.post(f"{self.api_url}/generate", json=payload, timeout=30)
            return response.status_code == 200
            
        except Exception as e:
            print(f"❌ Error testing model: {e}")
            return False
    
    def chat_with_model(self, model_name: str):
        """Chat with a specific model"""
        print(f"🎭 Chatting with Drogun using {model_name}")
        print("Type 'quit' to exit, 'switch' to change models")
        print("-" * 50)
        
        while True:
            message = input("\n👤 You: ").strip()
            if message.lower() == 'quit':
                print("👋 Goodbye!")
                break
            elif message.lower() == 'switch':
                self.show_models()
                choice = input("Select new model (1-4): ").strip()
                if self.switch_model(choice):
                    model_name = self.current_model
                continue
            
            if not message:
                continue
            
            try:
                payload = {
                    "character_name": "Drogun",
                    "character_type": "Gruff Blacksmith",
                    "traits": "Gruff, impatient, values hard work",
                    "player_input": message,
                    "model": model_name
                }
                
                start_time = time.time()
                response = requests.post(f"{self.api_url}/generate", json=payload, timeout=30)
                end_time = time.time()
                
                if response.status_code == 200:
                    result = response.json()
                    reply = result.get("reply", "No response")
                    print(f"\n🗡️ Drogun ({model_name}): {reply}")
                    print(f"⏱️ Response time: {(end_time - start_time):.2f}s")
                else:
                    print(f"❌ Error: {response.status_code}")
                    
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def compare_models(self):
        """Compare different models with the same input"""
        print("📊 Model Comparison Test")
        print("=" * 50)
        
        test_message = "Can you repair my sword?"
        results = {}
        
        for key, model_info in self.available_models.items():
            model_name = model_info['name']
            print(f"\n🔄 Testing {model_name}...")
            
            try:
                payload = {
                    "character_name": "Drogun",
                    "character_type": "Gruff Blacksmith",
                    "traits": "Gruff, impatient, values hard work",
                    "player_input": test_message,
                    "model": model_name
                }
                
                start_time = time.time()
                response = requests.post(f"{self.api_url}/generate", json=payload, timeout=30)
                end_time = time.time()
                
                if response.status_code == 200:
                    result = response.json()
                    reply = result.get("reply", "No response")
                    response_time = end_time - start_time
                    
                    results[model_name] = {
                        "response": reply,
                        "time": response_time,
                        "status": "✅ Working"
                    }
                    
                    print(f"✅ Response: {reply[:50]}...")
                    print(f"⏱️ Time: {response_time:.2f}s")
                else:
                    results[model_name] = {
                        "response": "Error",
                        "time": 0,
                        "status": "❌ Failed"
                    }
                    print(f"❌ Failed: {response.status_code}")
                    
            except Exception as e:
                results[model_name] = {
                    "response": "Error",
                    "time": 0,
                    "status": "❌ Error"
                }
                print(f"❌ Error: {e}")
        
        # Display comparison table
        print(f"\n📋 Comparison Results for: '{test_message}'")
        print("-" * 80)
        print(f"{'Model':<20} {'Status':<12} {'Time':<10} {'Response'}")
        print("-" * 80)
        
        for model_name, result in results.items():
            response_preview = result['response'][:30] + "..." if len(result['response']) > 30 else result['response']
            time_str = f"{result['time']:.2f}s" if result['time'] > 0 else "N/A"
            print(f"{model_name:<20} {result['status']:<12} {time_str:<10} {response_preview}")
    
    def run(self):
        """Run the model switcher"""
        print("🤖 Model Switcher for AI NPC Dialogue Generator")
        print("=" * 60)
        
        while True:
            print(f"\n🎮 Current Model: {self.current_model}")
            print("=" * 30)
            print("1. 📊 Show available models")
            print("2. 🔄 Switch model")
            print("3. 💬 Chat with current model")
            print("4. ⚖️ Compare all models")
            print("5. 🧪 Test specific model")
            print("0. ❌ Exit")
            print("-" * 30)
            
            choice = input("\n🎯 Enter your choice (0-5): ").strip()
            
            if choice == "0":
                print("👋 Goodbye!")
                break
            elif choice == "1":
                self.show_models()
            elif choice == "2":
                self.show_models()
                model_choice = input("Select model to switch to (1-4): ").strip()
                self.switch_model(model_choice)
            elif choice == "3":
                self.chat_with_model(self.current_model)
            elif choice == "4":
                self.compare_models()
            elif choice == "5":
                self.show_models()
                test_choice = input("Select model to test (1-4): ").strip()
                if test_choice in self.available_models:
                    model_name = self.available_models[test_choice]['name']
                    if self.test_model(model_name):
                        print(f"✅ {model_name} is working!")
                    else:
                        print(f"❌ {model_name} failed!")
                else:
                    print("❌ Invalid choice!")
            else:
                print("❌ Invalid choice! Please enter 0-5.")

if __name__ == "__main__":
    switcher = ModelSwitcher()
    switcher.run() 