"""
Prompt Service
Generates witty, chaotic, journal-selling ad prompts for 'You Won’t Believe This $H!T'.
"""

from openai import OpenAI
import os
import random

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SCENES = [
    "realizing your horoscope was right for all the wrong reasons",
    "apologizing to your barista for trauma-dumping again",
    "overthinking a text you haven’t even sent yet",
    "celebrating a small win like it’s a Grammy",
    "convincing yourself that scrolling counts as self-care",
    "telling your therapist you’re fine while clearly not fine",
    "finding clarity halfway through a nervous breakdown",
    "pretending Mercury retrograde explains your entire personality",
]

def generate_prompt() -> str:
    """Generate a short, ad-style micro scene that sells journaling as cathartic humor."""
    scene = random.choice(SCENES)
    instruction = f"""
    Write one clever, funny, ad-style caption promoting the journal
    'You Won’t Believe This $H!T'. Describe {scene} with wit and modern chaos energy.
    It should sound like a social post that makes people laugh and think “yeah, same.”
    End with a playful journaling nudge like “yeah, write that down,” “document the chaos,”
    or “the journal won’t fill itself.” Max 3 sentences.
    """

    response = client.responses.create(model="gpt-4.1-mini", input=instruction)
    return response.output_text.strip()

