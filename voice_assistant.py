#!/usr/bin/env python3
"""
Voice Assistant for AI NPC Dialogue Generator
Integrates speech recognition and text-to-speech with the Groq API
"""

import speech_recognition as sr
import pyttsx3
import requests
import json
import time
import threading
from queue import Queue
import os
from typing import Optional, Dict, Any

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.engine = pyttsx3.init()
        self.api_url = "http://127.0.0.1:8002"
        
        # Configure text-to-speech
        self.setup_tts()
        
        # Configure speech recognition
        self.setup_speech_recognition()
        
        # Available characters
        self.characters = {
            "drogun": {
                "name": "Drogun",
                "type": "Gruff Blacksmith",
                "traits": "Gruff, impatient, values hard work, speaks in short sentences",
                "voice_rate": 150,
                "voice_pitch": 0.8
            },
            "lira": {
                "name": "Lira",
                "type": "Enthusiastic Potion Seller",
                "traits": "Cheerful, talkative, always tries to upsell, uses lots of exclamations",
                "voice_rate": 180,
                "voice_pitch": 1.2
            },
            "eldrin": {
                "name": "Eldrin",
                "type": "Mysterious Forest Hermit",
                "traits": "Cryptic, wise, speaks in riddles, calm demeanor",
                "voice_rate": 120,
                "voice_pitch": 0.9
            },
            "garrick": {
                "name": "Garrick",
                "type": "Cynical City Guard",
                "traits": "Suspicious, direct, doesn't trust easily, speaks with authority",
                "voice_rate": 140,
                "voice_pitch": 0.85
            },
            "elara": {
                "name": "Elara",
                "type": "Cheerful Shopkeeper",
                "traits": "Friendly, helpful, loves to chat, always positive",
                "voice_rate": 160,
                "voice_pitch": 1.1
            }
        }
        
        self.current_character = "drogun"
        self.current_model = "llama3-8b-8192"
        self.conversation_history = []
        self.is_listening = False
        self.audio_queue = Queue()
        
    def setup_tts(self):
        """Configure text-to-speech settings"""
        voices = self.engine.getProperty('voices')
        
        # Try to set a good default voice
        if voices:
            # Prefer a female voice for variety
            for voice in voices:
                if "female" in voice.name.lower() or "samantha" in voice.name.lower():
                    self.engine.setProperty('voice', voice.id)
                    break
            else:
                self.engine.setProperty('voice', voices[0].id)
        
        # Set default properties
        self.engine.setProperty('rate', 150)
        self.engine.setProperty('volume', 0.9)
        
    def setup_speech_recognition(self):
        """Configure speech recognition settings"""
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
        # Set recognition parameters
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        
    def speak(self, text: str, character: str = None):
        """Speak text with character-specific voice settings"""
        if character and character in self.characters:
            char = self.characters[character]
            self.engine.setProperty('rate', char['voice_rate'])
            self.engine.setProperty('volume', 0.9)
        
        print(f"🤖 {text}")
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self) -> Optional[str]:
        """Listen for speech input and return transcribed text"""
        try:
            with self.microphone as source:
                print("🎤 Listening... (speak now)")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                
            print("🔄 Processing speech...")
            text = self.recognizer.recognize_google(audio)
            print(f"👤 You said: {text}")
            return text.lower()
            
        except sr.WaitTimeoutError:
            print("⏰ No speech detected within timeout")
            return None
        except sr.UnknownValueError:
            print("❓ Could not understand speech")
            return None
        except sr.RequestError as e:
            print(f"❌ Speech recognition error: {e}")
            return None
        except Exception as e:
            print(f"❌ Error during speech recognition: {e}")
            return None
    
    def get_ai_response(self, message: str) -> Optional[str]:
        """Get AI response from the Groq API"""
        try:
            payload = {
                "character_name": self.characters[self.current_character]["name"],
                "character_type": self.characters[self.current_character]["type"],
                "traits": self.characters[self.current_character]["traits"],
                "player_input": message,
                "conversation_history": self.conversation_history,
                "model": self.current_model
            }
            
            response = requests.post(f"{self.api_url}/generate", json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("reply", "I didn't understand that.")
            else:
                print(f"❌ API Error: {response.status_code}")
                return "Sorry, I'm having trouble connecting to the AI."
                
        except requests.exceptions.Timeout:
            print("⏰ Request timed out")
            return "Sorry, the AI is taking too long to respond."
        except requests.exceptions.ConnectionError:
            print("❌ Connection error")
            return "Sorry, I can't connect to the AI service."
        except Exception as e:
            print(f"❌ Error: {e}")
            return "Sorry, something went wrong."
    
    def update_conversation_history(self, user_message: str, ai_response: str):
        """Update conversation history"""
        self.conversation_history.append({"speaker": "Player", "text": user_message})
        self.conversation_history.append({"speaker": self.characters[self.current_character]["name"], "text": ai_response})
        
        # Keep only last 10 exchanges
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]
    
    def show_characters(self):
        """Display available characters"""
        print("\n🎭 Available Characters:")
        print("=" * 40)
        for key, char in self.characters.items():
            status = " (current)" if key == self.current_character else ""
            print(f"{key}: {char['name']} - {char['type']}{status}")
    
    def change_character(self, character_key: str):
        """Change the current character"""
        if character_key in self.characters:
            self.current_character = character_key
            char = self.characters[character_key]
            print(f"✅ Switched to {char['name']} ({char['type']})")
            self.speak(f"Hello! I am {char['name']}, {char['type']}. How may I assist you?", character_key)
        else:
            print(f"❌ Character '{character_key}' not found")
    
    def show_models(self):
        """Display available models"""
        models = {
            "llama3-8b-8192": "Fast, good for dialogue",
            "llama3-70b-8192": "More powerful, better responses",
            "mixtral-8x7b-32768": "Balanced performance",
            "gemma2-9b-it": "Efficient and reliable"
        }
        
        print("\n🤖 Available Models:")
        print("=" * 30)
        for model, desc in models.items():
            status = " (current)" if model == self.current_model else ""
            print(f"{model}: {desc}{status}")
    
    def change_model(self, model: str):
        """Change the current AI model"""
        valid_models = ["llama3-8b-8192", "llama3-70b-8192", "mixtral-8x7b-32768", "gemma2-9b-it"]
        if model in valid_models:
            self.current_model = model
            print(f"✅ Switched to model: {model}")
            self.speak(f"Model changed to {model}")
        else:
            print(f"❌ Model '{model}' not found")
    
    def voice_conversation(self):
        """Main voice conversation loop"""
        print("\n🎤 Starting Voice Conversation Mode")
        print("=" * 50)
        print("Commands:")
        print("- Say 'quit' or 'exit' to stop")
        print("- Say 'change character' to switch characters")
        print("- Say 'change model' to switch AI models")
        print("- Say 'status' to check API status")
        print("=" * 50)
        
        # Initial greeting
        char = self.characters[self.current_character]
        self.speak(f"Hello! I am {char['name']}, {char['type']}. How may I assist you?", self.current_character)
        
        while True:
            # Listen for user input
            user_input = self.listen()
            
            if not user_input:
                continue
            
            # Check for commands
            if user_input in ["quit", "exit", "stop", "bye"]:
                self.speak("Goodbye! It was nice talking with you.", self.current_character)
                break
            elif "change character" in user_input:
                self.handle_character_change()
                continue
            elif "change model" in user_input:
                self.handle_model_change()
                continue
            elif "status" in user_input:
                self.check_api_status()
                continue
            elif "help" in user_input:
                self.show_help()
                continue
            
            # Get AI response
            print("🤔 Thinking...")
            ai_response = self.get_ai_response(user_input)
            
            if ai_response:
                # Update conversation history
                self.update_conversation_history(user_input, ai_response)
                
                # Speak the response
                self.speak(ai_response, self.current_character)
            else:
                self.speak("I'm sorry, I didn't get a response. Please try again.")
    
    def handle_character_change(self):
        """Handle character change via voice"""
        self.speak("Which character would you like to switch to? Say the character name.")
        
        # Listen for character name
        character_input = self.listen()
        if character_input:
            # Find matching character
            for key, char in self.characters.items():
                if char['name'].lower() in character_input or key in character_input:
                    self.change_character(key)
                    return
            
            self.speak("I didn't recognize that character. Please try again.")
    
    def handle_model_change(self):
        """Handle model change via voice"""
        self.speak("Which model would you like to use? Say 'fast', 'powerful', 'balanced', or 'efficient'.")
        
        # Listen for model preference
        model_input = self.listen()
        if model_input:
            model_mapping = {
                "fast": "llama3-8b-8192",
                "powerful": "llama3-70b-8192", 
                "balanced": "mixtral-8x7b-32768",
                "efficient": "gemma2-9b-it"
            }
            
            for key, model in model_mapping.items():
                if key in model_input:
                    self.change_model(model)
                    return
            
            self.speak("I didn't recognize that model. Please try again.")
    
    def check_api_status(self):
        """Check API status"""
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                self.speak("The AI service is online and ready.")
            else:
                self.speak("The AI service is having issues.")
        except:
            self.speak("Cannot connect to the AI service.")
    
    def show_help(self):
        """Show help information"""
        help_text = """
        Voice Assistant Commands:
        - Say 'quit' or 'exit' to stop
        - Say 'change character' to switch characters
        - Say 'change model' to switch AI models
        - Say 'status' to check API status
        - Say 'help' for this message
        """
        print(help_text)
        self.speak("I've shown the help information on screen.")
    
    def interactive_menu(self):
        """Interactive menu for voice assistant setup"""
        while True:
            print("\n🎤 Voice Assistant Menu")
            print("=" * 30)
            print("1. 🎭 Show characters")
            print("2. 🤖 Show models")
            print("3. 🎤 Start voice conversation")
            print("4. ⚙️  Change character")
            print("5. 🔧 Change model")
            print("6. 📊 Check API status")
            print("7. 🧪 Test voice")
            print("0. ❌ Exit")
            print("-" * 30)
            
            choice = input("Select option: ").strip()
            
            if choice == "1":
                self.show_characters()
            elif choice == "2":
                self.show_models()
            elif choice == "3":
                self.voice_conversation()
            elif choice == "4":
                self.show_characters()
                char_key = input("Enter character key: ").strip()
                self.change_character(char_key)
            elif choice == "5":
                self.show_models()
                model = input("Enter model name: ").strip()
                self.change_model(model)
            elif choice == "6":
                self.check_api_status()
            elif choice == "7":
                self.test_voice()
            elif choice == "0":
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please try again.")
    
    def test_voice(self):
        """Test voice recognition and synthesis"""
        print("\n🧪 Voice Test Mode")
        print("=" * 20)
        
        # Test speech recognition
        print("🎤 Testing speech recognition...")
        print("Say something when prompted...")
        
        test_input = self.listen()
        if test_input:
            print(f"✅ Speech recognition works! You said: {test_input}")
            
            # Test text-to-speech
            print("🔊 Testing text-to-speech...")
            self.speak("This is a test of the voice synthesis system. If you can hear this clearly, the voice assistant is working properly.")
        else:
            print("❌ Speech recognition test failed")
    
    def run(self):
        """Main entry point"""
        print("🎤 AI NPC Voice Assistant")
        print("=" * 40)
        print("Make sure the Groq API server is running on port 8002")
        print("Current character:", self.characters[self.current_character]["name"])
        print("Current model:", self.current_model)
        print("=" * 40)
        
        # Check if API is available
        try:
            response = requests.get(f"{self.api_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ API server is online")
            else:
                print("❌ API server is not responding")
                return
        except:
            print("❌ Cannot connect to API server")
            print("Please start the server with: python3 main_groq.py")
            return
        
        # Start interactive menu
        self.interactive_menu()

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run() 