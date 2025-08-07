#!/usr/bin/env python3
"""
Simple Voice Test for AI NPC Dialogue Generator
Tests speech recognition and text-to-speech functionality
"""

import speech_recognition as sr
import pyttsx3
import time

def test_speech_recognition():
    """Test speech recognition"""
    print("🎤 Testing Speech Recognition")
    print("=" * 30)
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    
    # Adjust for ambient noise
    print("Adjusting for ambient noise...")
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=2)
    
    print("🎤 Say something when prompted...")
    print("(You have 5 seconds to speak)")
    
    try:
        with microphone as source:
            print("🎤 Listening... (speak now)")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        
        print("🔄 Processing speech...")
        text = recognizer.recognize_google(audio)
        print(f"✅ Success! You said: '{text}'")
        return text
        
    except sr.WaitTimeoutError:
        print("❌ No speech detected within timeout")
        return None
    except sr.UnknownValueError:
        print("❌ Could not understand speech")
        return None
    except sr.RequestError as e:
        print(f"❌ Speech recognition error: {e}")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def test_text_to_speech():
    """Test text-to-speech"""
    print("\n🔊 Testing Text-to-Speech")
    print("=" * 30)
    
    try:
        engine = pyttsx3.init()
        
        # Get available voices
        voices = engine.getProperty('voices')
        print(f"Available voices: {len(voices)}")
        
        # Set properties
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        # Try to set a good voice
        if voices:
            # Prefer a female voice
            for voice in voices:
                if "female" in voice.name.lower() or "samantha" in voice.name.lower():
                    engine.setProperty('voice', voice.id)
                    print(f"Using voice: {voice.name}")
                    break
            else:
                engine.setProperty('voice', voices[0].id)
                print(f"Using voice: {voices[0].name}")
        
        # Test speech
        test_text = "Hello! This is a test of the text-to-speech system. If you can hear this clearly, the voice synthesis is working properly."
        print(f"Speaking: '{test_text}'")
        
        engine.say(test_text)
        engine.runAndWait()
        
        print("✅ Text-to-speech test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Text-to-speech error: {e}")
        return False

def test_voice_conversation():
    """Test a simple voice conversation"""
    print("\n🎤 Testing Voice Conversation")
    print("=" * 35)
    
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()
    engine = pyttsx3.init()
    
    # Configure
    engine.setProperty('rate', 150)
    engine.setProperty('volume', 0.9)
    
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
    
    print("🎤 Say 'hello' to start the conversation...")
    
    try:
        with microphone as source:
            print("🎤 Listening... (say 'hello')")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        
        text = recognizer.recognize_google(audio).lower()
        print(f"👤 You said: '{text}'")
        
        if "hello" in text:
            response = "Hello! Nice to meet you. This is a test of the voice conversation system."
            print(f"🤖 Response: '{response}'")
            
            engine.say(response)
            engine.runAndWait()
            
            print("✅ Voice conversation test successful!")
            return True
        else:
            print("❌ Didn't hear 'hello'")
            return False
            
    except Exception as e:
        print(f"❌ Conversation test error: {e}")
        return False

def main():
    """Main test function"""
    print("🎤 Voice Assistant Test Suite")
    print("=" * 40)
    print("This will test speech recognition and text-to-speech")
    print("Make sure you have a working microphone and speakers")
    print("=" * 40)
    
    # Test 1: Speech Recognition
    print("\n1️⃣ Testing Speech Recognition...")
    speech_result = test_speech_recognition()
    
    # Test 2: Text-to-Speech
    print("\n2️⃣ Testing Text-to-Speech...")
    tts_result = test_text_to_speech()
    
    # Test 3: Voice Conversation
    print("\n3️⃣ Testing Voice Conversation...")
    conversation_result = test_voice_conversation()
    
    # Summary
    print("\n📊 Test Results Summary")
    print("=" * 25)
    print(f"Speech Recognition: {'✅ PASS' if speech_result else '❌ FAIL'}")
    print(f"Text-to-Speech: {'✅ PASS' if tts_result else '❌ FAIL'}")
    print(f"Voice Conversation: {'✅ PASS' if conversation_result else '❌ FAIL'}")
    
    if speech_result and tts_result:
        print("\n🎉 All tests passed! Voice assistant is ready to use.")
        print("Run 'python3 voice_assistant.py' to start the full voice assistant.")
    else:
        print("\n⚠️  Some tests failed. Please check your microphone and speakers.")
        print("Make sure you have the required packages installed:")
        print("pip install SpeechRecognition pyttsx3 pyaudio")

if __name__ == "__main__":
    main() 