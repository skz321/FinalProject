from pydantic import BaseModel

class MenuItemIngredientBase(BaseModel):
    menu_item_id: int
    ingredient_id: int
    required_quantity: float

class MenuItemIngredientCreate(MenuItemIngredientBase):
    pass

class MenuItemIngredient(MenuItemIngredientBase):
    id: int

    class Config:
        from_attributes = True
