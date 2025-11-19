"""
Prompt Service – ATRA v1.9
Generates witty, chaotic, Gen Z–centric journaling prompts that promote
'You Won’t Believe This $H!T' through humor, self-awareness, and relatable absurdity.
"""

import random
from openai import OpenAI

client = OpenAI()

TONE_GUIDE = """
You are Greg — a Gen Z ad exec who writes witty micro-prompts for social posts
promoting the chaotic journaling brand *You Won’t Believe This $H!T*.

Tone:
- Funny, self-aware, slightly unhinged
- Reflective yet playful (like if therapy had memes)
- Short, readable in under 10 seconds
- Each prompt must make the reader laugh, nod, or feel seen
- Always tie chaos → journaling as the outlet (directly or subtly)

Do NOT sound like an ad.
No hashtags. No emojis.
Write as if the brand is your inner monologue turned printable.
"""

PROMPT_STARTERS = [
    "When your brain is buffering but life’s in 4K…",
    "Therapy’s great, but have you tried talking to your journal instead?",
    "If overthinking was cardio, I’d have abs by now.",
    "The chaos is free; the journaling is optional, but recommended.",
    "My intrusive thoughts just applied for creative direction.",
    "Somehow, Mercury’s in retrograde *and* so am I.",
    "We’re calling it ‘self-reflection,’ but it’s really just a recap of bad decisions.",
    "Another episode of ‘Who Approved My Life Choices?’ just dropped.",
    "If my mind had pop-up ads, today’s would say: ‘Write it down before you combust.’",
    "Chaos called. I answered with a pen."
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
    print(f"🧠 Generated witty chaos prompt: {text}")
    return text

