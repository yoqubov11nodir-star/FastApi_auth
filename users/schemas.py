from pydantic import BaseModel, EmailStr
from typing import Optional

class SignUpSchema(BaseModel):
    user_name: str
    first_name: Optional[str] = None 
    email: str
    password: str

    model_config = {                   
        "from_attributes": True,      
        "json_schema_extra": {         
            "example": {
                "user_name": "nodir_swe",
                "first_name": "Nodir",
                "email": "nodir@example.com",
                "password": "password123"
            }
        }
    }


class LoginSchema(BaseModel):
    user_name: str
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "user_name": "nodir_swe",
                "password": "password123"
            }
        }
    }


class Settings(BaseModel):
    authjwt_secret_key: str = "aa682e49c01fd1ce4dd9b6ad55d5af936a5aca3c37ab19c24f16aff557e910bd"


class UpdateUser(BaseModel):
    user_name: Optional[str]
    first_name: Optional[str] = None
    email: Optional[str]
    password: Optional[str]


class PasswordUpdate(BaseModel):
    old_password:str
    new_password:str
    confirm_password:str
    

class CartCreate(BaseModel):
    product_name: str
    quantity: int
    price: float

class OrderResponse(BaseModel):
    id: int
    total_price: float
    status: str

    class Config:
        from_attributes = True