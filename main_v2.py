import os
import asyncio
from typing import Optional, Dict, Any, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator
from aiohttp import ClientSession, ClientError
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv('.env')

# --- Environment Configuration ---
API_KEY = os.getenv("GEMINI_API_KEY", "")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key="

# Rate limiting for free tier (15 requests/minute)
request_times = []
MAX_REQUESTS_PER_MINUTE = 15

# --- Example Dialogue Snippets for Few-Shot Prompting ---
FEW_SHOT_EXAMPLES = {
    "Cynical City Guard": [
        ("Player: Can I enter the city?", "Garrick: (sighs) Another one, huh? What's your business? Don't try anything funny."),
        ("Player: Nice weather today!", "Garrick: Weather's the least of my worries. Move along."),
    ],
    "Cheerful Shopkeeper": [
        ("Player: What do you sell?", "Elara: Oh, everything your heart desires! Take a look, and let me know if you need a recommendation!"),
        ("Player: How are you today?", "Elara: Absolutely wonderful! Every day is a gift, don't you think?"),
    ],
    "Mysterious Sage": [
        ("Player: Can you help me?", "Kaelen: The river flows where it must. Help comes to those who listen to the wind."),
        ("Player: What is the meaning of this symbol?", "Kaelen: Symbols are doors. Some open to truth, others to riddles. Which do you seek?"),
    ],
    "Gruff Blacksmith": [
        ("Player: Can you repair my sword?", "Drogun: Hmph. Let me see it. *examines blade* This'll take time. Come back tomorrow."),
        ("Player: How much for a new blade?", "Drogun: Quality costs. 50 gold for steel, 100 for enchanted. Take it or leave it."),
    ],
    "Enthusiastic Potion Seller": [
        ("Player: I need a healing potion", "Lira: Oh, you're in luck! I have the finest healing elixirs in the realm! Only 25 gold for the premium blend!"),
        ("Player: Do you have anything stronger?", "Lira: Stronger? My dear, I have potions that could bring a dragon back from the brink! *winks* For the right price, of course!"),
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

# --- Character Profile Parser ---
class CharacterProfile(BaseModel):
    name: str = Field(..., max_length=32)
    role: str = Field(..., max_length=64)
    traits: str = Field(..., max_length=256)
    backstory: Optional[str] = Field(default=None, max_length=512)
    scenario: Optional[str] = Field(default=None, max_length=512)

# --- Sample NPCs ---
sample_npcs = [
    CharacterProfile(
        name="Drogun",
        role="Gruff Blacksmith",
        traits="Gruff, impatient, values hard work, speaks in short sentences",
        backstory="Once a renowned warrior, now forges weapons for the worthy.",
        scenario="The player approaches Drogun's forge, seeking a weapon."
    ),
    CharacterProfile(
        name="Lira",
        role="Enthusiastic Potion Seller",
        traits="Cheerful, talkative, always tries to upsell, uses lots of exclamations",
        backstory="Inherited the shop from her grandmother, loves helping adventurers.",
        scenario="The player enters Lira's shop, looking for a healing potion."
    ),
    CharacterProfile(
        name="Eldrin",
        role="Mysterious Forest Hermit",
        traits="Cryptic, wise, speaks in riddles, calm demeanor",
        backstory="Lives alone in the woods, rumored to know ancient secrets.",
        scenario="The player seeks Eldrin's advice about a strange artifact."
    ),
]

# --- FastAPI Application Instance ---
app = FastAPI(
    title="AI NPC Dialogue Generator (Phase 2)",
    description="A backend to generate character-consistent dialogue for NPCs with robust memory and security.",
    version="2.0.0"
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

# --- Gemini API Call with Async Retry ---
async def call_gemini_api_with_retry(prompt: str) -> Optional[Dict[str, Any]]:
    global request_times
    
    # Rate limiting: respect 15 requests/minute
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
        while retries < 3:  # Reduced retries for free tier
            try:
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                async with session.post(f"{API_URL}{API_KEY}", json=payload, timeout=15) as response:
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
        api_result = await call_gemini_api_with_retry(system_prompt)
        if not api_result:
            raise HTTPException(status_code=500, detail="Failed to get a response from the AI model after multiple retries.")
        candidate = api_result.get("candidates", [])[0]
        generated_text = candidate.get("content", {}).get("parts", [])[0].get("text", "")
        if not generated_text:
            raise HTTPException(status_code=500, detail="The AI model returned an empty response.")
        return GenerateResponse(npc=request.character_name, reply=generated_text.strip())
    except (IndexError, KeyError) as e:
        print(f"Error parsing API response: {e}")
        raise HTTPException(status_code=500, detail="Could not parse the AI model's response.")

# --- Additional Endpoints ---
@app.get("/")
async def root():
    return {"message": "AI NPC Dialogue Generator Phase 2", "version": "2.0.0"}

@app.get("/sample-npcs")
async def get_sample_npcs():
    """Get sample NPC profiles for testing"""
    return {"npcs": [npc.dict() for npc in sample_npcs]}

@app.get("/health")
async def health_check():
    """Health check endpoint with rate limit info"""
    current_time = time.time()
    recent_requests = len([t for t in request_times if current_time - t < 60])
    return {
        "status": "healthy", 
        "api_key_configured": bool(API_KEY),
        "rate_limit": {
            "requests_this_minute": recent_requests,
            "max_requests_per_minute": MAX_REQUESTS_PER_MINUTE,
            "remaining_requests": max(0, MAX_REQUESTS_PER_MINUTE - recent_requests)
        }
    }

# --- Test the prompt builder with sample NPCs ---
def test_prompt_builder():
    player_input = "Can I buy your best sword?"
    for npc in sample_npcs:
        prompt = build_system_prompt(GenerateRequest(
            character_name=npc.name,
            character_type=npc.role,
            traits=npc.traits,
            player_input=player_input
        ))
        print(f"\n--- Prompt for {npc.name} ---\n{prompt}\n")

if __name__ == "__main__":
    test_prompt_builder() 