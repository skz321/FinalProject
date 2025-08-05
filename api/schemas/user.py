from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str
    password: str
    phone_number: Optional[str] = None
    address: Optional[str] = None
    order_type_preference: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class ConfigDict:
        from_attributes = True