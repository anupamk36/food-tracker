from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    meals = relationship("Meal", back_populates="owner")

class Meal(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    image_path = Column(Text, nullable=True)
    status = Column(String(50), default="pending", nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    items = Column(JSONB, nullable=True)
    nutrition = Column(JSONB, nullable=True)
    notes = Column(Text, nullable=True)

    owner = relationship("User", back_populates="meals")