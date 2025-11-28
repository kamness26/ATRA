# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the only authoritative and canonical version of this file.
# Regenerated for Phase 1: Joanie Personality Modes (Mixed Explicitness)

"""
Prompt Service – ATRA (Joanie Edition v2.0)

Generates journaling prompts influenced by Joanie’s five emotional modes:
- corporate_burnout (explicit)
- adhd_spiral (implicit)
- delusional_romantic (implicit)
- existentially_exhausted (implicit)
- sunday_scaries (explicit)
"""

import random
from openai import OpenAI

client = OpenAI()

# Explicit-mode intros
EXPLICIT_PREFIX = {
    "corporate_burnout": "In full corporate burnout mode, ",
    "sunday_scaries": "With the Sunday Scaries creeping in, ",
}

# Implicit seeds for mixed-mode influence
IMPLICIT_SEEDS = {
    "adhd_spiral": [
        "Write about the thought that sprinted through your brain for no reason today.",
        "Journal the mental side quest that derailed your whole afternoon.",
        "Describe a moment where your brain chose chaos instead of logic.",
        "Write about something tiny that your mind turned into a whole event.",
    ],
    "delusional_romantic": [
        "Explain the entirely fictional relationship you formed from one glance.",
        "Write a poetic recap of your latest delusional crush moment.",
        "Document the red flag you rebranded as ‘quirky.’",
        "Describe the rom-com scene your brain staged today without permission.",
    ],
    "existentially_exhausted": [
        "Write about the moment today where you questioned your entire existence for no reason.",
        "Describe a tiny moment that made you spiral into deep thoughts.",
        "Journal the feeling of being emotionally logged out but still functioning.",
        "Write about a time today when everything felt a little too… cosmic.",
    ],
}

# Explicit-mode seed lists
EXPLICIT_SEEDS = {
    "corporate_burnout": [
        "write about the meeting today that should’ve been an email.",
        "describe the task that drained 80% of your soul.",
        "journal the moment you pretended to care on a Zoom call.",
        "write about the micro-rage that kept you awake last night.",
    ],
    "sunday_scaries": [
        "write about the dread lurking in the back of your mind.",
        "describe why Monday already feels like a threat.",
        "journal the thing you’re avoiding for no real reason.",
        "write about the self-negotiation you’re doing to get through tonight.",
    ],
}


def generate_prompt(mode: str) -> str:
    """
    Generate a single Joanie-coded journaling prompt based on mood.
    Mixed explicitness:
    - some moods referenced directly
    - others influence tone/seed implicitly
    """
    # Explicit modes (corporate_burnout, sunday_scaries)
    if mode in EXPLICIT_PREFIX:
        prefix = EXPLICIT_PREFIX[mode]
        seed = random.choice(EXPLICIT_SEEDS[mode])
        starter = f"{prefix}{seed}"
    else:
        # Implicit modes (ADHD, romantic delusion, existential exhaustion)
        starter = random.choice(IMPLICIT_SEEDS[mode])

    system_prompt = f"""
    You are Joanie — a chaotic, self-aware, feminine narrator writing
    journaling prompts for 'You Won’t Believe This $H!T'.

    Mode: {mode}

    Guidelines:
    - Short, punchy, personal, emotional, very human.
    - Tone intensity depends on mode:
        * corporate_burnout → drier, sarcastic
        * adhd_spiral → frantic, racing thoughts, playful
        * delusional_romantic → dreamy, dramatic, almost poetic
        * existentially_exhausted → weary, cosmic, overthinking
        * sunday_scaries → dread mixed with humor
    - NO hashtags. NO emojis. NO inspirational quotes.
    - Must read like something Joanie would actually journal.
    - Max length: ~22 words.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": starter},
        ],
        temperature=0.9,
        max_tokens=60,
    )

    text = response.choices[0].message.content.strip()
    print(f"🧠 Generated Joanie prompt ({mode}): {text}")
    return text
