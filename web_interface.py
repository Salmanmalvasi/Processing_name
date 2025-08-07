#!/usr/bin/env python3
"""
Web Interface for AI NPC Dialogue Generator
Simple Flask-based chatbot with character and model selection + Voice Assistant
"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)

# Character definitions with enhanced voice settings
CHARACTERS = {
    "drogun": {
        "name": "Drogun",
        "type": "Gruff Blacksmith",
        "traits": "Gruff, impatient, values hard work, speaks in short sentences",
        "emoji": "⚒️",
        "voice_rate": 120,
        "voice_pitch": 0.7,
        "voice_volume": 0.9,
        "voice_style": "deep_grumpy"
    },
    "lira": {
        "name": "Lira",
        "type": "Enthusiastic Potion Seller",
        "traits": "Cheerful, talkative, always tries to upsell, uses lots of exclamations",
        "emoji": "🧪",
        "voice_rate": 180,
        "voice_pitch": 1.3,
        "voice_volume": 0.95,
        "voice_style": "bubbly_excited"
    },
    "eldrin": {
        "name": "Eldrin",
        "type": "Mysterious Forest Hermit",
        "traits": "Cryptic, wise, speaks in riddles, calm demeanor",
        "emoji": "🌲",
        "voice_rate": 100,
        "voice_pitch": 0.8,
        "voice_volume": 0.85,
        "voice_style": "mysterious_whisper"
    },
    "garrick": {
        "name": "Garrick",
        "type": "Cynical City Guard",
        "traits": "Suspicious, direct, doesn't trust easily, speaks with authority",
        "emoji": "🛡️",
        "voice_rate": 140,
        "voice_pitch": 0.75,
        "voice_volume": 0.9,
        "voice_style": "authoritative_stern"
    },
    "elara": {
        "name": "Elara",
        "type": "Cheerful Shopkeeper",
        "traits": "Friendly, helpful, loves to chat, always positive",
        "emoji": "🏪",
        "voice_rate": 160,
        "voice_pitch": 1.2,
        "voice_volume": 0.9,
        "voice_style": "friendly_warm"
    },
    "thorin": {
        "name": "Thorin",
        "type": "Ancient Wizard",
        "traits": "Wise, speaks in ancient tongues, mysterious, powerful",
        "emoji": "🔮",
        "voice_rate": 90,
        "voice_pitch": 0.6,
        "voice_volume": 0.8,
        "voice_style": "ancient_mystical"
    },
    "zara": {
        "name": "Zara",
        "type": "Fierce Warrior",
        "traits": "Bold, confident, speaks with passion, battle-hardened",
        "emoji": "⚔️",
        "voice_rate": 150,
        "voice_pitch": 1.1,
        "voice_volume": 0.95,
        "voice_style": "fierce_passionate"
    },
    "merlin": {
        "name": "Merlin",
        "type": "Mischievous Trickster",
        "traits": "Playful, witty, loves jokes, unpredictable",
        "emoji": "🎭",
        "voice_rate": 170,
        "voice_pitch": 1.4,
        "voice_volume": 0.9,
        "voice_style": "playful_mischievous"
    }
}

# AI Models
MODELS = {
    "llama3-8b-8192": {
        "name": "llama3-8b-8192",
        "description": "Fast, good for dialogue",
        "speed": "Very Fast",
        "quality": "Good"
    },
    "llama3-70b-8192": {
        "name": "llama3-70b-8192",
        "description": "More powerful, better responses",
        "speed": "Fast",
        "quality": "Excellent"
    },
    "mixtral-8x7b-32768": {
        "name": "mixtral-8x7b-32768",
        "description": "Balanced performance",
        "speed": "Fast",
        "quality": "Very Good"
    },
    "gemma2-9b-it": {
        "name": "gemma2-9b-it",
        "description": "Efficient and reliable",
        "speed": "Very Fast",
        "quality": "Good"
    }
}

@app.route('/')
def index():
    return render_template('index.html', characters=CHARACTERS, models=MODELS)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        message = data.get('message', '')
        character = data.get('character', 'drogun')
        model = data.get('model', 'llama3-8b-8192')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Prepare payload for Groq API
        payload = {
            "character_name": CHARACTERS[character]["name"],
            "character_type": CHARACTERS[character]["type"],
            "traits": CHARACTERS[character]["traits"],
            "player_input": message,
            "model": model
        }
        
        # Call Groq API
        response = requests.post('http://127.0.0.1:8002/generate', json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                'reply': result.get('reply', 'I didn\'t understand that.'),
                'character': CHARACTERS[character]["name"],
                'voice_settings': {
                    'rate': CHARACTERS[character]["voice_rate"],
                    'pitch': CHARACTERS[character]["voice_pitch"],
                    'volume': CHARACTERS[character]["voice_volume"],
                    'style': CHARACTERS[character]["voice_style"]
                }
            })
        else:
            return jsonify({'error': f'API Error: {response.status_code}'}), 500
            
    except requests.exceptions.Timeout:
        return jsonify({'error': 'Request timed out'}), 408
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'Cannot connect to AI service'}), 503
    except Exception as e:
        return jsonify({'error': f'Error: {str(e)}'}), 500

@app.route('/api/status')
def status():
    try:
        response = requests.get('http://127.0.0.1:8002/health', timeout=5)
        if response.status_code == 200:
            return jsonify({'status': 'online'})
        else:
            return jsonify({'status': 'offline'})
    except:
        return jsonify({'status': 'offline'})

@app.route('/api/voice-settings/<character>')
def voice_settings(character):
    """Get voice settings for a character"""
    if character in CHARACTERS:
        return jsonify({
            'rate': CHARACTERS[character]["voice_rate"],
            'pitch': CHARACTERS[character]["voice_pitch"],
            'volume': CHARACTERS[character]["voice_volume"],
            'style': CHARACTERS[character]["voice_style"],
            'name': CHARACTERS[character]["name"]
        })
    else:
        return jsonify({'error': 'Character not found'}), 404

@app.route('/api/characters')
def get_characters():
    """Get all available characters"""
    return jsonify(CHARACTERS)

@app.route('/api/models')
def get_models():
    """Get all available models"""
    return jsonify(MODELS)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 