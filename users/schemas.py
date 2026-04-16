from pydantic import BaseModel, Field
from typing import Optional 

class SignUpSchema(BaseModel):
    first_name : Optional[str]
    username : str
    email : str
    password : str

    class Config:
        from_attributes = True
        json_schema_extra = {
            'example': {
                'first_name': 'Nodir',
                'username': 'nodir',
                'email': 'nodir@gmail.com',
                'password': 'pass123'
            }
        }