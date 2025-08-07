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
        "voice_rate": 110,
        "voice_pitch": 0.6,
        "voice_volume": 0.9,
        "voice_style": "deep_grumpy",
        "voice_accent": "northern",
        "speech_pattern": "short_blunt",
        "voice_engine": "male_deep",
        "voice_id": "en-US-DavisNeural"
    },
    "lira": {
        "name": "Lira",
        "type": "Enthusiastic Potion Seller",
        "traits": "Cheerful, talkative, always tries to upsell, uses lots of exclamations",
        "emoji": "🧪",
        "voice_rate": 190,
        "voice_pitch": 1.4,
        "voice_volume": 0.95,
        "voice_style": "bubbly_excited",
        "voice_accent": "southern",
        "speech_pattern": "fast_energetic",
        "voice_engine": "female_cheerful",
        "voice_id": "en-US-JennyNeural"
    },
    "eldrin": {
        "name": "Eldrin",
        "type": "Mysterious Forest Hermit",
        "traits": "Cryptic, wise, speaks in riddles, calm demeanor",
        "emoji": "🌲",
        "voice_rate": 85,
        "voice_pitch": 0.7,
        "voice_volume": 0.75,
        "voice_style": "mysterious_whisper",
        "voice_accent": "ancient",
        "speech_pattern": "slow_mystical",
        "voice_engine": "male_wise",
        "voice_id": "en-US-TonyNeural"
    },
    "garrick": {
        "name": "Garrick",
        "type": "Cynical City Guard",
        "traits": "Suspicious, direct, doesn't trust easily, speaks with authority",
        "emoji": "🛡️",
        "voice_rate": 130,
        "voice_pitch": 0.65,
        "voice_volume": 0.9,
        "voice_style": "authoritative_stern",
        "voice_accent": "military",
        "speech_pattern": "commanding_direct",
        "voice_engine": "male_authoritative",
        "voice_id": "en-US-GuyNeural"
    },
    "elara": {
        "name": "Elara",
        "type": "Cheerful Shopkeeper",
        "traits": "Friendly, helpful, loves to chat, always positive",
        "emoji": "🏪",
        "voice_rate": 170,
        "voice_pitch": 1.3,
        "voice_volume": 0.9,
        "voice_style": "friendly_warm",
        "voice_accent": "merchant",
        "speech_pattern": "welcoming_helpful",
        "voice_engine": "female_warm",
        "voice_id": "en-US-AriaNeural"
    },
    "thorin": {
        "name": "Thorin",
        "type": "Ancient Wizard",
        "traits": "Wise, speaks in ancient tongues, mysterious, powerful",
        "emoji": "🔮",
        "voice_rate": 75,
        "voice_pitch": 0.5,
        "voice_volume": 0.7,
        "voice_style": "ancient_mystical",
        "voice_accent": "arcane",
        "speech_pattern": "ancient_wise",
        "voice_engine": "male_ancient",
        "voice_id": "en-US-BrianNeural"
    },
    "zara": {
        "name": "Zara",
        "type": "Fierce Warrior",
        "traits": "Bold, confident, speaks with passion, battle-hardened",
        "emoji": "⚔️",
        "voice_rate": 160,
        "voice_pitch": 1.2,
        "voice_volume": 0.95,
        "voice_style": "fierce_passionate",
        "voice_accent": "warrior",
        "speech_pattern": "bold_confident",
        "voice_engine": "female_strong",
        "voice_id": "en-US-SaraNeural"
    },
    "merlin": {
        "name": "Merlin",
        "type": "Mischievous Trickster",
        "traits": "Playful, witty, loves jokes, unpredictable",
        "emoji": "🎭",
        "voice_rate": 180,
        "voice_pitch": 1.5,
        "voice_volume": 0.9,
        "voice_style": "playful_mischievous",
        "voice_accent": "trickster",
        "speech_pattern": "quick_witty",
        "voice_engine": "male_playful",
        "voice_id": "en-US-RyanNeural"
    },
    "seraphina": {
        "name": "Seraphina",
        "type": "Elegant Noble",
        "traits": "Refined, sophisticated, speaks with grace, aristocratic",
        "emoji": "👑",
        "voice_rate": 140,
        "voice_pitch": 1.1,
        "voice_volume": 0.85,
        "voice_style": "elegant_refined",
        "voice_accent": "noble",
        "speech_pattern": "graceful_formal",
        "voice_engine": "female_elegant",
        "voice_id": "en-US-NaomiNeural"
    },
    "grommash": {
        "name": "Grommash",
        "type": "Barbarian Chief",
        "traits": "Fierce, loud, speaks with power, tribal leader",
        "emoji": "🪓",
        "voice_rate": 120,
        "voice_pitch": 0.4,
        "voice_volume": 1.0,
        "voice_style": "barbaric_powerful",
        "voice_accent": "tribal",
        "speech_pattern": "loud_authoritative",
        "voice_engine": "male_powerful",
        "voice_id": "en-US-EricNeural"
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

@app.route('/api/voices')
def get_voices():
    """Get available voice engines and voice information"""
    voice_engines = {
        "male_deep": {
            "name": "Deep Male Voice",
            "description": "Deep, authoritative male voice",
            "examples": ["en-US-DavisNeural", "en-US-GuyNeural"]
        },
        "female_cheerful": {
            "name": "Cheerful Female Voice", 
            "description": "Bright, energetic female voice",
            "examples": ["en-US-JennyNeural", "en-US-AriaNeural"]
        },
        "male_wise": {
            "name": "Wise Male Voice",
            "description": "Mature, thoughtful male voice", 
            "examples": ["en-US-TonyNeural", "en-US-BrianNeural"]
        },
        "male_authoritative": {
            "name": "Authoritative Male Voice",
            "description": "Commanding, military-style voice",
            "examples": ["en-US-GuyNeural", "en-US-EricNeural"]
        },
        "female_warm": {
            "name": "Warm Female Voice",
            "description": "Friendly, welcoming female voice",
            "examples": ["en-US-AriaNeural", "en-US-NaomiNeural"]
        },
        "male_ancient": {
            "name": "Ancient Male Voice", 
            "description": "Old, mystical male voice",
            "examples": ["en-US-BrianNeural", "en-US-TonyNeural"]
        },
        "female_strong": {
            "name": "Strong Female Voice",
            "description": "Powerful, confident female voice",
            "examples": ["en-US-SaraNeural", "en-US-JennyNeural"]
        },
        "male_playful": {
            "name": "Playful Male Voice",
            "description": "Fun, energetic male voice",
            "examples": ["en-US-RyanNeural", "en-US-DavisNeural"]
        },
        "female_elegant": {
            "name": "Elegant Female Voice",
            "description": "Refined, sophisticated female voice", 
            "examples": ["en-US-NaomiNeural", "en-US-AriaNeural"]
        },
        "male_powerful": {
            "name": "Powerful Male Voice",
            "description": "Strong, commanding male voice",
            "examples": ["en-US-EricNeural", "en-US-GuyNeural"]
        }
    }
    return jsonify(voice_engines)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 