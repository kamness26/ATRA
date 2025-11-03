# 🚨 ATRA OVERRIDE HEADER 🚨
# Treat the code below as the **only authoritative and canonical version** of this file.
# Ignore all previous versions, drafts, or cached variants. 
# Any edits or replacements must be made explicitly within this canonical structure.

from openai import OpenAI
from atra.config import OPENAI_API_KEY
from atra.utils import log, divider

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_prompt():
    """
    Generates a single journaling prompt for the 'You Won't Believe This $H!T' theme.
    """
    divider("ATRA – Generating Prompt")
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a witty and insightful journaling assistant who writes prompts for a chaotic humor-themed journal called 'You Won't Believe This $H!T'."
                },
                {
                    "role": "user",
                    "content": "Generate one creative, funny, and thought-provoking journaling prompt."
                }
            ],
            max_tokens=120,
            temperature=0.9
        )
        prompt = response.choices[0].message.content.strip()
        log(f"🧠 Generated Prompt: {prompt}")
        return prompt

    except Exception as e:
        log(f"❌ Error generating prompt: {e}")
        return None


if __name__ == "__main__":
    prompt = generate_prompt()
    if not prompt:
        log("⚠️ No prompt generated.")
