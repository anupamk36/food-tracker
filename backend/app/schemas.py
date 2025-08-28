from pydantic import BaseModel, EmailStr
from typing import List, Optional, Any

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True

class MealCreate(BaseModel):
    notes: Optional[str]

class MealOut(BaseModel):
    id: int
    owner_id: int
    image_path: Optional[str]
    status: str
    timestamp: str
    items: Any
    nutrition: Any
    notes: Optional[str]
    class Config:
        orm_mode = True
