from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Settings(BaseModel):
    authjwt_secret_key: str = "aa682e49c01fd1ce4dd9b6ad55d5af936a5aca3c37ab19c24f16aff557e910bd"

class SignUpSchema(BaseModel):
    user_name: str
    first_name: Optional[str] = None 
    email: str
    password: str

class LoginSchema(BaseModel):
    user_name: str
    password: str

class UpdateUser(BaseModel):
    user_name: Optional[str] = None
    first_name: Optional[str] = None
    email: Optional[str] = None

class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

class CartCreate(BaseModel):
    product_name: str
    quantity: int
    price: float

class OrderResponse(BaseModel):
    id: int
    total_price: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class OrderStatusUpdate(BaseModel):
    status: str