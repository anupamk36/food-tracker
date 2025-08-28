from sqlalchemy.orm import Session
from app import models
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, email: str, password: str):
    hashed = pwd_context.hash(password)
    user = models.User(email=email, hashed_password=hashed)
    db.add(user); db.commit(); db.refresh(user)
    return user

def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)

def create_meal(db: Session, owner_id: int, image_path: str, notes: str | None = None):
    meal = models.Meal(owner_id=owner_id, image_path=image_path, notes=notes, status="processing")
    db.add(meal); db.commit(); db.refresh(meal)
    return meal

def update_meal_analysis(db: Session, meal_id: int, items: list, nutrition: dict, status: str = "done"):
    meal = db.query(models.Meal).get(meal_id)
    if not meal:
        return None
    meal.items = items
    meal.nutrition = nutrition
    meal.status = status
    db.add(meal); db.commit(); db.refresh(meal)
    return meal

def list_meals_for_user(db: Session, user_id: int, limit=100):
    return db.query(models.Meal).filter(models.Meal.owner_id == user_id).order_by(models.Meal.timestamp.desc()).limit(limit).all()

def get_meal(db: Session, meal_id: int):
    return db.query(models.Meal).get(meal_id)
