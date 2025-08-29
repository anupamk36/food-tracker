from fastapi import APIRouter, Depends, UploadFile, File, Form, BackgroundTasks, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import text
from pathlib import Path
import os, uuid, shutil, json

from app.db import get_db
from app import crud
from app.schemas import MealOut, MealsList
from app.auth_lib import decode_token
from app.services.openai_client import analyze_food_image_text  # <-- your analyzer (returns items/nutrition)
# If you renamed/moved it, just point to the correct function.

router = APIRouter()
security = HTTPBearer()
UPLOAD_DIR = Path(os.environ.get("UPLOAD_DIR", "uploads"))
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    if not credentials or not credentials.credentials:
        raise HTTPException(status_code=403, detail="Not authenticated")
    payload = decode_token(credentials.credentials)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload["sub"])

@router.post("/", response_model=MealOut)
async def create_meal(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id),
    file: UploadFile | None = File(default=None),
    notes: str | None = Form(default=None),
    items: str | None = Form(default=None),       # JSON string (optional)
    nutrition: str | None = Form(default=None),   # JSON string (optional)
):
    # 1) Save the image if provided
    image_path = None
    local_path = None
    if file is not None:
        ext = Path(file.filename or "").suffix.lower() or ".jpg"
        dest_name = f"{uuid.uuid4().hex}{ext}"
        dest_path = UPLOAD_DIR / dest_name
        with dest_path.open("wb") as out:
            shutil.copyfileobj(file.file, out)
        image_path = f"/uploads/{dest_name}"
        local_path = str(dest_path)

    # 2) Parse optional json strings
    items_obj = None
    nutrition_obj = None
    try:
        if items:
            items_obj = json.loads(items)
        if nutrition:
            nutrition_obj = json.loads(nutrition)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in 'items' or 'nutrition'")

    # 3) Create the meal row
    status = "done" if nutrition_obj is not None else "pending"
    meal = crud.create_meal(
        db,
        owner_id=user_id,
        image_path=image_path,
        notes=notes,
        items=items_obj,
        nutrition=nutrition_obj,
        status=status,
    )

    # 4) If we already have nutrition, return immediately
    if nutrition_obj is not None:
        return meal

    # 5) Otherwise analyze in the background and update the same row
    async def analyze_and_update(mid: int, img_path: str | None):
        db2 = next(get_db())
        try:
            items_result = None
            nutrition_result = None

            if img_path:
                # EXPECTED RETURN SHAPES:
                #  a) {"items":[...], "nutrition": {...}}
                #  b) {"items":[...]}  (then keep nutrition None)
                #  c) [{"name":...}, ...] (items list only)
                result = await analyze_food_image_text(img_path)

                # normalize
                if isinstance(result, dict):
                    items_result = result.get("items")
                    nutrition_result = result.get("nutrition")
                elif isinstance(result, list):
                    items_result = result
                else:
                    items_result = None
                    nutrition_result = None

            # mark done if we got anything useful; else failed
            new_status = "done" if (items_result is not None and nutrition_result is not None) else "failed"
            crud.update_meal_analysis(db2, mid, items_result, nutrition_result, status=new_status)
        except Exception as e:
            # if analysis explodes, mark failed (so it doesn't sit as pending forever)
            try:
                crud.update_meal_analysis(db2, mid, None, None, status="failed")
            except Exception:
                pass
            print(f"[meals.analyze_and_update] error for {mid}: {type(e).__name__}: {e}")
        finally:
            db2.close()

    background_tasks.add_task(analyze_and_update, meal.id, local_path)
    return meal

@router.get("/", response_model=MealsList)
def list_my_meals(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    meals = crud.list_meals(db, owner_id=user_id)
    return {"items": meals}

@router.get("/stats")
def get_stats(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    # ... keep the scalar-safe queries we added earlier ...
    day_rows = db.execute(text("""
        SELECT
          DATE(timestamp) AS date,
          SUM(COALESCE( (CASE WHEN jsonb_typeof(nutrition)='object' THEN (nutrition->>'calories')::numeric ELSE 0 END), 0))::float  AS calories,
          SUM(COALESCE( (CASE WHEN jsonb_typeof(nutrition)='object' THEN (nutrition->>'protein_g')::numeric ELSE 0 END), 0))::float AS protein_g,
          SUM(COALESCE( (CASE WHEN jsonb_typeof(nutrition)='object' THEN (nutrition->>'carbs_g')::numeric  ELSE 0 END), 0))::float AS carbs_g,
          SUM(COALESCE( (CASE WHEN jsonb_typeof(nutrition)='object' THEN (nutrition->>'fat_g')::numeric    ELSE 0 END), 0))::float AS fat_g
        FROM meals
        WHERE owner_id = :uid
        GROUP BY 1
        ORDER BY 1
    """), {"uid": user_id}).mappings().all()

    series = [dict(r) for r in day_rows]

    top_rows = db.execute(text("""
        SELECT
          LOWER(elem->>'name') AS name,
          COUNT(*)::int AS count
        FROM meals m
        CROSS JOIN LATERAL jsonb_array_elements(
          CASE WHEN jsonb_typeof(m.items)='array' THEN m.items ELSE '[]'::jsonb END
        ) AS elem
        WHERE m.owner_id = :uid
        GROUP BY 1
        ORDER BY count DESC, name ASC
        LIMIT 10
    """), {"uid": user_id}).mappings().all()

    top_items = [dict(r) for r in top_rows]
    return {"series": series, "topItems": top_items}
