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

def create_meal(db: Session, owner_id: int, image_path: str | None, notes: str | None) -> models.Meal:
    meal = models.Meal(owner_id=owner_id, image_path=image_path, notes=notes, status="pending")
    db.add(meal)
    db.commit()
    db.refresh(meal)
    return meal

def update_meal_analysis(db: Session, meal_id: int, items: List[Dict[str, Any]], nutrition: Dict[str, Any], status: str = "done"):
    meal = db.get(models.Meal, meal_id)
    if not meal:
        return None
    meal.items = items
    meal.nutrition = nutrition
    meal.status = status
    db.commit()
    db.refresh(meal)
    return meal

def get_meal(db: Session, meal_id: int) -> Optional[models.Meal]:
    return db.get(models.Meal, meal_id)

def list_meals(db: Session, owner_id: int):
    return db.execute(select(models.Meal).where(models.Meal.owner_id == owner_id).order_by(models.Meal.timestamp.desc())).scalars().all()
