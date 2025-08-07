#!/usr/bin/env python3
"""
Interactive Model Manager for AI NPC Dialogue Generator
Allows users to check, test, and manage the Groq AI model
"""

import requests
import json
import time
import sys
from typing import Dict, List, Optional

class ModelManager:
    def __init__(self):
        self.apis = {
            "groq": {
                "url": "http://127.0.0.1:8002",
                "name": "Groq API",
                "model": "llama3-8b-8192",
                "provider": "Groq"
            }
        }
        
    def print_banner(self):
        """Print the application banner"""
        print("🔧" + "="*60 + "🔧")
        print("           AI NPC DIALOGUE GENERATOR - MODEL MANAGER")
        print("🔧" + "="*60 + "🔧")
        print()
    
    def check_api_status(self, api_key: str) -> Dict:
        """Check if an API is running and get its status"""
        try:
            response = requests.get(f"{self.apis[api_key]['url']}/health", timeout=5)
            if response.status_code == 200:
                return {"status": "running", "data": response.json()}
            else:
                return {"status": "error", "data": f"HTTP {response.status_code}"}
        except requests.exceptions.ConnectionError:
            return {"status": "not_running", "data": "Connection refused"}
        except Exception as e:
            return {"status": "error", "data": str(e)}
    
    def get_all_api_status(self) -> Dict:
        """Check status of all APIs"""
        status = {}
        for api_key, api_info in self.apis.items():
            status[api_key] = self.check_api_status(api_key)
        return status
    
    def test_model(self, api_key: str, test_message: str = "Hello, what model are you using?") -> Optional[str]:
        """Test a specific model with a message"""
        try:
            payload = {
                "character_name": "Drogun",
                "character_type": "Gruff Blacksmith",
                "traits": "Gruff, impatient, values hard work",
                "player_input": test_message
            }
            
            response = requests.post(
                f"{self.apis[api_key]['url']}/generate", 
                json=payload, 
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("reply", "No response")
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error: {e}"
    
    def show_model_info(self, api_key: str):
        """Show detailed information about a specific model"""
        api_info = self.apis[api_key]
        status = self.check_api_status(api_key)
        
        print(f"\n📊 Model Information: {api_info['name']}")
        print("=" * 50)
        print(f"Provider: {api_info['provider']}")
        print(f"Model: {api_info['model']}")
        print(f"URL: {api_info['url']}")
        
        if status["status"] == "running":
            data = status["data"]
            print(f"Status: ✅ {data['status']}")
            if "rate_limit" in data:
                rate_limit = data["rate_limit"]
                print(f"Rate Limit: {rate_limit['requests_this_minute']}/{rate_limit['max_requests_per_minute']}")
                print(f"Remaining: {rate_limit['remaining_requests']}")
        elif status["status"] == "not_running":
            print("Status: ❌ Not running")
        else:
            print(f"Status: ⚠️ {status['data']}")
        
        print()
    
    def test_model_interactive(self, api_key: str):
        """Interactive model testing"""
        api_info = self.apis[api_key]
        status = self.check_api_status(api_key)
        
        if status["status"] != "running":
            print(f"❌ {api_info['name']} is not running!")
            return
        
        print(f"\n🧪 Testing {api_info['name']} ({api_info['model']})")
        print("=" * 50)
        
        while True:
            test_message = input("\n💬 Enter test message (or 'quit' to exit): ").strip()
            if test_message.lower() == 'quit':
                break
            
            if not test_message:
                continue
            
            print("🔄 Testing...")
            start_time = time.time()
            response = self.test_model(api_key, test_message)
            end_time = time.time()
            
            print(f"⏱️ Response time: {(end_time - start_time):.2f} seconds")
            print(f"🤖 Response: {response}")
    
    def show_menu(self):
        """Show the main menu"""
        print("\n🎮 Model Manager Menu")
        print("=" * 30)
        print("1. 📊 Check model status")
        print("2. 🔍 Show model information")
        print("3. 🧪 Test model interactively")
        print("4. 🚀 Quick test")
        print("5. 📈 Performance test")
        print("6. 🔄 Refresh status")
        print("0. ❌ Exit")
        print("-" * 30)
    
    def performance_test(self, api_key: str = "groq"):
        """Run a performance test on the specified model"""
        api_info = self.apis[api_key]
        status = self.check_api_status(api_key)
        
        if status["status"] != "running":
            print(f"❌ {api_info['name']} is not running!")
            return
        
        print(f"\n⚡ Performance Test: {api_info['name']}")
        print("=" * 50)
        
        test_messages = [
            "Hello",
            "What can you do?",
            "Tell me a story",
            "How are you today?",
            "What's the weather like?"
        ]
        
        times = []
        responses = []
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n🔄 Test {i}/5: '{message}'")
            start_time = time.time()
            response = self.test_model(api_key, message)
            end_time = time.time()
            
            response_time = end_time - start_time
            times.append(response_time)
            responses.append(response)
            
            print(f"⏱️ Time: {response_time:.2f}s")
            print(f"🤖 Response: {response[:100]}...")
        
        # Calculate statistics
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"\n📈 Performance Summary:")
        print(f"Average Response Time: {avg_time:.2f}s")
        print(f"Fastest Response: {min_time:.2f}s")
        print(f"Slowest Response: {max_time:.2f}s")
        print(f"Total Test Time: {sum(times):.2f}s")
    
    def run(self):
        """Run the interactive model manager"""
        self.print_banner()
        
        while True:
            self.show_menu()
            
            try:
                choice = input("\n🎯 Enter your choice (0-6): ").strip()
                
                if choice == "0":
                    print("👋 Goodbye!")
                    break
                
                elif choice == "1":
                    print("\n📊 Checking model status...")
                    status = self.get_all_api_status()
                    
                    for api_key, api_status in status.items():
                        api_info = self.apis[api_key]
                        if api_status["status"] == "running":
                            print(f"✅ {api_info['name']}: Running")
                        else:
                            print(f"❌ {api_info['name']}: {api_status['data']}")
                
                elif choice == "2":
                    self.show_model_info("groq")
                
                elif choice == "3":
                    self.test_model_interactive("groq")
                
                elif choice == "4":
                    print("\n🚀 Quick test with Groq...")
                    response = self.test_model("groq", "Hello, what model are you using?")
                    print(f"🤖 Response: {response}")
                
                elif choice == "5":
                    print("\n📈 Performance testing...")
                    self.performance_test()
                
                elif choice == "6":
                    print("\n🔄 Refreshing status...")
                    # This will be handled in the next loop iteration
                
                else:
                    print("❌ Invalid choice! Please enter 0-6.")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    manager = ModelManager()
    manager.run() 