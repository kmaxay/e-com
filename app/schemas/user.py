from pydantic import BaseModel, validator
from typing import Optional
import re

class UserBase(BaseModel):
    phone_number: str
    username: Optional[str] = None
    full_name: Optional[str] = None

    @validator('phone_number')
    def validate_phone_number(cls, v):
        # Basic international phone validation
        if not re.match(r'^\+?[1-9]\d{1,14}$', v.replace(" ", "")):
            raise ValueError('Invalid phone number format')
        return v

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    phone_number: str
    password: str

class UserResponse(BaseModel):
    id: str
    phone_number: str
    username: Optional[str]
    full_name: Optional[str]
    is_active: bool

class User(UserResponse):
    hashed_password: str