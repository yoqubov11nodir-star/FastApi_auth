from pydantic import BaseModel, Field, EmailStr
from typing import Optional 

class SignUpSchema(BaseModel):
    first_name: Optional[str] = None
    username: str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    username: str
    password: str