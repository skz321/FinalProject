from pydantic import BaseModel
from typing import Optional

class MenuItemBase(BaseModel):
    name: str
    price: float
    calories: Optional[float] = None
    category: Optional[str] = None


class MenuItemCreate(MenuItemBase):
    pass

class MenuItem(MenuItemBase):
    id: int

    class ConfigDict:
        from_attributes = True
