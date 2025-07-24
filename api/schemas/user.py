from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    name: str
    email: str
    phone_number: Optional[str] = None
    address: Optional[str] = None

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class ConfigDict:
        from_attributes = True