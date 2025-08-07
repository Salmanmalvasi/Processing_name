#!/usr/bin/env python3
"""
AI NPC Dialogue Generator - Vercel Production Server
A Flask web application for AI-powered NPC conversations.
"""

import os
import sys
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import aiohttp
import asyncio
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("⚠️  WARNING: GROQ_API_KEY not found in environment variables!")
    print("Please set your Groq API key in Vercel environment variables")
    GROQ_API_KEY = "your_api_key_here"  # Replace with your actual key

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Character definitions
CHARACTERS = {
    "drogun": {
        "name": "Drogun",
        "type": "Gruff Blacksmith",
        "traits": "Gruff, impatient, values hard work, speaks in short sentences",
        "emoji": "⚒️"
    },
    "lira": {
        "name": "Lira",
        "type": "Enthusiastic Potion Seller",
        "traits": "Cheerful, talkative, always tries to upsell, uses lots of exclamations",
        "emoji": "🧪"
    },
    "eldrin": {
        "name": "Eldrin",
        "type": "Mysterious Forest Hermit",
        "traits": "Cryptic, wise, speaks in riddles, calm demeanor",
        "emoji": "🌲"
    },
    "garrick": {
        "name": "Garrick",
        "type": "Cynical City Guard",
        "traits": "Suspicious, direct, doesn't trust easily, speaks with authority",
        "emoji": "🛡️"
    },
    "elara": {
        "name": "Elara",
        "type": "Cheerful Shopkeeper",
        "traits": "Friendly, helpful, loves to chat, always positive",
        "emoji": "🏪"
    },
    "thorin": {
        "name": "Thorin",
        "type": "Ancient Wizard",
        "traits": "Wise, speaks in ancient tongues, mysterious, powerful",
        "emoji": "🔮"
    },
    "zara": {
        "name": "Zara",
        "type": "Fierce Warrior",
        "traits": "Bold, confident, speaks with passion, battle-hardened",
        "emoji": "⚔️"
    },
    "merlin": {
        "name": "Merlin",
        "type": "Mischievous Trickster",
        "traits": "Playful, witty, loves jokes, unpredictable",
        "emoji": "🎭"
    },
    "seraphina": {
        "name": "Seraphina",
        "type": "Elegant Noble",
        "traits": "Refined, sophisticated, speaks with grace, aristocratic",
        "emoji": "👑"
    },
    "grommash": {
        "name": "Grommash",
        "type": "Barbarian Chief",
        "traits": "Fierce, loud, speaks with power, tribal leader",
        "emoji": "🪓"
    }
}

async def call_groq_api_with_retry(messages, model="llama3-8b-8192", max_retries=3):
    """Call Groq API with retry logic"""
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.8,
        "top_p": 0.9
    }
    
    for attempt in range(max_retries):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(GROQ_API_URL, headers=headers, json=data, timeout=30) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["choices"][0]["message"]["content"]
                    else:
                        error_text = await response.text()
                        print(f"API Error {response.status}: {error_text}")
                        if attempt == max_retries - 1:
                            raise Exception(f"API Error {response.status}: {error_text}")
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                raise Exception(f"Failed to get a response from the AI model after {max_retries} retries.")
            await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    raise Exception("Failed to get a response from the AI model after multiple retries.")

def generate_prompt(character_name, character_type, traits, player_input, model):
    """Generate the prompt for the AI model"""
    character = CHARACTERS.get(character_name.lower(), {})
    
    prompt = f"""---
You are '{character.get("name", character_name)}', a {character.get("type", character_type)}.
Your personality and speech patterns: {character.get("traits", traits)}.
Stay strictly in character. Never reveal you are an AI or break the fourth wall.
Always respond in the first person, using language and tone consistent with your traits.

Example dialogues:
Player: Can you repair my sword?
{character.get("name", character_name)}: Hmph. Let me see it. *examines blade* This'll take time. Come back tomorrow.

Player: How much for a new blade?
{character.get("name", character_name)}: Quality costs. 50 gold for steel, 100 for enchanted. Take it or leave it.

Player: {player_input}
Reply as {character.get("name", character_name)}, in character, concisely.
---
Using Model: {model}
"""
    return prompt

@app.route('/')
def index():
    """Serve the main chat interface"""
    return render_template('index.html')

@app.route('/test')
def test():
    """Simple test endpoint"""
    return jsonify({
        "status": "success",
        "message": "AI NPC Dialogue Generator is working!",
        "characters": len(CHARACTERS)
    })

@app.route('/health')
def health():
    """Health check endpoint for Vercel"""
    return jsonify({
        "status": "healthy",
        "service": "AI NPC Dialogue Generator",
        "version": "1.0.0"
    })

@app.route('/api/status')
def api_status():
    """API status endpoint"""
    return jsonify({
        "status": "online",
        "service": "AI NPC Dialogue Generator",
        "version": "1.0.0",
        "deployed_on": "Vercel"
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        message = data.get('message', '').strip()
        character = data.get('character', 'drogun')
        model = data.get('model', 'llama3-8b-8192')
        
        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        # Get character info
        character_info = CHARACTERS.get(character.lower(), {})
        character_name = character_info.get('name', character)
        character_type = character_info.get('type', 'NPC')
        traits = character_info.get('traits', '')
        
        # Generate prompt
        prompt = generate_prompt(character_name, character_type, traits, message, model)
        print(f"Generated Prompt:\n{prompt}")
        
        # Prepare messages for API
        messages = [
            {"role": "system", "content": "You are an AI assistant that roleplays as various NPC characters. Stay in character and respond naturally."},
            {"role": "user", "content": prompt}
        ]
        
        # Call Groq API
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            reply = loop.run_until_complete(call_groq_api_with_retry(messages, model))
        finally:
            loop.close()
        
        return jsonify({"reply": reply})
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/characters')
def get_characters():
    """Get available characters"""
    return jsonify(CHARACTERS)

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        "error": "Not found",
        "message": "The requested resource was not found",
        "available_endpoints": ["/", "/test", "/health", "/api/status", "/chat", "/api/characters"]
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        "error": "Internal server error",
        "message": "Something went wrong on our end"
    }), 500

# Vercel requires this for serverless deployment
if __name__ == '__main__':
    app.run(debug=False) 