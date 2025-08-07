def build_prompt(name, type, traits, message):
    """
    Build a prompt for the Gemini model to generate dialogue as the specified NPC.
    """
    prompt = f"""
You are roleplaying as an NPC in a game.

Character Profile:
- Name: {name}
- Type: {type}
- Traits: {traits}

Stay in character and reply to the player below in a way that fits the NPC's personality, background, and speaking style.

Player: {message}
NPC ({name}):
"""
    return prompt