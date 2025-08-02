from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..models import ingredients as model_ingredient
from ..schemas import ingredients as schema_ingredient
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, ingredient: schema_ingredient.IngredientCreate):
    new_ingredient = model_ingredient.Ingredient(**ingredient.model_dump())
    try:
        db.add(new_ingredient)
        db.commit()
        db.refresh(new_ingredient)
        return new_ingredient
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def read_all(db: Session):
    return db.query(model_ingredient.Ingredient).all()


def read_one(db: Session, ingredient_id: int):
    ingredient = db.query(model_ingredient.Ingredient).filter_by(id=ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient


def update(db: Session, ingredient_id: int, update_data: schema_ingredient.IngredientCreate):
    ingredient = db.query(model_ingredient.Ingredient).filter_by(id=ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    for key, value in update_data.dict().items():
        setattr(ingredient, key, value)

    db.commit()
    db.refresh(ingredient)
    return ingredient


def delete(db: Session, ingredient_id: int):
    ingredient = db.query(model_ingredient.Ingredient).filter_by(id=ingredient_id).first()
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    db.delete(ingredient)
    db.commit()
    return {"message": "Ingredient deleted"}
