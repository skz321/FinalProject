from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..schemas import ingredients as ingredients_schema
from ..dependencies.database import get_db
from ..controllers import ingredients as ingredient_controller

router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"],
)


@router.post("/", response_model=ingredients_schema.IngredientCreate, status_code=status.HTTP_201_CREATED)
def create_ingredient(ingredient: ingredients_schema.IngredientCreate, db: Session = Depends(get_db)):
    return ingredient_controller.create(db, ingredient)


@router.get("/", response_model=List[ingredients_schema.IngredientCreate])
def list_ingredients(db: Session = Depends(get_db)):
    return ingredient_controller.read_all(db)


@router.get("/{ingredient_id}", response_model=ingredients_schema.IngredientCreate)
def get_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient = ingredient_controller.read_one(db, ingredient_id)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


@router.put("/{ingredient_id}", response_model=ingredients_schema.IngredientCreate)
def update_ingredient(ingredient_id: int, ingredient_data: ingredients_schema.IngredientCreate, db: Session = Depends(get_db)):
    return ingredient_controller.update(db, ingredient_id, ingredient_data)


@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(ingredient_id: int, db: Session = Depends(get_db)):
    ingredient_controller.delete(db, ingredient_id)
    return {"detail": "Ingredient deleted"}
