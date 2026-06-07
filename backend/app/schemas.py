from pydantic import BaseModel, EmailStr
from typing import Optional, List


class SignupRequest(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ProductResponse(BaseModel):
    product_id: str
    name: str
    description: Optional[str]
    price: Optional[float]
    brand: Optional[str]
    category: Optional[str]
    subcategory: Optional[str]
    image_url: Optional[str]

    class Config:
        from_attributes = True


class SearchResponse(BaseModel):
    product: ProductResponse
    score: float


class OnboardingRequest(BaseModel):
    interests: str


class PurchaseRequest(BaseModel):
    product_id: str