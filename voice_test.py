#!/usr/bin/env python3
"""
Voice Test Script for AI NPC Dialogue Generator
Test different voice engines and voice selection
"""
import speech_recognition as sr
import pyttsx3
import time

def test_voice_engines():
    """Test different voice engines available on the system"""
    print("🎤 Voice Engine Test")
    print("=" * 50)
    
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        print(f"Found {len(voices)} available voices:")
        print("-" * 50)
        
        for i, voice in enumerate(voices):
            print(f"{i+1}. {voice.name}")
            print(f"   Language: {voice.languages[0] if voice.languages else 'Unknown'}")
            print(f"   Gender: {voice.gender if hasattr(voice, 'gender') else 'Unknown'}")
            print(f"   Age: {voice.age if hasattr(voice, 'age') else 'Unknown'}")
            print()
        
        # Test different voice types
        test_text = "Hello! This is a test of the voice synthesis system."
        
        print("Testing different voice types:")
        print("-" * 30)
        
        # Test male voices
        male_voices = [v for v in voices if 'male' in v.name.lower() or 'david' in v.name.lower() or 'guy' in v.name.lower()]
        if male_voices:
            print(f"Testing male voice: {male_voices[0].name}")
            engine.setProperty('voice', male_voices[0].id)
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.9)
            engine.say("This is a deep male voice test.")
            engine.runAndWait()
            time.sleep(1)
        
        # Test female voices
        female_voices = [v for v in voices if 'female' in v.name.lower() or 'jenny' in v.name.lower() or 'aria' in v.name.lower()]
        if female_voices:
            print(f"Testing female voice: {female_voices[0].name}")
            engine.setProperty('voice', female_voices[0].id)
            engine.setProperty('rate', 170)
            engine.setProperty('volume', 0.9)
            engine.say("This is a cheerful female voice test.")
            engine.runAndWait()
            time.sleep(1)
        
        # Test different rates
        print("Testing different speech rates:")
        print("-" * 30)
        
        rates = [100, 150, 200]
        for rate in rates:
            print(f"Testing rate: {rate} WPM")
            engine.setProperty('rate', rate)
            engine.say(f"This is a test at {rate} words per minute.")
            engine.runAndWait()
            time.sleep(0.5)
        
        # Test different pitches
        print("Testing different voice pitches:")
        print("-" * 30)
        
        # Note: pyttsx3 doesn't directly support pitch, but we can simulate with rate
        print("Testing deep voice (slow rate)")
        engine.setProperty('rate', 100)
        engine.say("This is a deep voice test.")
        engine.runAndWait()
        time.sleep(0.5)
        
        print("Testing high voice (fast rate)")
        engine.setProperty('rate', 200)
        engine.say("This is a high voice test.")
        engine.runAndWait()
        time.sleep(0.5)
        
        print("✅ Voice engine test completed!")
        
    except Exception as e:
        print(f"❌ Error testing voice engines: {e}")

def test_character_voices():
    """Test character-specific voice settings"""
    print("\n🎭 Character Voice Test")
    print("=" * 50)
    
    characters = {
        "Drogun": {
            "description": "Deep, grumpy blacksmith",
            "rate": 110,
            "pitch": "deep",
            "style": "grumpy"
        },
        "Lira": {
            "description": "Cheerful potion seller", 
            "rate": 190,
            "pitch": "high",
            "style": "excited"
        },
        "Eldrin": {
            "description": "Mysterious forest hermit",
            "rate": 85,
            "pitch": "low",
            "style": "whisper"
        },
        "Garrick": {
            "description": "Authoritative city guard",
            "rate": 130,
            "pitch": "deep",
            "style": "stern"
        },
        "Elara": {
            "description": "Warm shopkeeper",
            "rate": 170,
            "pitch": "medium-high",
            "style": "friendly"
        }
    }
    
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        # Get male and female voices
        male_voices = [v for v in voices if 'male' in v.name.lower() or 'david' in v.name.lower()]
        female_voices = [v for v in voices if 'female' in v.name.lower() or 'jenny' in v.name.lower()]
        
        for char_name, char_data in characters.items():
            print(f"\n🎭 Testing {char_name} ({char_data['description']}):")
            print(f"   Rate: {char_data['rate']} WPM")
            print(f"   Pitch: {char_data['pitch']}")
            print(f"   Style: {char_data['style']}")
            
            # Set voice based on character
            if char_name in ["Lira", "Elara"]:
                if female_voices:
                    engine.setProperty('voice', female_voices[0].id)
                    print(f"   Using voice: {female_voices[0].name}")
            else:
                if male_voices:
                    engine.setProperty('voice', male_voices[0].id)
                    print(f"   Using voice: {male_voices[0].name}")
            
            # Set rate
            engine.setProperty('rate', char_data['rate'])
            engine.setProperty('volume', 0.9)
            
            # Test message
            test_message = f"Hello! I am {char_name}. This is my unique voice."
            print(f"   Speaking: '{test_message}'")
            
            engine.say(test_message)
            engine.runAndWait()
            time.sleep(1)
        
        print("\n✅ Character voice test completed!")
        
    except Exception as e:
        print(f"❌ Error testing character voices: {e}")

def test_voice_selection():
    """Test voice selection and switching"""
    print("\n🔄 Voice Selection Test")
    print("=" * 50)
    
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        print("Available voices:")
        for i, voice in enumerate(voices):
            print(f"  {i+1}. {voice.name}")
        
        print("\nTesting voice switching:")
        print("-" * 30)
        
        test_messages = [
            "This is voice number one.",
            "This is voice number two.", 
            "This is voice number three."
        ]
        
        for i, message in enumerate(test_messages):
            if i < len(voices):
                voice = voices[i]
                print(f"Testing voice: {voice.name}")
                engine.setProperty('voice', voice.id)
                engine.setProperty('rate', 150)
                engine.setProperty('volume', 0.9)
                engine.say(message)
                engine.runAndWait()
                time.sleep(1)
        
        print("✅ Voice selection test completed!")
        
    except Exception as e:
        print(f"❌ Error testing voice selection: {e}")

def main():
    """Main test function"""
    print("🎤 Voice System Test Suite")
    print("=" * 60)
    print("This will test different voice engines and voice selection")
    print("Make sure you have speakers/headphones connected")
    print("=" * 60)
    
    # Test 1: Voice Engines
    print("\n1️⃣ Testing Voice Engines...")
    test_voice_engines()
    
    # Test 2: Character Voices
    print("\n2️⃣ Testing Character Voices...")
    test_character_voices()
    
    # Test 3: Voice Selection
    print("\n3️⃣ Testing Voice Selection...")
    test_voice_selection()
    
    print("\n🎉 All voice tests completed!")
    print("\n💡 Tips for better voice diversity:")
    print("   - Install additional voice engines")
    print("   - Use different voice providers (Microsoft, Google, Amazon)")
    print("   - Configure voice settings in your OS")
    print("   - Try different languages for more variety")

if __name__ == "__main__":
    main() 