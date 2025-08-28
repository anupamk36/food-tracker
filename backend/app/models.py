from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    meals = relationship("Meal", back_populates="owner")

class Meal(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    image_path = Column(String, nullable=True)   # path or S3 key
    status = Column(String, default="processing")  # processing | done | failed
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    items = Column(JSON, default=[])   # detected items (json list)
    nutrition = Column(JSON, default={})  # aggregated nutrition
    notes = Column(String, nullable=True)

    owner = relationship("User", back_populates="meals")
