#!/usr/bin/env python3
"""
Deep Voice Test Script for AI NPC Dialogue Generator
Test improved deep voices with better voice selection
"""
import pyttsx3
import time

def test_deep_voices():
    """Test different deep voice options"""
    print("🎤 Deep Voice Quality Test")
    print("=" * 50)
    
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        # Find deep male voices
        deep_voices = []
        for voice in voices:
            if (voice.lang.startsWith('en') and 
                (voice.name.lower().includes('daniel') or
                 voice.name.lower().includes('albert') or
                 voice.name.lower().includes('fred') or
                 voice.name.lower().includes('ralph') or
                 voice.name.lower().includes('grandpa'))):
                deep_voices.append(voice)
        
        print(f"Found {len(deep_voices)} deep voices:")
        for voice in deep_voices:
            print(f"  - {voice.name}")
        
        # Test each deep voice
        test_message = "This is a test of deep voice quality. How does this sound?"
        
        for voice in deep_voices:
            print(f"\n🎤 Testing {voice.name}:")
            engine.setProperty('voice', voice.id)
            engine.setProperty('rate', 120)
            engine.setProperty('volume', 0.9)
            
            print(f"   Speaking: '{test_message}'")
            engine.say(test_message)
            engine.runAndWait()
            time.sleep(2)
        
        print("\n✅ Deep voice test completed!")
        
    except Exception as e:
        print(f"❌ Error testing deep voices: {e}")

def test_character_deep_voices():
    """Test character-specific deep voice settings"""
    print("\n🎭 Character Deep Voice Test")
    print("=" * 50)
    
    deep_characters = {
        "Drogun": {
            "description": "Gruff blacksmith",
            "voice": "daniel",
            "rate": 120,
            "pitch": 0.8,
            "style": "deep_grumpy"
        },
        "Garrick": {
            "description": "Authoritative guard",
            "voice": "albert", 
            "rate": 140,
            "pitch": 0.7,
            "style": "authoritative_stern"
        },
        "Eldrin": {
            "description": "Mysterious hermit",
            "voice": "fred",
            "rate": 90,
            "pitch": 0.9,
            "style": "mysterious_whisper"
        },
        "Thorin": {
            "description": "Ancient wizard",
            "voice": "ralph",
            "rate": 80,
            "pitch": 0.6,
            "style": "ancient_mystical"
        },
        "Grommash": {
            "description": "Barbarian chief",
            "voice": "grandpa",
            "rate": 110,
            "pitch": 0.5,
            "style": "barbaric_powerful"
        }
    }
    
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        for char_name, char_data in deep_characters.items():
            print(f"\n🎭 Testing {char_name} ({char_data['description']}):")
            print(f"   Voice: {char_data['voice']}")
            print(f"   Rate: {char_data['rate']} WPM")
            print(f"   Pitch: {char_data['pitch']}")
            print(f"   Style: {char_data['style']}")
            
            # Find the voice
            target_voice = None
            for voice in voices:
                if char_data['voice'].lower() in voice.name.lower():
                    target_voice = voice
                    break
            
            if target_voice:
                engine.setProperty('voice', target_voice.id)
                engine.setProperty('rate', char_data['rate'])
                engine.setProperty('volume', 0.9)
                
                print(f"   ✅ Using: {target_voice.name}")
                
                # Test message
                test_message = f"Hello! I am {char_name}. This is my improved deep voice."
                print(f"   Speaking: '{test_message}'")
                
                engine.say(test_message)
                engine.runAndWait()
                time.sleep(2)
            else:
                print(f"   ❌ Voice '{char_data['voice']}' not found")
        
        print("\n✅ Character deep voice test completed!")
        
    except Exception as e:
        print(f"❌ Error testing character deep voices: {e}")

def test_voice_improvements():
    """Test voice improvements for deep voices"""
    print("\n🚀 Deep Voice Improvements Test")
    print("=" * 50)
    
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        # Find a good deep voice
        test_voice = None
        for voice in voices:
            if 'daniel' in voice.name.lower():
                test_voice = voice
                break
        
        if test_voice:
            engine.setProperty('voice', test_voice.id)
            print(f"Using voice: {test_voice.name}")
            
            # Test different settings for better deep voice
            settings = [
                {"rate": 100, "description": "Slow, deep"},
                {"rate": 120, "description": "Normal, deep"},
                {"rate": 140, "description": "Fast, deep"},
                {"rate": 80, "description": "Very slow, deep"}
            ]
            
            test_message = "This is a test of deep voice improvements."
            
            for setting in settings:
                print(f"\n🎤 Testing: {setting['description']}")
                engine.setProperty('rate', setting['rate'])
                engine.setProperty('volume', 0.9)
                
                print(f"   Rate: {setting['rate']} WPM")
                print(f"   Speaking: '{test_message}'")
                
                engine.say(test_message)
                engine.runAndWait()
                time.sleep(1)
        
        print("\n✅ Deep voice improvements test completed!")
        
    except Exception as e:
        print(f"❌ Error testing deep voice improvements: {e}")

def main():
    """Main test function"""
    print("🎤 Deep Voice Test Suite")
    print("=" * 60)
    print("Testing improved deep voices with better voice selection")
    print("Make sure you have speakers/headphones connected")
    print("=" * 60)
    
    # Test 1: Deep Voices
    print("\n1️⃣ Testing Deep Voice Quality...")
    test_deep_voices()
    
    # Test 2: Character Deep Voices
    print("\n2️⃣ Testing Character Deep Voices...")
    test_character_deep_voices()
    
    # Test 3: Deep Voice Improvements
    print("\n3️⃣ Testing Deep Voice Improvements...")
    test_voice_improvements()
    
    print("\n🎉 All deep voice tests completed!")
    print("\n💡 Deep Voice Tips:")
    print("   - Daniel voice is good for grumpy characters")
    print("   - Albert voice is good for authoritative characters")
    print("   - Fred voice is good for mysterious characters")
    print("   - Ralph voice is good for ancient characters")
    print("   - Grandpa voice is good for barbaric characters")

if __name__ == "__main__":
    main() 