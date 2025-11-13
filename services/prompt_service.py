"""
Prompt Service
Generates specific, brand-aligned prompts for ATRA.
"""

from openai import OpenAI
import os
import random

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define brand tone + categories
CATEGORIES = [
    "absurd daily chaos",
    "funny life advice",
    "modern burnout confessions",
    "unexpected moments of peace",
    "ironic motivational poster",
]

def generate_prompt() -> str:
    """Generate a witty, vivid prompt aligned with You Won’t Believe This $H!T."""
    category = random.choice(CATEGORIES)
    instruction = f"Write a vivid, short creative prompt in the style of dark humor and daily absurdity, themed around {category}. Make it specific enough that it could inspire an image for a journal post."
    
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=instruction
    )
    
    prompt = response.output_text.strip()
    return prompt

