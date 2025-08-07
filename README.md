# AI NPC Dialogue Generator

A FastAPI-based AI NPC dialogue generator that creates character-consistent conversations using Groq API. Features interactive chat interfaces, conversation memory, and multiple AI provider support.

## 🎮 Features

### Core Functionality
- **Character-Consistent Dialogue**: NPCs maintain their personality and speech patterns
- **Interactive Chat Interface**: Real-time conversation with NPCs
- **Conversation Memory**: NPCs remember previous interactions
- **Multiple AI Providers**: Support for Groq and Google Gemini APIs
- **Rate Limiting**: Built-in rate limit management for free tier usage
- **Security**: Input validation and prompt injection prevention

### Available NPCs
- **Drogun**: Gruff Blacksmith - "Hmph. Show me."
- **Lira**: Enthusiastic Potion Seller - "Oh, wonderful! We have *just* the thing!"
- **Eldrin**: Mysterious Forest Hermit - Cryptic, wise responses

## 🚀 Quick Start

### Prerequisites
```bash
pip install -r requirements.txt
```

### Environment Setup
Create a `.env` file:
```bash
# For Groq (Recommended - Higher limits)
GROQ_API_KEY=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

# For Google Gemini (Alternative)
GEMINI_API_KEY=your_gemini_key_here
```

### Start Servers

**Groq Version (Recommended):**
```bash
python3 -m uvicorn main_groq:app --reload --port 8002
```

**Gemini Version (Phase 2):**
```bash
python3 -m uvicorn main_v2:app --reload --port 8001
```

**Gemini Version (Phase 1):**
```bash
python3 -m uvicorn main:app --reload --port 8000
```

### Interactive Chat

**Groq Chat (Recommended):**
```bash
python3 quick_chat_groq.py
```

**Gemini Chat:**
```bash
python3 quick_chat.py
```

**NPC Selection Chat:**
```bash
python3 chat.py
```

## 📡 API Endpoints

### Generate Dialogue
```bash
# Groq Version
curl -X POST "http://127.0.0.1:8002/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "character_name": "Drogun",
    "character_type": "Gruff Blacksmith",
    "traits": "Gruff, impatient, values hard work",
    "player_input": "Can you repair my sword?"
  }'
```

### Health Check
```bash
curl -X GET "http://127.0.0.1:8002/health"
```

### Sample NPCs
```bash
curl -X GET "http://127.0.0.1:8002/sample-npcs"
```

## 🎯 API Comparison

| Feature | Groq | Gemini |
|---------|------|--------|
| **Rate Limit** | 100 req/min | 15 req/min |
| **Daily Limit** | Much higher | 50 req/day |
| **Speed** | Very fast | Moderate |
| **Free Tier** | Generous | Limited |
| **Status** | ✅ Working | ❌ Quota issues |

## 🛠️ Project Structure

```
hackathomnmmmmm/
├── main_groq.py          # Groq API version (Recommended)
├── main_v2.py            # Gemini Phase 2 (Advanced)
├── main.py               # Gemini Phase 1 (Basic)
├── quick_chat_groq.py    # Groq chat interface
├── quick_chat.py         # Gemini chat interface
├── chat.py               # NPC selection interface
├── test_api.py           # Automated testing
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## 🧪 Testing

### Automated Test Suite
```bash
python3 test_api.py
```

### Manual Testing
```bash
# Test Groq API
curl -X POST "http://127.0.0.1:8002/generate" \
  -H "Content-Type: application/json" \
  -d '{"character_name": "Drogun", "character_type": "Gruff Blacksmith", "traits": "Gruff, impatient", "player_input": "hey"}'
```

## 🔧 Configuration

### Rate Limiting
- **Groq**: 100 requests/minute
- **Gemini**: 15 requests/minute (free tier)

### Models Used
- **Groq**: `llama3-8b-8192` (fast, reliable)
- **Gemini**: `gemini-1.5-flash` (quota limited)

## 🚀 Deployment

### Local Development
```bash
# Start Groq server
python3 -m uvicorn main_groq:app --reload --port 8002

# Start chat interface
python3 quick_chat_groq.py
```

### Production Deployment
1. **Render.com** (Recommended)
2. **Railway.app**
3. **Heroku**

## 📊 Performance

### Response Times
- **Groq**: ~200-500ms
- **Gemini**: ~1-3 seconds

### Character Consistency
- ✅ **Drogun**: Maintains grumpy, short responses
- ✅ **Lira**: Stays enthusiastic and talkative
- ✅ **Eldrin**: Keeps cryptic, wise tone

## 🎮 Example Conversations

### Drogun (Gruff Blacksmith)
```
Player: Can you repair my sword?
Drogun: Hmph. Let me see it. *examines blade* This'll take time. Come back tomorrow.

Player: How much will it cost?
Drogun: Depends. Broken bad? More gold.
```

### Lira (Enthusiastic Potion Seller)
```
Player: I need a healing potion
Lira: Oh, a healing potion, you say? Wonderful! We have *just* the thing!

Player: Do you have anything stronger?
Lira: Stronger? My dear, I have potions that could bring a dragon back from the brink! *winks*
```

## 🔒 Security Features

- **Input Validation**: Prevents malicious inputs
- **Prompt Injection Prevention**: Blocks AI manipulation attempts
- **Rate Limiting**: Prevents abuse
- **Error Handling**: Graceful failure management

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🎯 Future Enhancements

- [ ] Web UI interface
- [ ] More NPC characters
- [ ] Voice synthesis
- [ ] Multi-language support
- [ ] Advanced conversation memory
- [ ] Character customization tools

---

**Built with ❤️ for AI-powered gaming experiences** 