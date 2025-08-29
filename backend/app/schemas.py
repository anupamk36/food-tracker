from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, Any, List, Dict
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

class MealBase(BaseModel):
    id: int
    owner_id: int
    image_path: Optional[str] = None
    status: str
    timestamp: datetime
    items: Optional[List[Dict[str, Any]]] = None
    nutrition: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True

class MealOut(MealBase):
    pass

class MealsList(BaseModel):
    items: List[MealOut]
