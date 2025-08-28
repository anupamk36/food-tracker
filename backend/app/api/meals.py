from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import crud
from app.schemas import MealOut, MealsList
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth_lib import decode_token
from app.services.openai_client import analyze_food_image_text
from app.services.nutrition_mapper import map_items_to_nutrition
import time, os

router = APIRouter()
security = HTTPBearer()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> int:
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload.get("sub"))

UPLOAD_DIR = "/data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=MealOut)
async def upload_meal(background_tasks: BackgroundTasks,
                      file: UploadFile = File(...),
                      notes: str | None = None,
                      db: Session = Depends(get_db),
                      user_id: int = Depends(get_current_user_id)):
    filename = f"{user_id}_{int(time.time())}_{file.filename}"
    local_path = os.path.join(UPLOAD_DIR, filename)
    with open(local_path, "wb") as out:
        out.write(await file.read())

    meal = crud.create_meal(db, owner_id=user_id, image_path=local_path, notes=notes)
    background_tasks.add_task(process_meal_analysis, meal.id, local_path)
    return crud.get_meal(db, meal.id)

def process_meal_analysis(meal_id: int, local_path: str):
    from app.db import SessionLocal
    db = SessionLocal()
    try:
        import asyncio
        items = asyncio.get_event_loop().run_until_complete(analyze_food_image_text(local_path))
        nutrition, mapped = map_items_to_nutrition(items)
        crud.update_meal_analysis(db, meal_id, mapped, nutrition, status="done")
    except Exception as e:
        crud.update_meal_analysis(db, meal_id, [], {}, status="failed")
    finally:
        db.close()

@router.get("/", response_model=MealsList)
def list_my_meals(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    meals = crud.list_meals(db, owner_id=user_id)
    return {"items": meals}
