# AI NPC Dialogue Generator

A FastAPI-based AI NPC dialogue generator that creates character-consistent conversations using Groq API. Features interactive chat interfaces, conversation memory, and robust AI provider support.

## 🎮 Features

### Core Functionality
- **Character-Consistent Dialogue**: NPCs maintain their personality and speech patterns
- **Interactive Chat Interface**: Real-time conversation with NPCs
- **Conversation Memory**: NPCs remember previous interactions
- **Groq AI Integration**: Fast and reliable AI responses
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
# Groq API Key (Required)
GROQ_API_KEY=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
```

### Start Server
```bash
python3 -m uvicorn main_groq:app --reload --port 8002
```

### Interactive Chat

**Quick Chat (Recommended):**
```bash
python3 quick_chat_groq.py
```

**NPC Selection Chat:**
```bash
python3 chat_fixed.py
```

**Model Manager:**
```bash
python3 model_manager.py
```

## 📡 API Endpoints

### Generate Dialogue
```bash
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

## 🎯 Groq API Features

| Feature | Details |
|---------|---------|
| **Model** | llama3-8b-8192 |
| **Rate Limit** | 100 requests/minute |
| **Response Time** | ~200-500ms |
| **Reliability** | High |
| **Free Tier** | Generous limits |

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