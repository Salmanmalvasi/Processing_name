#!/usr/bin/env python3
"""
Web Interface for AI NPC Dialogue Generator
Simple Flask-based chatbot with character and model selection
"""

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Available characters
CHARACTERS = {
    "drogun": {
        "name": "Drogun",
        "type": "Gruff Blacksmith",
        "traits": "Gruff, impatient, values hard work, speaks in short sentences",
        "description": "A grumpy blacksmith who values hard work",
        "emoji": "🗡️"
    },
    "lira": {
        "name": "Lira",
        "type": "Enthusiastic Potion Seller",
        "traits": "Cheerful, talkative, always tries to upsell, uses lots of exclamations",
        "description": "A cheerful potion seller who loves to upsell",
        "emoji": "🧪"
    },
    "eldrin": {
        "name": "Eldrin",
        "type": "Mysterious Forest Hermit",
        "traits": "Cryptic, wise, speaks in riddles, calm demeanor",
        "description": "A mysterious hermit who speaks in riddles",
        "emoji": "🌲"
    },
    "garrick": {
        "name": "Garrick",
        "type": "Cynical City Guard",
        "traits": "Suspicious, direct, doesn't trust easily, speaks with authority",
        "description": "A cynical city guard who's suspicious of everyone",
        "emoji": "🛡️"
    },
    "elara": {
        "name": "Elara",
        "type": "Cheerful Shopkeeper",
        "traits": "Friendly, helpful, loves to chat, always positive",
        "description": "A friendly shopkeeper who loves to chat",
        "emoji": "🏪"
    }
}

# Available models
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
    """Main page with chatbot interface"""
    return render_template('index.html', characters=CHARACTERS, models=MODELS)

@app.route('/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        character_key = data.get('character', 'drogun')
        model = data.get('model', 'llama3-8b-8192')
        
        if not message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get character info
        character = CHARACTERS.get(character_key, CHARACTERS['drogun'])
        
        # Prepare payload for API
        payload = {
            "character_name": character["name"],
            "character_type": character["type"],
            "traits": character["traits"],
            "player_input": message,
            "model": model
        }
        
        # Call the API
        response = requests.post(
            "http://127.0.0.1:8002/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            reply = result.get('reply', 'No response')
            return jsonify({
                'reply': reply,
                'character': character['name'],
                'model': model
            })
        else:
            return jsonify({'error': f'API Error: {response.status_code}'}), 500
            
    except Exception as e:
        return jsonify({'error': f'Server Error: {str(e)}'}), 500

@app.route('/api/status')
def status():
    """Check API status"""
    try:
        response = requests.get("http://127.0.0.1:8002/health", timeout=5)
        if response.status_code == 200:
            return jsonify({'status': 'online', 'data': response.json()})
        else:
            return jsonify({'status': 'error', 'message': f'HTTP {response.status_code}'})
    except Exception as e:
        return jsonify({'status': 'offline', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080) 