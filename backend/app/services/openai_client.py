import os, base64, json, asyncio
from app.core.config import settings
from openai import OpenAI

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY') or settings.openai_api_key

async def analyze_food_image_text(local_path: str):
    """Send image to OpenAI and request a structured nutrition analysis.
    Returns a list of detected items (name, serving) or raises an exception.
    This function uses the OpenAI chat/completions endpoint and asks the model
    to return JSON. If OPENAI_API_KEY is not set, this falls back to a dummy response.
    """
    if not OPENAI_API_KEY:
        # fallback: return dummy items
        return [
            {"name": "Grilled Chicken", "serving": "150g"},
            {"name": "Steamed Rice", "serving": "1 cup"},
            {"name": "Broccoli", "serving": "1 cup"}
        ]

    client = OpenAI(api_key=OPENAI_API_KEY)

    # Read and encode image
    with open(local_path, 'rb') as f:
        img_bytes = f.read()
    b64 = base64.b64encode(img_bytes).decode('ascii')
    data_url = f"data:image/jpeg;base64,{b64}"

    system = "You are an assistant that extracts food items and nutrition facts from images. Respond with valid JSON only, for example: {'items':[{'name':'Chicken','serving':'150g'}]}"
    user = ("Analyze the food in the provided image. Return a JSON object with a top-level key 'items' which is a list of objects with 'name' and 'serving'.\n"
            "Also include a top-level 'nutrition' object with calories, protein_g, carbs_g, fat_g when possible.\n"
            "Only return JSON.\n")
    # Build a prompt with the image as a data URL
    messages = [
        {"role": "system", "content": system},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": user},
                {"type": "image_url", "image_url": {"url": data_url}},
            ],
        },
    ]

    # Use ChatCompletion
    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",  # change to desired model
            messages=messages,
            max_tokens=800,
            temperature=0.0,
        )
        print("Response from the OpenAI API:", resp)
        text = resp.choices[0].message.content
    except Exception as e:
        raise e

    # parse JSON from model output
    try:
        parsed = json.loads(text)
        # ensure items list present
        items = parsed.get('items', [])
        return items if items is not None else []
    except Exception:
        # attempt to extract JSON fragment from text
        import re
        m = re.search(r'\{.*\}', text, flags=re.S)
        if m:
            try:
                parsed = json.loads(m.group(0))
                return parsed.get('items', [])
            except Exception:
                pass
    # if parsing fails, return empty list
    return []
