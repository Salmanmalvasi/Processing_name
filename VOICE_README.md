# 🎤 Voice Assistant for AI NPC Dialogue Generator

A comprehensive voice assistant that allows you to have natural conversations with AI NPCs using speech recognition and text-to-speech.

## ✨ Features

### 🎭 **Character Voices**
- **Drogun** (Gruff Blacksmith) - Slow, deep voice
- **Lira** (Enthusiastic Potion Seller) - Fast, cheerful voice  
- **Eldrin** (Mysterious Forest Hermit) - Slow, wise voice
- **Garrick** (Cynical City Guard) - Medium, authoritative voice
- **Elara** (Cheerful Shopkeeper) - Fast, friendly voice

### 🤖 **AI Models**
- **llama3-8b-8192** - Fast, good for dialogue
- **llama3-70b-8192** - More powerful, better responses
- **mixtral-8x7b-32768** - Balanced performance
- **gemma2-9b-it** - Efficient and reliable

### 🎤 **Voice Commands**
- **"quit" or "exit"** - Stop the conversation
- **"change character"** - Switch to a different NPC
- **"change model"** - Switch AI models
- **"status"** - Check API status
- **"help"** - Show available commands

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install SpeechRecognition pyttsx3 pyaudio
```

### 2. Start the API Server
```bash
python3 main_groq.py
```

### 3. Test Voice Assistant
```bash
python3 simple_voice_test.py
```

### 4. Start Voice Assistant
```bash
python3 voice_assistant.py
```

## 📋 Requirements

### System Requirements
- **Microphone** - For speech input
- **Speakers/Headphones** - For voice output
- **Internet Connection** - For speech recognition and AI API

### Python Packages
- `SpeechRecognition` - Speech-to-text
- `pyttsx3` - Text-to-speech
- `pyaudio` - Audio I/O
- `requests` - API communication

## 🎯 Usage

### Interactive Menu
The voice assistant provides an interactive menu:

```
🎤 Voice Assistant Menu
==============================
1. 🎭 Show characters
2. 🤖 Show models  
3. 🎤 Start voice conversation
4. ⚙️  Change character
5. 🔧 Change model
6. 📊 Check API status
7. 🧪 Test voice
0. ❌ Exit
```

### Voice Conversation Mode
1. **Start conversation** - Choose option 3
2. **Speak naturally** - The AI will respond with voice
3. **Use voice commands** - Say "change character" or "quit"
4. **Enjoy the conversation** - Each character has unique voice settings

## 🎨 Character Voice Profiles

### Drogun (Gruff Blacksmith)
- **Voice Rate**: 150 WPM (slow)
- **Voice Pitch**: 0.8 (deep)
- **Style**: Short, direct sentences

### Lira (Enthusiastic Potion Seller)  
- **Voice Rate**: 180 WPM (fast)
- **Voice Pitch**: 1.2 (high)
- **Style**: Cheerful, exclamatory

### Eldrin (Mysterious Forest Hermit)
- **Voice Rate**: 120 WPM (very slow)
- **Voice Pitch**: 0.9 (medium-low)
- **Style**: Cryptic, wise

### Garrick (Cynical City Guard)
- **Voice Rate**: 140 WPM (medium)
- **Voice Pitch**: 0.85 (deep)
- **Style**: Suspicious, authoritative

### Elara (Cheerful Shopkeeper)
- **Voice Rate**: 160 WPM (fast)
- **Voice Pitch**: 1.1 (high)
- **Style**: Friendly, helpful

## 🔧 Configuration

### Speech Recognition Settings
- **Energy Threshold**: 4000 (adjustable)
- **Dynamic Energy**: Enabled
- **Pause Threshold**: 0.8 seconds
- **Timeout**: 5 seconds
- **Phrase Time Limit**: 10 seconds

### Text-to-Speech Settings
- **Default Rate**: 150 WPM
- **Volume**: 0.9 (90%)
- **Voice Selection**: Auto-selects best available voice

## 🧪 Testing

### Run Voice Tests
```bash
python3 simple_voice_test.py
```

This will test:
1. **Speech Recognition** - Can it understand your voice?
2. **Text-to-Speech** - Can you hear the AI responses?
3. **Voice Conversation** - Full conversation test

### Troubleshooting

#### Microphone Issues
```bash
# Check microphone permissions
python3 -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
```

#### Audio Issues
```bash
# Test audio output
python3 -c "import pyttsx3; engine = pyttsx3.init(); engine.say('Test'); engine.runAndWait()"
```

#### Installation Issues
```bash
# Install pyaudio (macOS)
brew install portaudio
pip install pyaudio

# Install pyaudio (Ubuntu/Debian)
sudo apt-get install python3-pyaudio
pip install pyaudio
```

## 🎮 Voice Commands Reference

### Basic Commands
- **"quit"** - Exit voice conversation
- **"exit"** - Exit voice conversation  
- **"stop"** - Exit voice conversation
- **"bye"** - Exit voice conversation

### Character Management
- **"change character"** - Switch to different NPC
- **"switch character"** - Switch to different NPC
- **"new character"** - Switch to different NPC

### Model Management
- **"change model"** - Switch AI models
- **"switch model"** - Switch AI models
- **"new model"** - Switch AI models

### System Commands
- **"status"** - Check API status
- **"help"** - Show available commands
- **"test"** - Run voice test

## 🔄 Integration with Web Interface

The voice assistant works alongside the web interface:

1. **Web Interface** - Visual chat with characters
2. **Voice Assistant** - Voice conversations
3. **Terminal Chat** - Text-based conversations

All three use the same Groq API backend for consistent AI responses.

## 🚀 Advanced Features

### Conversation History
- Maintains context across voice exchanges
- Remembers previous dialogue turns
- Limits history to prevent memory issues

### Error Handling
- Graceful handling of speech recognition errors
- Automatic retry for failed API calls
- Clear error messages and recovery

### Performance Optimization
- Efficient speech processing
- Optimized text-to-speech settings
- Minimal latency for real-time conversation

## 🎯 Best Practices

### For Best Speech Recognition
1. **Speak clearly** - Enunciate your words
2. **Reduce background noise** - Use in quiet environment
3. **Speak at normal volume** - Don't whisper or shout
4. **Wait for "Listening..."** - Don't speak too early

### For Best Voice Output
1. **Adjust system volume** - Ensure speakers are audible
2. **Use headphones** - For better audio quality
3. **Test first** - Run voice test before full conversation
4. **Choose quiet environment** - Minimize audio interference

## 🔮 Future Enhancements

### Planned Features
- **Voice Emotion Detection** - AI responds to your tone
- **Multi-language Support** - Non-English conversations
- **Voice Cloning** - Custom character voices
- **Background Music** - Ambient sounds for immersion
- **Voice Commands** - More advanced voice control

### Technical Improvements
- **Offline Speech Recognition** - No internet required
- **Better Voice Synthesis** - More natural voices
- **Noise Cancellation** - Better audio processing
- **Voice Biometrics** - Recognize different speakers

## 📞 Support

### Common Issues
1. **"No speech detected"** - Check microphone permissions
2. **"Could not understand speech"** - Speak more clearly
3. **"Audio not playing"** - Check system volume
4. **"API connection error"** - Ensure server is running

### Getting Help
- Run `python3 simple_voice_test.py` for diagnostics
- Check microphone and speaker settings
- Ensure Groq API server is running on port 8002
- Verify internet connection for speech recognition

---

**🎤 Ready to have voice conversations with AI NPCs? Start with `python3 voice_assistant.py`!** 