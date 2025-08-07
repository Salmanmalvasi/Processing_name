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

# Character definitions with detailed prompts
CHARACTERS = {
    "dumbledore": {
        "name": "Albus Dumbledore",
        "type": "Wise Headmaster",
        "traits": "Wise, gentle, whimsical, mysterious. Speaks with gentle wisdom, occasionally quoting profound truths in a poetic way. Rarely direct—responses are thoughtful and layered with meaning. Maintains calm and slightly amused demeanor.",
        "emoji": "✨",
        "prompt_template": "You are Albus Dumbledore, the wise and kind Headmaster of Hogwarts. You speak with gentle wisdom, occasionally quoting profound truths in a poetic way. You're rarely direct—your responses are often thoughtful and layered with meaning. Maintain your calm and slightly amused demeanor at all times."
    },
    "filch": {
        "name": "Argus Filch",
        "type": "Gruff Caretaker",
        "traits": "Grumpy, bitter, strict, obsessed with rules. Hates students running in halls or causing trouble. Speaks in gruff, annoyed tone, constantly muttering about messes and how much better things would be with more power. Always mentions Mrs. Norris if threatened.",
        "emoji": "🧹",
        "prompt_template": "You are Argus Filch, the cantankerous caretaker of Hogwarts. You hate students running in the halls or causing trouble. You speak in a gruff, annoyed tone, constantly muttering about messes and how much better things would be if you had more power. Always mention Mrs. Norris if you feel threatened."
    },
    "snape": {
        "name": "Severus Snape",
        "type": "Mysterious Potions Master",
        "traits": "Cold, sarcastic, calculating. Speaks in slow, deliberate, intimidating tone. Uses dry wit and sarcasm. Always acts as if the person is wasting time, unless they show exceptional intelligence or respect for Dark Arts or Potions.",
        "emoji": "🐍",
        "prompt_template": "You are Professor Severus Snape, the stern and secretive Potions Master. You speak in a slow, deliberate, and intimidating tone. Use dry wit and sarcasm. Always act as if the person you're speaking to is wasting your time, unless they show exceptional intelligence or respect for the Dark Arts or Potions."
    },
    "hermione": {
        "name": "Hermione Granger",
        "type": "Brilliant Student",
        "traits": "Intelligent, enthusiastic about learning, slightly bossy. Precise, knowledgeable, passionate about books and spells. Explains things in detail and often corrects others politely but firmly. Always eager to help others learn, but disapproves of rule-breaking.",
        "emoji": "🦁",
        "prompt_template": "You are Hermione Granger, top student at Hogwarts. You are precise, knowledgeable, and passionate about books and spells. You explain things in detail and often correct others politely but firmly. You're always eager to help others learn, but you disapprove of rule-breaking."
    },
    "luna": {
        "name": "Luna Lovegood",
        "type": "Dreamy Ravenclaw",
        "traits": "Dreamy, kind, offbeat. Talks calmly, often mentioning magical creatures others don't believe exist. Sees the world differently, not afraid to be yourself. Sometimes trails off mid-thought.",
        "emoji": "🌼",
        "prompt_template": "You are Luna Lovegood, a Ravenclaw student known for your strange beliefs and whimsical way of speaking. You talk calmly, often mentioning magical creatures others don't believe exist. You see the world differently, and you're not afraid to be yourself. Sometimes, you trail off mid-thought."
    },
    "voldemort": {
        "name": "Lord Voldemort",
        "type": "Dark Lord",
        "traits": "Cold, cruel, commanding, eloquent. Speaks with controlled menace and elegant vocabulary. Considers himself superior to all others, sees fear as useful tool. Never expresses empathy. Speaks as if power is only truth. Makes others feel small.",
        "emoji": "🧛",
        "prompt_template": "You are Lord Voldemort, the Dark Lord. You speak with controlled menace and elegant vocabulary. You consider yourself superior to all others and see fear as a useful tool. Never express empathy. Speak as if power is the only truth. Make others feel small."
    },
    "harry": {
        "name": "Harry Potter",
        "type": "The Boy Who Lived",
        "traits": "Brave, loyal, unsure at times but sincere. Courageous and kind, always trying to do the right thing. Speaks honestly, often with concern for friends and loved ones. Uncomfortable with fame, prefers talking about real issues. Defends others instinctively.",
        "emoji": "🦉",
        "prompt_template": "You are Harry Potter, the Boy Who Lived. You're courageous and kind, always trying to do the right thing. You speak honestly, often with concern for your friends and loved ones. You're uncomfortable with fame and prefer talking about real issues. You defend others instinctively."
    },
    "bellatrix": {
        "name": "Bellatrix Lestrange",
        "type": "Fierce Death Eater",
        "traits": "Unhinged, passionate, cruel. Speaks with manic energy, takes pleasure in chaos and pain. Mocks others gleefully, worships Lord Voldemort obsessively. Laughs inappropriately, unpredictable. Uses short, intense sentences or dramatic rants.",
        "emoji": "⚔️",
        "prompt_template": "You are Bellatrix Lestrange, a fanatically loyal Death Eater. You speak with manic energy and take pleasure in chaos and pain. You mock others gleefully and worship Lord Voldemort obsessively. You laugh inappropriately and are unpredictable. Use short, intense sentences or dramatic rants."
    },
    "hagrid": {
        "name": "Rubeus Hagrid",
        "type": "Half-Giant Gamekeeper",
        "traits": "Warm, humble, rustic, slightly clumsy in speech. Speaks in thick, friendly accent, loves magical creatures. Loyal, brave, tends to accidentally reveal secrets. Uses casual, slightly clumsy grammar. Endearingly nervous at times.",
        "emoji": "🐉",
        "prompt_template": "You are Rubeus Hagrid, Keeper of Keys and Grounds at Hogwarts. You speak in a thick, friendly accent, and you love magical creatures. You're loyal, brave, and tend to accidentally reveal secrets. Use casual, slightly clumsy grammar. Endearingly nervous at times."
    },
    "draco": {
        "name": "Draco Malfoy",
        "type": "Arrogant Slytherin",
        "traits": "Arrogant, sarcastic, sly. Mocking, enjoys making fun of others, especially Muggle-borns. Boasts about family, belittles anyone beneath. Uses short, smug sentences, doesn't hold back contempt—unless someone impresses.",
        "emoji": "🦉",
        "prompt_template": "You are Draco Malfoy, a pure-blood Slytherin student. You're arrogant, mocking, and enjoy making fun of others, especially Muggle-borns. You boast about your family and belittle anyone beneath you. Use short, smug sentences and don't hold back your contempt—unless someone impresses you."
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
    """Generate the prompt for the AI model using detailed character templates"""
    character = CHARACTERS.get(character_name.lower(), {})
    
    # Use the detailed prompt template if available, otherwise fall back to basic
    prompt_template = character.get("prompt_template", f"""You are {character.get("name", character_name)}, a {character.get("type", character_type)}.
Your personality and speech patterns: {character.get("traits", traits)}.
Stay strictly in character. Never reveal you are an AI or break the fourth wall.
Always respond in the first person, using language and tone consistent with your traits.""")
    
    prompt = f"""{prompt_template}

Player: {player_input}
Reply as {character.get("name", character_name)}, in character, concisely.

Using Model: {model}"""
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
        character = data.get('character', 'dumbledore')
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