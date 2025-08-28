from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.api.v1.auth import get_current_user_id
from app import crud

router = APIRouter()

@router.get("/me")
def me(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    user = crud.get_user_by_email(db, None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "email": user.email}
