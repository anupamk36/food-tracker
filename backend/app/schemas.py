from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, Any, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None

class TokenData(BaseModel):
    sub: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    email: EmailStr

class MealCreate(BaseModel):
    notes: Optional[str] = None

class MealOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    owner_id: int
    image_path: Optional[str]
    status: str
    timestamp: datetime
    items: Any | None = None
    nutrition: Any | None = None
    notes: Optional[str] = None

class MealsList(BaseModel):
    items: List[MealOut]
