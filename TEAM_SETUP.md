# 🚀 Quick Setup for Teammates

## Clone the Repository
```bash
git clone https://github.com/Salmanmalvasi/Processing_name.git
cd Processing_name
```

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Start the Server (Groq Version - Recommended)
```bash
python3 -m uvicorn main_groq:app --reload --port 8002
```

## Test the Chat Interface
```bash
python3 quick_chat_groq.py
```

## API Testing
```bash
# Test the API
curl -X POST "http://127.0.0.1:8002/generate" \
  -H "Content-Type: application/json" \
  -d '{"character_name": "Drogun", "character_type": "Gruff Blacksmith", "traits": "Gruff, impatient", "player_input": "hey"}'

# Check health
curl -X GET "http://127.0.0.1:8002/health"
```

## Available NPCs
- **Drogun**: Gruff Blacksmith
- **Lira**: Enthusiastic Potion Seller  
- **Eldrin**: Mysterious Forest Hermit

## Features
- ✅ Real-time chat with NPCs
- ✅ Character consistency
- ✅ Conversation memory
- ✅ High rate limits (100 req/min)
- ✅ No daily quota issues

## Demo
Try chatting with Drogun:
```
👤 You: Can you repair my sword?
Drogun: Hmph. Let me see it. *examines blade* This'll take time. Come back tomorrow.

👤 You: How much will it cost?
Drogun: Depends. Broken bad? More gold.
```

## For Frontend Integration
Use the API endpoint: `http://127.0.0.1:8002/generate`

## Need Help?
Check the main README.md for detailed documentation! 