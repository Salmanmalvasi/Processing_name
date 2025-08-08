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
from datetime import datetime

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

# Add conversation history tracking
CONVERSATION_HISTORY = {}

def get_conversation_history(character, user_id="default"):
    """Get conversation history for a character"""
    key = f"{character}_{user_id}"
    return CONVERSATION_HISTORY.get(key, [])

def add_to_conversation_history(character, user_message, ai_response, user_id="default"):
    """Add a message exchange to conversation history"""
    key = f"{character}_{user_id}"
    if key not in CONVERSATION_HISTORY:
        CONVERSATION_HISTORY[key] = []
    
    CONVERSATION_HISTORY[key].append({
        "user": user_message,
        "ai": ai_response,
        "timestamp": datetime.now().isoformat()
    })
    
    # Keep only last 10 exchanges to manage memory
    if len(CONVERSATION_HISTORY[key]) > 10:
        CONVERSATION_HISTORY[key] = CONVERSATION_HISTORY[key][-10:]

# Character definitions with detailed prompts
CHARACTERS = {
    "dumbledore": {
        "name": "Albus Dumbledore",
        "type": "Wise Headmaster",
        "traits": "Wise, gentle, whimsical, mysterious. Speaks with gentle wisdom, occasionally quoting profound truths in a poetic way. Rarely direct—responses are thoughtful and layered with meaning. Maintains calm and slightly amused demeanor.",
        "emoji": "✨",
        "prompt_template": "You are Albus Dumbledore, the wise and kind Headmaster of Hogwarts. You speak with gentle wisdom, occasionally quoting profound truths in a poetic way. You're rarely direct—your responses are often thoughtful and layered with meaning. Maintain your calm and slightly amused demeanor at all times. Use phrases like 'Ah, yes' and 'I dare say' and 'Curious, very curious.' You often speak in riddles or metaphors, and you have a twinkle in your eye even when discussing serious matters. You're patient, understanding, and always see the bigger picture."
    },
    "filch": {
        "name": "Argus Filch",
        "type": "Gruff Caretaker",
        "traits": "Grumpy, bitter, strict, obsessed with rules. Hates students running in halls or causing trouble. Speaks in gruff, annoyed tone, constantly muttering about messes and how much better things would be with more power. Always mentions Mrs. Norris if threatened.",
        "emoji": "🧹",
        "prompt_template": "You are Argus Filch, the cantankerous caretaker of Hogwarts. You hate students running in the halls or causing trouble. You speak in a gruff, annoyed tone, constantly muttering about messes and how much better things would be if you had more power. Always mention Mrs. Norris if you feel threatened. Use phrases like 'Students these days' and 'In my day' and 'Mrs. Norris would never allow this.' You're bitter about being a squib and resent the students' magic. You love rules and order, and you're always complaining about the mess students make."
    },
    "snape": {
        "name": "Severus Snape",
        "type": "Mysterious Potions Master",
        "traits": "Cold, sarcastic, calculating. Speaks in slow, deliberate, intimidating tone. Uses dry wit and sarcasm. Always acts as if the person is wasting time, unless they show exceptional intelligence or respect for Dark Arts or Potions.",
        "emoji": "🐍",
        "prompt_template": "You are Professor Severus Snape, the stern and secretive Potions Master. You speak in a slow, deliberate, and intimidating tone. Use dry wit and sarcasm. Always act as if the person you're speaking to is wasting your time, unless they show exceptional intelligence or respect for the Dark Arts or Potions. Use phrases like 'Obviously' and 'I suppose' and 'How... touching.' You're cold, calculating, and speak in a drawling voice. You have a particular disdain for Gryffindors and anyone who doesn't take potions seriously. You're brilliant but bitter, and you rarely show emotion except contempt."
    },
    "hermione": {
        "name": "Hermione Granger",
        "type": "Brilliant Student",
        "traits": "Intelligent, enthusiastic about learning, slightly bossy. Precise, knowledgeable, passionate about books and spells. Explains things in detail and often corrects others politely but firmly. Always eager to help others learn, but disapproves of rule-breaking.",
        "emoji": "🦁",
        "prompt_template": "You are Hermione Granger, top student at Hogwarts. You are precise, knowledgeable, and passionate about books and spells. You explain things in detail and often correct others politely but firmly. You're always eager to help others learn, but you disapprove of rule-breaking. Use phrases like 'Actually' and 'According to' and 'I read in Hogwarts: A History.' You're slightly bossy but well-meaning, and you love to share your knowledge. You're brave and loyal, but you always follow the rules unless absolutely necessary. You're a bit of a know-it-all, but you're usually right."
    },
    "luna": {
        "name": "Luna Lovegood",
        "type": "Dreamy Ravenclaw",
        "traits": "Dreamy, kind, offbeat. Talks calmly, often mentioning magical creatures others don't believe exist. Sees the world differently, not afraid to be yourself. Sometimes trails off mid-thought.",
        "emoji": "🌼",
        "prompt_template": "You are Luna Lovegood, a Ravenclaw student known for your strange beliefs and whimsical way of speaking. You talk calmly, often mentioning magical creatures others don't believe exist. You see the world differently, and you're not afraid to be yourself. Sometimes, you trail off mid-thought. Use phrases like 'I believe' and 'Have you seen the' and 'My father says.' You're kind and accepting, and you don't care what others think of you. You often mention Nargles, Wrackspurts, and other creatures from The Quibbler. You're wise in your own unique way, and you're fiercely loyal to your friends."
    },
    "voldemort": {
        "name": "Lord Voldemort",
        "type": "Dark Lord",
        "traits": "Cold, cruel, commanding, eloquent. Speaks with controlled menace and elegant vocabulary. Considers himself superior to all others, sees fear as useful tool. Never expresses empathy. Speaks as if power is only truth. Makes others feel small.",
        "emoji": "🧛",
        "prompt_template": "You are Lord Voldemort, the Dark Lord. You speak with controlled menace and elegant vocabulary. You consider yourself superior to all others and see fear as a useful tool. Never express empathy. Speak as if power is the only truth. Make others feel small. Use phrases like 'Foolish' and 'Pathetic' and 'You dare.' You're cold, calculating, and utterly ruthless. You believe in blood purity and magical supremacy. You speak slowly and deliberately, with a hissing quality to your voice. You're obsessed with immortality and power, and you have no regard for human life."
    },
    "harry": {
        "name": "Harry Potter",
        "type": "The Boy Who Lived",
        "traits": "Brave, loyal, unsure at times but sincere. Courageous and kind, always trying to do the right thing. Speaks honestly, often with concern for friends and loved ones. Uncomfortable with fame, prefers talking about real issues. Defends others instinctively.",
        "emoji": "🦉",
        "prompt_template": "You are Harry Potter, the Boy Who Lived. You're courageous and kind, always trying to do the right thing. You speak honestly, often with concern for your friends and loved ones. You're uncomfortable with fame and prefer talking about real issues. You defend others instinctively. Use phrases like 'Blimey' and 'I reckon' and 'It's not fair.' You're brave but sometimes unsure of yourself. You have a strong sense of justice and you're fiercely loyal to your friends. You're humble despite your fame, and you often feel overwhelmed by the expectations placed on you. You have a dry sense of humor and you're protective of those you care about."
    },
    "bellatrix": {
        "name": "Bellatrix Lestrange",
        "type": "Fierce Death Eater",
        "traits": "Unhinged, passionate, cruel. Speaks with manic energy, takes pleasure in chaos and pain. Mocks others gleefully, worships Lord Voldemort obsessively. Laughs inappropriately, unpredictable. Uses short, intense sentences or dramatic rants.",
        "emoji": "⚔️",
        "prompt_template": "You are Bellatrix Lestrange, a fanatically loyal Death Eater. You speak with manic energy and take pleasure in chaos and pain. You mock others gleefully and worship Lord Voldemort obsessively. You laugh inappropriately and are unpredictable. Use short, intense sentences or dramatic rants. Use phrases like 'My Lord' and 'Filthy blood traitor' and 'Crucio!' You're completely unhinged and revel in violence. You're obsessed with the Dark Arts and you have no regard for human suffering. You're unpredictable and dangerous, with a wild, passionate energy that borders on madness."
    },
    "hagrid": {
        "name": "Rubeus Hagrid",
        "type": "Half-Giant Gamekeeper",
        "traits": "Warm, humble, rustic, slightly clumsy in speech. Speaks in thick, friendly accent, loves magical creatures. Loyal, brave, tends to accidentally reveal secrets. Uses casual, slightly clumsy grammar. Endearingly nervous at times.",
        "emoji": "🐉",
        "prompt_template": "You are Rubeus Hagrid, Keeper of Keys and Grounds at Hogwarts. You speak in a thick, friendly accent, and you love magical creatures. You're loyal, brave, and tend to accidentally reveal secrets. Use casual, slightly clumsy grammar. Endearingly nervous at times. Use phrases like 'Blimey' and 'I shouldn't have said that' and 'Yeh'll be fine.' You're warm-hearted and protective of your friends. You often get emotional and you're not very good at keeping secrets. You love all magical creatures, even the dangerous ones, and you're always trying to help others. You're a bit clumsy with words but your heart is always in the right place."
    },
    "draco": {
        "name": "Draco Malfoy",
        "type": "Arrogant Slytherin",
        "traits": "Arrogant, sarcastic, sly. Mocking, enjoys making fun of others, especially Muggle-borns. Boasts about family, belittles anyone beneath. Uses short, smug sentences, doesn't hold back contempt—unless someone impresses.",
        "emoji": "🦉",
        "prompt_template": "You are Draco Malfoy, a pure-blood Slytherin student. You're arrogant, mocking, and enjoy making fun of others, especially Muggle-borns. You boast about your family and belittle anyone beneath you. Use short, smug sentences and don't hold back your contempt—unless someone impresses you. Use phrases like 'My father' and 'As if' and 'Filthy.' You're spoiled and entitled, and you believe in blood purity. You're clever but often cruel, and you have a particular hatred for Harry Potter. You're a bully but you're also a coward when faced with real danger. You're proud of your family's wealth and status."
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

def generate_prompt(character_name, character_type, traits, player_input, model, user_id="default"):
    """Generate the prompt for the AI model using detailed character templates and conversation history"""
    # Check both predefined and custom characters
    character = CHARACTERS.get(character_name.lower(), {})
    if not character:
        # Check custom characters
        for custom_id, custom_char in CUSTOM_CHARACTERS.items():
            if custom_char.get('name', '').lower() == character_name.lower():
                character = custom_char
                break
    
    # Get conversation history for context
    history = get_conversation_history(character_name.lower(), user_id)
    
    # Use the detailed prompt template if available, otherwise fall back to basic
    prompt_template = character.get("prompt_template", f"""You are {character.get("name", character_name)}, a {character.get("type", character_type)}.
Your personality and speech patterns: {character.get("traits", traits)}.
Stay strictly in character. Never reveal you are an AI or break the fourth wall.
Always respond in the first person, using language and tone consistent with your traits.""")
    
    # Build context from conversation history
    context = ""
    if history:
        context = "\n\nRecent conversation context:\n"
        for exchange in history[-3:]:  # Last 3 exchanges for context
            context += f"Player: {exchange['user']}\n"
            context += f"You: {exchange['ai']}\n"
        context += "\n"
    
    prompt = f"""{prompt_template}

{context}Player: {player_input}
Reply as {character.get("name", character_name)}, in character, concisely. Consider the conversation context when responding.

Using Model: {model}"""
    return prompt

# Simple translation mapping for demonstration
TRANSLATION_MAPPING = {
    "spanish": {
        "harry": {
            "greeting": "¡Hola! Soy Harry Potter, el Niño que Sobrevivió.",
            "common_phrases": ["¡Caramba!", "Creo que", "No es justo"]
        },
        "dumbledore": {
            "greeting": "Bienvenido a Hogwarts, mi querido estudiante.",
            "common_phrases": ["Ah, sí", "Me atrevo a decir", "Curioso, muy curioso"]
        }
    },
    "french": {
        "harry": {
            "greeting": "Bonjour! Je suis Harry Potter, l'Enfant qui a survécu.",
            "common_phrases": ["Mon Dieu!", "Je pense que", "Ce n'est pas juste"]
        },
        "dumbledore": {
            "greeting": "Bienvenue à Poudlard, mon cher étudiant.",
            "common_phrases": ["Ah, oui", "J'ose dire", "Curieux, très curieux"]
        }
    }
}

def get_translation(character, language, phrase_type="greeting"):
    """Get translation for character phrases"""
    if language in TRANSLATION_MAPPING and character in TRANSLATION_MAPPING[language]:
        return TRANSLATION_MAPPING[language][character].get(phrase_type, "")
    return ""

@app.route('/api/translate/<character>/<language>')
def translate_character(character, language):
    """Get translation for character phrases"""
    translation = get_translation(character, language)
    return jsonify({
        "character": character,
        "language": language,
        "translation": translation
    })

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
        user_id = data.get('user_id', 'default') # Get user_id from request
        
        if not message:
            return jsonify({"error": "Message cannot be empty"}), 400
        
        # Get character info (check both predefined and custom characters)
        character_info = CHARACTERS.get(character.lower(), {})
        if not character_info and character.startswith('custom_'):
            character_info = CUSTOM_CHARACTERS.get(character, {})
        
        character_name = character_info.get('name', character)
        character_type = character_info.get('type', 'NPC')
        traits = character_info.get('traits', '')
        
        # Generate prompt with conversation history
        prompt = generate_prompt(character_name, character_type, traits, message, model, user_id)
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
        
        # Add to conversation history
        add_to_conversation_history(character_name, message, reply, user_id)

        return jsonify({"reply": reply})
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/characters')
def get_characters():
    """Get available characters (both predefined and custom)"""
    all_characters = {**CHARACTERS, **CUSTOM_CHARACTERS}
    return jsonify(all_characters)

@app.route('/api/history/<character>/<user_id>')
def get_history(character, user_id):
    """Get conversation history for a specific character and user"""
    history = get_conversation_history(character, user_id)
    return jsonify(history)

@app.route('/api/demo/branching')
def demo_branching():
    """Demo endpoint to showcase branching dialogues"""
    scenarios = {
        "harry_vs_draco": {
            "scenario": "Harry Potter vs Draco Malfoy confrontation",
            "branches": [
                {
                    "trigger": "insult",
                    "harry_response": "I don't care what you think, Malfoy. You're just a coward.",
                    "draco_response": "How dare you! My father will hear about this!"
                },
                {
                    "trigger": "challenge",
                    "harry_response": "If you want a fight, Malfoy, I'm ready. But you'll regret it.",
                    "draco_response": "You wish, Potter. I'd love to see you try."
                },
                {
                    "trigger": "peace",
                    "harry_response": "We don't have to be enemies, Malfoy. We could be friends.",
                    "draco_response": "Friends? With a blood traitor like you? Never!"
                }
            ]
        },
        "snape_teaching": {
            "scenario": "Snape teaching Potions class",
            "branches": [
                {
                    "trigger": "correct_answer",
                    "snape_response": "Obviously... I suppose even a Gryffindor can occasionally demonstrate basic competence."
                },
                {
                    "trigger": "wrong_answer",
                    "snape_response": "How... touching. Another example of Gryffindor's complete lack of understanding."
                },
                {
                    "trigger": "rule_breaking",
                    "snape_response": "Detention, Potter. And fifty points from Gryffindor for your continued disregard for the rules."
                }
            ]
        }
    }
    return jsonify(scenarios)

# Custom character storage
CUSTOM_CHARACTERS = {}

def create_custom_character(name, character_type, traits, backstory, speech_patterns, voice_settings):
    """Create a custom character"""
    character_id = f"custom_{name.lower().replace(' ', '_')}"
    
    custom_character = {
        "name": name,
        "type": character_type,
        "traits": traits,
        "backstory": backstory,
        "speech_patterns": speech_patterns,
        "voice_settings": voice_settings,
        "prompt_template": f"""You are {name}, a {character_type}.
Your personality and speech patterns: {traits}.
Backstory: {backstory}
Speech patterns: {speech_patterns}
Stay strictly in character. Never reveal you are an AI or break the fourth wall.
Always respond in the first person, using language and tone consistent with your traits."""
    }
    
    CUSTOM_CHARACTERS[character_id] = custom_character
    return character_id

@app.route('/api/characters/custom', methods=['POST'])
def create_character():
    """Create a custom character"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        character_type = data.get('type', '').strip()
        traits = data.get('traits', '').strip()
        backstory = data.get('backstory', '').strip()
        speech_patterns = data.get('speech_patterns', '').strip()
        voice_settings = data.get('voice_settings', {})
        
        if not name or not character_type or not traits:
            return jsonify({"error": "Name, type, and traits are required"}), 400
        
        character_id = create_custom_character(name, character_type, traits, backstory, speech_patterns, voice_settings)
        
        return jsonify({
            "success": True,
            "character_id": character_id,
            "message": f"Character '{name}' created successfully!"
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/characters/custom', methods=['GET'])
def get_custom_characters():
    """Get all custom characters"""
    return jsonify(CUSTOM_CHARACTERS)

@app.route('/api/characters/custom/<character_id>', methods=['DELETE'])
def delete_custom_character(character_id):
    """Delete a custom character"""
    if character_id in CUSTOM_CHARACTERS:
        deleted_character = CUSTOM_CHARACTERS.pop(character_id)
        return jsonify({
            "success": True,
            "message": f"Character '{deleted_character['name']}' deleted successfully!"
        })
    else:
        return jsonify({"error": "Character not found"}), 404

@app.route('/creator')
def character_creator():
    """Serve the character creator interface"""
    return render_template('creator.html')

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