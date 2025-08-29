from sqlalchemy.orm import Session
from sqlalchemy import select
from app import models
from typing import Optional, Any, Dict, List

def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.execute(select(models.User).where(models.User.email == email)).scalar_one_or_none()

def create_user(db: Session, email: str, password_hash: str) -> models.User:
    user = models.User(email=email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def create_meal(
    db: Session,
    owner_id: int,
    image_path: str | None,
    notes: str | None,
    items: List[Dict[str, Any]] | None = None,
    nutrition: Dict[str, Any] | None = None,
    status: str = "pending",
) -> models.Meal:
    meal = models.Meal(
        owner_id=owner_id,
        image_path=image_path,
        notes=notes,
        items=items,
        nutrition=nutrition,
        status=status,
    )
    db.add(meal)
    db.commit()
    db.refresh(meal)
    return meal

# app/crud.py
def update_meal_analysis(db: Session, meal_id: int, items, nutrition, status: str = "done"):
    meal = db.get(models.Meal, meal_id)
    if not meal:
        return None
    if items is not None:
        meal.items = items           # <-- list of dicts, not json.dumps
    if nutrition is not None:
        meal.nutrition = nutrition   # <-- dict, not json.dumps
    meal.status = status
    db.commit()
    db.refresh(meal)
    return meal



def get_meal(db: Session, meal_id: int) -> Optional[models.Meal]:
    return db.get(models.Meal, meal_id)

def list_meals(db: Session, owner_id: int) -> List[models.Meal]:
    return (
        db.execute(
            select(models.Meal)
            .where(models.Meal.owner_id == owner_id)
            .order_by(models.Meal.timestamp.desc())
        ).scalars().all()
    )
