import os
from openai import OpenAI

# ✅ Explicitly get API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def build_icse_visual_prompt(question: str, grade: int) -> str:
    prompt = f"""
You are an ICSE textbook diagram designer.

Create an educational infographic diagram for:
Class {grade} ICSE syllabus.

Topic:
{question}

STRICT RULES:
- EXACT ICSE textbook style
- Clean white background
- Flat vector diagram
- Proper labels
- Clear arrows and flow
- No cartoons
- No decorative art
- No extra text
- Diagram must explain the topic fully
- Suitable for exam revision

Style:
- Simple colors (blue, green, yellow)
- Professional school textbook look
- High clarity

Return ONLY the image description prompt.
"""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )
        return response.output_text.strip()
    except Exception as e:
        print(f"❌ Prompt building failed: {str(e)}")
        raise
