import os
from openai import OpenAI
import json

# ✅ Explicitly get API key from environment
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_study_json(question: str, grade: int) -> dict:
    prompt = f"""
You are an API that returns ONLY JSON.

Role:
You are an experienced ICSE school teacher.

Task:
Convert the topic into a study-friendly format for Class {grade} ICSE students.

STRICT RULES:
- Use very simple English
- Do NOT add extra information
- Keep it exam-oriented
- Do NOT use markdown
- Do NOT add explanations
- Output MUST be valid JSON only
- Do NOT add any text before or after JSON

JSON FORMAT (must match exactly):
{{
  "title": "string",
  "simple_explanation": ["string"],
  "keywords": ["string"],
  "exam_points": ["string"],
  "memory_trick": "string"
}}

Topic:
{question}
"""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        raw = response.output_text.strip()

        if not raw:
            raise ValueError("Empty JSON response")

        return json.loads(raw)
    except Exception as e:
        print(f"❌ Study JSON generation failed: {str(e)}")
        raise
