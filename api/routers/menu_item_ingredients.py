from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..schemas import menu_item_ingredients as menu_item_ingredient_schema
from ..dependencies.database import get_db
from ..controllers import menu_item_ingredients as menu_item_ingredient_controller

router = APIRouter(
    prefix="/menu-item-ingredients",
    tags=["Menu Item Ingredients"],
)


@router.post("/", response_model=menu_item_ingredient_schema.MenuItemIngredient, status_code=status.HTTP_201_CREATED)
def create_menu_item_ingredient(item_ingredient: menu_item_ingredient_schema.MenuItemIngredientCreate, db: Session = Depends(get_db)):
    return menu_item_ingredient_controller.create(db, item_ingredient)


@router.get("/", response_model=List[menu_item_ingredient_schema.MenuItemIngredient])
def list_menu_item_ingredients(db: Session = Depends(get_db)):
    return menu_item_ingredient_controller.read_all(db)


@router.get("/{menu_item_ingredient_id}", response_model=menu_item_ingredient_schema.MenuItemIngredient)
def get_menu_item_ingredient(menu_item_ingredient_id: int, db: Session = Depends(get_db)):
    item_ingredient = menu_item_ingredient_controller.read_by_id(db, menu_item_ingredient_id)
    if not item_ingredient:
        raise HTTPException(status_code=404, detail="Menu item ingredient not found")
    return item_ingredient


@router.put("/{menu_item_ingredient_id}", response_model=menu_item_ingredient_schema.MenuItemIngredient)
def update_menu_item_ingredient(menu_item_ingredient_id: int, item_ingredient_data: menu_item_ingredient_schema.MenuItemIngredientCreate, db: Session = Depends(get_db)):
    return menu_item_ingredient_controller.update(db, menu_item_ingredient_id, item_ingredient_data)


@router.delete("/{menu_item_ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_menu_item_ingredient(menu_item_ingredient_id: int, db: Session = Depends(get_db)):
    menu_item_ingredient_controller.delete(db, menu_item_ingredient_id)
    return {"detail": "Menu item ingredient deleted"}
