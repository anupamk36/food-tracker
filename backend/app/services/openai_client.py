# app/services/openai_client.py
import json
import re
from typing import Any, Dict, List, Optional, Tuple

from openai import OpenAI
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

_JSON_BLOCK_RE = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)

def _parse_json_from_text(text: str) -> Optional[Dict[str, Any]]:
    """
    Accepts raw assistant text. Tries to extract JSON, including:
      - full content is JSON
      - JSON inside ```json ... ```
      - minor trailing punctuation/whitespace
    Returns dict or None.
    """
    if not text:
        return None

    # Try code-fence first
    m = _JSON_BLOCK_RE.search(text)
    if m:
        snippet = m.group(1).strip()
        try:
            return json.loads(snippet)
        except json.JSONDecodeError:
            pass

    # Try whole content as JSON
    s = text.strip()
    # trim any leading/trailing backticks
    s = s.strip("`")
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        return None

def _normalize_items_nutrition(obj: Any) -> Tuple[Optional[List[Dict[str, Any]]], Optional[Dict[str, Any]]]:
    """
    Accepts various shapes and normalizes to (items, nutrition).
      - {"items":[...], "nutrition": {...}}
      - {"items":[...]}  (nutrition None)
      - [{"name":...}, ...]  (items only)
      - string content with JSON → parsed
    """
    # If it’s a string, try parse
    if isinstance(obj, str):
        parsed = _parse_json_from_text(obj)
        if parsed is not None:
            return _normalize_items_nutrition(parsed)
        return None, None

    # If it’s already a dict with keys
    if isinstance(obj, dict):
        items = obj.get("items")
        nutrition = obj.get("nutrition")
        # items might be a dict in bad generations; coerce to list if so
        if isinstance(items, dict):
            items = [items]
        if items is not None and not isinstance(items, list):
            items = None
        if nutrition is not None and not isinstance(nutrition, dict):
            nutrition = None
        return items, nutrition

    # If it’s a list, assume it's the items list
    if isinstance(obj, list):
        return obj, None

    return None, None

async def analyze_food_image_text(local_path: str) -> Dict[str, Any]:
    """
    Returns a dict with keys:
      { "items": [...], "nutrition": {...} }
    If the model returns only one of them, the missing key will be absent.
    """
    # You may already be sending the image; leaving the exact call as-is is fine.
    # The key point is: parse the assistant message content.

    # EXAMPLE: using text-only instruction with an image URL/file you uploaded earlier.
    # Replace this with your existing call if you already handle the image upload to OpenAI storage.
    resp = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a nutrition extractor. Reply ONLY with minified JSON matching:\n"
                    '{"items":[{"name":"string","serving":"string"}],'
                    '"nutrition":{"calories":number,"protein_g":number,"carbs_g":number,"fat_g":number}}'
                ),
            },
            {
                "role": "user",
                "content": f"Analyze this meal image at local path (for context only): {local_path}",
            },
        ],
        temperature=0.2,
    )

    # ---- robust parsing of assistant content ----
    msg = resp.choices[0].message
    content_text = getattr(msg, "content", None)

    items, nutrition = _normalize_items_nutrition(content_text)

    # If still empty, try to see if SDK object was directly returned somehow
    if items is None and nutrition is None:
        # users sometimes print resp dict-like; try to parse again from str
        try:
            as_text = str(content_text)
            items, nutrition = _normalize_items_nutrition(as_text)
        except Exception:
            pass

    result: Dict[str, Any] = {}
    if items is not None:
        result["items"] = items
    if nutrition is not None:
        result["nutrition"] = nutrition
    return result
