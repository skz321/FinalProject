from pydantic import BaseModel

class IngredientBase(BaseModel):
    name: str
    quantity: float

class IngredientCreate(IngredientBase):
    pass

class Ingredient(IngredientBase):
    id: int

    class Config:
        from_attributes = True
