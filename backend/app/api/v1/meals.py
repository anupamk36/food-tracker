from fastapi import APIRouter, Depends, UploadFile, File, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app import crud
from app.schemas import MealOut
from app.utils.storage import save_file_local, upload_to_s3
from app.core.config import settings
from app.services.openai_client import analyze_food_image_text
from app.services.nutrition_mapper import map_items_to_nutrition
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth import decode_token

router = APIRouter()
security = HTTPBearer()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    return int(payload.get("sub"))

@router.post("/", response_model=MealOut)
async def upload_meal(background_tasks: BackgroundTasks,
                      file: UploadFile = File(...),
                      notes: str | None = None,
                      db: Session = Depends(get_db),
                      user_id: int = Depends(get_current_user_id)):
    # save file locally
    filename = f"{user_id}_{int(__import__('time').time())}_{file.filename}"
    local_path = save_file_local(file.file, filename)
    image_ref = local_path
    if settings.S3_ENABLED:
        key = f"users/{user_id}/{filename}"
        image_ref = upload_to_s3(local_path, key)

    meal = crud.create_meal(db, owner_id=user_id, image_path=image_ref, notes=notes)

    # schedule background analysis
    background_tasks.add_task(process_meal_analysis, meal.id, local_path)

    return crud.get_meal(db, meal.id)

def process_meal_analysis(meal_id: int, local_path: str):
    # synchronous worker (background thread)
    from app.db import SessionLocal
    db = SessionLocal()
    try:
        items = __import__('asyncio').get_event_loop().run_until_complete(analyze_food_image_text(local_path))
        nutrition, mapped_items = map_items_to_nutrition(items)
        crud.update_meal_analysis(db, meal_id, mapped_items, nutrition, status="done")
    except Exception as e:
        crud.update_meal_analysis(db, meal_id, [], {}, status="failed")
    finally:
        db.close()
