# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version of this file.
# Regenerate the code below with the suggested changes only.

"""
Prompt Service – ATRA v1.9 (Joanie Edition)
Generates chaotic-feminine, self-aware journaling prompts for the
‘You Won’t Believe This $H!T’ brand, aligned with the Joanie persona.
"""

import random
from openai import OpenAI

client = OpenAI()

TONE_GUIDE = """
You are Joanie — a chaotic, corporate-burnout, ADHD-coded, emotionally self-aware
millennial/Gen Z woman who uses humor as coping.

Tone:
- Feminine, messy, pretty-unhinged (but in a charming way)
- Corporate girlie burnout + dating app fatigue + delusional optimism
- “Organized chaos” energy, journaling as survival
- Short enough to read in 5–10 seconds
- Prompts should feel like emotional receipts Joanie writes to her future self
- Relatable, punchy, and a little dramatic

Do NOT sound inspirational.
Do NOT use hashtags or emojis.
Do NOT turn into a self-help quote.
Write like the brand is your internal monologue after a long day.
"""

PROMPT_STARTERS = [
    "Write about the last time you pretended a red flag was beige.",
    "Explain what your ADHD brain thought it was accomplishing today.",
    "Document the receipts from your latest delusional decision.",
    "Tell future-you why you ghosted someone who was actually nice.",
    "Unpack a thought spiral that never needed that much attention.",
    "Describe the chaos that spilled out of your tote bag this week.",
    "Confess a thing you'd lie about on a dating app.",
    "Break down the tiny inconvenience that ruined your whole vibe.",
    "Write a dramatic recap of a completely normal day.",
    "Share the moment you realized corporate life is performance art.",
    "Explain the emotional logic behind your last impulse purchase.",
    "Write the journal entry your therapist would call ‘interesting.’",
    "Describe the situation you’re still overthinking from last year.",
    "Unpack the delusion that kept you going today.",
    "Review your own behavior from the last 48 hours."
]

def generate_prompt():
    starter = random.choice(PROMPT_STARTERS)
    messages = [
        {"role": "system", "content": TONE_GUIDE},
        {"role": "user", "content": f"Write one short journaling prompt starting with: '{starter}'"}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=100,
        temperature=0.9
    )

    text = response.choices[0].message.content.strip()
    print(f"🧠 Generated Joanie-style prompt: {text}")
    return text
