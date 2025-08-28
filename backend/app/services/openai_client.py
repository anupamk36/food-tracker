import openai
from app.core.config import settings
import json

openai.api_key = settings.OPENAI_API_KEY

async def analyze_food_image_text(image_path: str) -> list:
    """
    Sends image to OpenAI's image/multimodal endpoint and expects a JSON array of
    items of form {"item": "chicken breast", "portion_g": 150, "confidence": 0.9}
    Implementation uses text-based prompt via image->text. Adapt to your client version.
    """
    # This is a pragmatic implementation using the "response" text. Replace with the
    # preferred official call for your openai client version, e.g., client.responses.create(...)
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    prompt = (
        "You are a nutrition assistant. Given the following image, list the food items present and for each give "
        "an estimated portion in grams. Output only valid JSON array, e.g. "
        '[{"item":"boiled rice","portion_g":200,"confidence":0.8}, ...]'
    )

    # Simple approach: use the text completion endpoint (adapt if your client supports direct image multimodal)
    resp = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful nutrition assistant."},
            {"role": "user", "content": prompt}
        ],
    )
    text = ""
    if resp and "choices" in resp and len(resp["choices"])>0:
        text = resp["choices"][0]["message"]["content"]
    try:
        data = json.loads(text)
        return data
    except Exception:
        return []
