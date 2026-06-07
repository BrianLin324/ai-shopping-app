from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)
    price = Column(Float)
    brand = Column(String)
    category = Column(String, index=True)
    subcategory = Column(String)
    category_path = Column(String)
    type = Column(String)
    image_url = Column(String)
    embedding = Column(Text, nullable=True)


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(String, nullable=True)
    query = Column(Text, nullable=True)
    activity_type = Column(String, nullable=False)  # search, view, purchase, onboarding
    created_at = Column(DateTime, default=datetime.utcnow)