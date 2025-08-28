from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.schemas import UserOut
from app.api.auth import get_current_user_id
from app import models

router = APIRouter()

@router.get("/me", response_model=UserOut)
def me(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    user = db.get(models.User, user_id)
    return user
