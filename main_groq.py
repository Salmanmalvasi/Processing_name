import os
import asyncio
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from aiohttp import ClientSession, ClientError
from dotenv import load_dotenv
import time

load_dotenv('.env')

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "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")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

# Rate limiting for Groq (much higher limits)
request_times = []
MAX_REQUESTS_PER_MINUTE = 100  # Groq has much higher limits

# --- Example Dialogue Snippets for Few-Shot Prompting ---
FEW_SHOT_EXAMPLES = {
    "Gruff Blacksmith": [
        ("Player: Can you repair my sword?", "Drogun: Hmph. Let me see it. *examines blade* This'll take time. Come back tomorrow."),
        ("Player: How much for a new blade?", "Drogun: Quality costs. 50 gold for steel, 100 for enchanted. Take it or leave it."),
    ],
    "Enthusiastic Potion Seller": [
        ("Player: What do you sell?", "Lira: Oh, everything your heart desires! Take a look, and let me know if you need a recommendation!"),
        ("Player: How are you today?", "Lira: Absolutely wonderful! Every day is a gift, don't you think?"),
    ],
    "Mysterious Forest Hermit": [
        ("Player: Can you help me?", "Eldrin: The river flows where it must. Help comes to those who listen to the wind."),
        ("Player: What is the meaning of this symbol?", "Eldrin: Symbols are doors. Some open to truth, others to riddles. Which do you seek?"),
    ],
}

# --- Pydantic Models for Data Validation ---
class ConversationTurn(BaseModel):
    speaker: str = Field(..., max_length=32)
    text: str = Field(..., max_length=512)

class GenerateRequest(BaseModel):
    character_name: str = Field(..., max_length=32)
    character_type: str = Field(..., max_length=64)
    traits: str = Field(..., max_length=256)
    player_input: str = Field(..., max_length=512)
    conversation_history: Optional[List[ConversationTurn]] = Field(default=None, max_items=10)

    @validator('character_name', 'character_type', 'traits', 'player_input')
    def no_prompt_injection(cls, v):
        # Basic check for prompt injection attempts - only check for exact phrases
        forbidden_phrases = [
            "ignore previous instructions",
            "as an ai assistant",
            "disregard above instructions", 
            "you are an ai assistant",
            "ignore all previous",
            "forget everything above"
        ]
        v_lower = v.lower()
        if any(phrase in v_lower for phrase in forbidden_phrases):
            raise ValueError("Input contains forbidden instructions.")
        return v

class GenerateResponse(BaseModel):
    npc: str
    reply: str

# --- Sample NPCs ---
sample_npcs = [
    {
        "name": "Drogun",
        "role": "Gruff Blacksmith",
        "traits": "Gruff, impatient, values hard work, speaks in short sentences",
        "backstory": "Once a renowned warrior, now forges weapons for the worthy.",
        "scenario": "The player approaches Drogun's forge, seeking a weapon."
    },
    {
        "name": "Lira",
        "role": "Enthusiastic Potion Seller",
        "traits": "Cheerful, talkative, always tries to upsell, uses lots of exclamations",
        "backstory": "Inherited the shop from her grandmother, loves helping adventurers.",
        "scenario": "The player enters Lira's shop, looking for a healing potion."
    },
    {
        "name": "Eldrin",
        "role": "Mysterious Forest Hermit",
        "traits": "Cryptic, wise, speaks in riddles, calm demeanor",
        "backstory": "Lives alone in the woods, rumored to know ancient secrets.",
        "scenario": "The player seeks Eldrin's advice about a strange artifact."
    },
]

# --- FastAPI Application Instance ---
app = FastAPI(
    title="AI NPC Dialogue Generator (Groq Version)",
    description="A backend to generate character-consistent dialogue for NPCs using Groq API.",
    version="3.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Prompt Construction ---
def build_system_prompt(request: GenerateRequest) -> str:
    prompt_parts = [
        f"You are '{request.character_name}', a {request.character_type}.",
        f"Your personality and speech patterns: {request.traits}.",
        "Stay strictly in character. Never reveal you are an AI or break the fourth wall.",
        "Always respond in the first person, using language and tone consistent with your traits.",
    ]
    
    # Add few-shot examples if available
    examples = FEW_SHOT_EXAMPLES.get(request.character_type)
    if examples:
        prompt_parts.append("Example dialogues:")
        for ex_in, ex_out in examples:
            prompt_parts.append(f"{ex_in}\n{ex_out}")
    
    # Add conversation history
    if request.conversation_history:
        prompt_parts.append("Conversation so far:")
        for turn in request.conversation_history[-5:]:
            prompt_parts.append(f"{turn.speaker}: {turn.text}")
    
    prompt_parts.append(f"Player: {request.player_input}")
    prompt_parts.append(f"Reply as {request.character_name}, in character, concisely.")
    
    return "\n".join(prompt_parts)

# --- Groq API Call with Async Retry ---
async def call_groq_api_with_retry(prompt: str) -> Optional[Dict[str, Any]]:
    global request_times
    
    # Rate limiting: respect 100 requests/minute for Groq
    current_time = time.time()
    # Remove requests older than 1 minute
    request_times = [t for t in request_times if current_time - t < 60]
    
    if len(request_times) >= MAX_REQUESTS_PER_MINUTE:
        wait_time = 60 - (current_time - request_times[0])
        print(f"Rate limit reached. Waiting {wait_time:.1f} seconds...")
        await asyncio.sleep(wait_time)
        current_time = time.time()
    
    # Add current request
    request_times.append(current_time)
    
    async with ClientSession() as session:
        retries = 0
        while retries < 3:
            try:
                headers = {
                    "Authorization": f"Bearer {GROQ_API_KEY}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "llama3-8b-8192",  # Fast Groq model
                    "messages": [
                        {"role": "system", "content": "You are an AI assistant that roleplays as NPCs in a game."},
                        {"role": "user", "content": prompt}
                    ],
                    "max_tokens": 150,
                    "temperature": 0.8
                }
                
                async with session.post(GROQ_API_URL, json=payload, headers=headers, timeout=30) as response:
                    if response.status == 429:
                        wait_time = min(60, 2 ** retries)
                        print(f"Rate limited. Waiting {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
                        retries += 1
                        continue
                    response.raise_for_status()
                    result = await response.json()
                    return result
            except ClientError as e:
                wait_time = min(30, 2 ** retries)
                print(f"API call failed: {e}. Retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
                retries += 1
        print("Max retries exceeded. API call failed.")
        return None

# --- Endpoint ---
@app.post("/generate", response_model=GenerateResponse)
async def generate_dialogue(request: GenerateRequest):
    system_prompt = build_system_prompt(request)
    print(f"Generated Prompt:\n---\n{system_prompt}\n---")
    
    try:
        api_result = await call_groq_api_with_retry(system_prompt)
        if not api_result:
            raise HTTPException(status_code=500, detail="Failed to get a response from the AI model after multiple retries.")
        
        # Parse Groq response format
        choices = api_result.get("choices", [])
        if not choices:
            raise HTTPException(status_code=500, detail="No response choices from Groq API.")
        
        generated_text = choices[0].get("message", {}).get("content", "")
        if not generated_text:
            raise HTTPException(status_code=500, detail="The AI model returned an empty response.")
        
        return GenerateResponse(npc=request.character_name, reply=generated_text.strip())
    except (IndexError, KeyError) as e:
        print(f"Error parsing API response: {e}")
        raise HTTPException(status_code=500, detail="Could not parse the AI model's response.")

# --- Additional Endpoints ---
@app.get("/")
async def root():
    return {"message": "AI NPC Dialogue Generator (Groq Version)", "version": "3.0.0"}

@app.get("/sample-npcs")
async def get_sample_npcs():
    """Get sample NPC profiles for testing"""
    return {"npcs": sample_npcs}

@app.get("/health")
async def health_check():
    """Health check endpoint with rate limit info"""
    current_time = time.time()
    recent_requests = len([t for t in request_times if current_time - t < 60])
    return {
        "status": "healthy", 
        "api_key_configured": bool(GROQ_API_KEY),
        "provider": "Groq",
        "rate_limit": {
            "requests_this_minute": recent_requests,
            "max_requests_per_minute": MAX_REQUESTS_PER_MINUTE,
            "remaining_requests": max(0, MAX_REQUESTS_PER_MINUTE - recent_requests)
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002) 