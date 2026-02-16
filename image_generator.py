from openai import OpenAI
import base64
import os

client = OpenAI()

def generate_icse_infographic(image_prompt: str, output_path: str):
    result = client.images.generate(
        model="gpt-image-1",
        prompt=image_prompt,
        size="1024x1024"
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(image_bytes)

    print("✅ ICSE Infographic Generated:", output_path)
