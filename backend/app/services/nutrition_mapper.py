# Minimal nutrition mapping. In prod, use USDA or Nutritionix dataset.
NUTRITION_DB = {
    "boiled rice": {"calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3},
    "chicken breast": {"calories": 165, "protein": 31, "carbs": 0, "fat": 3.6},
    "salad": {"calories": 20, "protein": 1, "carbs": 4, "fat": 0.2},
    "bread": {"calories": 265, "protein": 9, "carbs": 49, "fat": 3.2},
}

def map_items_to_nutrition(items):
    aggregated = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
    mapped = []
    for it in items:
        name = it.get("item", "").lower()
        portion = it.get("portion_g") or it.get("portion") or 100
        canon = name.strip().lower()
        # naive lookup: exact match then best-effort
        row = NUTRITION_DB.get(canon)
        if not row:
            # try tokenization
            for k in NUTRITION_DB.keys():
                if k in canon or canon in k:
                    row = NUTRITION_DB[k]
                    break
        if not row:
            mapped.append({**it, "mapped": False})
            continue
        factor = float(portion) / 100.0
        for k, v in row.items():
            aggregated[k] += v * factor
        mapped.append({**it, "mapped": True, "nutrition_per_100g": row})
    return aggregated, mapped
