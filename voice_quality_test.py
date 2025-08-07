#!/usr/bin/env python3
"""
Voice Quality Test Script for AI NPC Dialogue Generator
Test improved voice system with better voice selection
"""
import pyttsx3
import time

def test_character_voices():
    """Test character-specific voice settings with improved voices"""
    print("🎭 Character Voice Quality Test")
    print("=" * 60)
    
    characters = {
        "Drogun": {
            "description": "Deep, grumpy blacksmith",
            "rate": 90,
            "pitch": 0.4,
            "style": "deep_grumpy",
            "voice_target": "albert"
        },
        "Lira": {
            "description": "Cheerful potion seller", 
            "rate": 200,
            "pitch": 1.6,
            "style": "bubbly_excited",
            "voice_target": "samantha"
        },
        "Eldrin": {
            "description": "Mysterious forest hermit",
            "rate": 70,
            "pitch": 0.6,
            "style": "mysterious_whisper",
            "voice_target": "daniel"
        },
        "Garrick": {
            "description": "Authoritative city guard",
            "rate": 110,
            "pitch": 0.5,
            "style": "authoritative_stern",
            "voice_target": "fred"
        },
        "Elara": {
            "description": "Warm shopkeeper",
            "rate": 180,
            "pitch": 1.4,
            "style": "friendly_warm",
            "voice_target": "karen"
        },
        "Thorin": {
            "description": "Ancient wizard",
            "rate": 60,
            "pitch": 0.3,
            "style": "ancient_mystical",
            "voice_target": "grandpa"
        },
        "Zara": {
            "description": "Fierce warrior",
            "rate": 170,
            "pitch": 1.3,
            "style": "fierce_passionate",
            "voice_target": "tessa"
        },
        "Merlin": {
            "description": "Mischievous trickster",
            "rate": 190,
            "pitch": 1.7,
            "style": "playful_mischievous",
            "voice_target": "jester"
        },
        "Seraphina": {
            "description": "Elegant noble",
            "rate": 130,
            "pitch": 1.2,
            "style": "elegant_refined",
            "voice_target": "moira"
        },
        "Grommash": {
            "description": "Barbarian chief",
            "rate": 100,
            "pitch": 0.2,
            "style": "barbaric_powerful",
            "voice_target": "ralph"
        }
    }
    
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        print(f"Found {len(voices)} available voices")
        print("Testing character voices with improved settings:")
        print("-" * 60)
        
        for char_name, char_data in characters.items():
            print(f"\n🎭 Testing {char_name} ({char_data['description']}):")
            print(f"   Rate: {char_data['rate']} WPM")
            print(f"   Pitch: {char_data['pitch']}")
            print(f"   Style: {char_data['style']}")
            print(f"   Target Voice: {char_data['voice_target']}")
            
            # Find the target voice
            target_voice = None
            for voice in voices:
                if char_data['voice_target'].lower() in voice.name.lower():
                    target_voice = voice
                    break
            
            if target_voice:
                engine.setProperty('voice', target_voice.id)
                print(f"   ✅ Using voice: {target_voice.name}")
            else:
                print(f"   ⚠️  Target voice '{char_data['voice_target']}' not found, using default")
            
            # Set improved voice settings
            engine.setProperty('rate', char_data['rate'])
            engine.setProperty('volume', 0.9)
            
            # Test message
            test_message = f"Hello! I am {char_name}. This is my improved voice with better quality."
            print(f"   Speaking: '{test_message}'")
            
            engine.say(test_message)
            engine.runAndWait()
            time.sleep(2)
        
        print("\n✅ Character voice quality test completed!")
        
    except Exception as e:
        print(f"❌ Error testing character voices: {e}")

def test_voice_comparison():
    """Compare different voice qualities"""
    print("\n🔍 Voice Quality Comparison Test")
    print("=" * 60)
    
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        # Test different voice types
        test_message = "This is a test of voice quality and clarity."
        
        voice_types = [
            {"name": "Albert", "target": "albert", "description": "Deep male voice"},
            {"name": "Samantha", "target": "samantha", "description": "Clear female voice"},
            {"name": "Daniel", "target": "daniel", "description": "Strong male voice"},
            {"name": "Fred", "target": "fred", "description": "Authoritative male voice"},
            {"name": "Karen", "target": "karen", "description": "Warm female voice"},
            {"name": "Grandpa", "target": "grandpa", "description": "Elderly male voice"},
            {"name": "Tessa", "target": "tessa", "description": "Strong female voice"},
            {"name": "Jester", "target": "jester", "description": "Playful voice"},
            {"name": "Moira", "target": "moira", "description": "Elegant female voice"},
            {"name": "Ralph", "target": "ralph", "description": "Powerful male voice"}
        ]
        
        for voice_type in voice_types:
            print(f"\n🎤 Testing {voice_type['name']} ({voice_type['description']}):")
            
            # Find the voice
            target_voice = None
            for voice in voices:
                if voice_type['target'].lower() in voice.name.lower():
                    target_voice = voice
                    break
            
            if target_voice:
                engine.setProperty('voice', target_voice.id)
                engine.setProperty('rate', 150)
                engine.setProperty('volume', 0.9)
                
                print(f"   ✅ Using: {target_voice.name}")
                print(f"   Speaking: '{test_message}'")
                
                engine.say(test_message)
                engine.runAndWait()
                time.sleep(1)
            else:
                print(f"   ❌ Voice '{voice_type['name']}' not found")
        
        print("\n✅ Voice quality comparison completed!")
        
    except Exception as e:
        print(f"❌ Error testing voice comparison: {e}")

def test_voice_improvements():
    """Test voice improvements and enhancements"""
    print("\n🚀 Voice Improvements Test")
    print("=" * 60)
    
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        print("Testing voice improvements:")
        print("-" * 40)
        
        # Test different rates for better quality
        rates = [80, 120, 160, 200]
        test_voice = None
        
        # Find a good test voice
        for voice in voices:
            if 'samantha' in voice.name.lower() or 'albert' in voice.name.lower():
                test_voice = voice
                break
        
        if test_voice:
            engine.setProperty('voice', test_voice.id)
            print(f"Using voice: {test_voice.name}")
            
            for rate in rates:
                print(f"\n🎤 Testing rate: {rate} WPM")
                engine.setProperty('rate', rate)
                engine.setProperty('volume', 0.9)
                
                test_message = f"This is a test at {rate} words per minute for better voice quality."
                engine.say(test_message)
                engine.runAndWait()
                time.sleep(1)
        
        print("\n✅ Voice improvements test completed!")
        
    except Exception as e:
        print(f"❌ Error testing voice improvements: {e}")

def main():
    """Main test function"""
    print("🎤 Voice Quality Test Suite")
    print("=" * 60)
    print("Testing improved voice system with better voice selection")
    print("Make sure you have speakers/headphones connected")
    print("=" * 60)
    
    # Test 1: Character Voices
    print("\n1️⃣ Testing Character Voices with Improved Quality...")
    test_character_voices()
    
    # Test 2: Voice Comparison
    print("\n2️⃣ Testing Voice Quality Comparison...")
    test_voice_comparison()
    
    # Test 3: Voice Improvements
    print("\n3️⃣ Testing Voice Improvements...")
    test_voice_improvements()
    
    print("\n🎉 All voice quality tests completed!")
    print("\n💡 Voice Quality Tips:")
    print("   - Use system voices for better quality")
    print("   - Adjust rate and pitch for character personality")
    print("   - Test different voice engines")
    print("   - Consider using cloud voice services for even better quality")

if __name__ == "__main__":
    main() 