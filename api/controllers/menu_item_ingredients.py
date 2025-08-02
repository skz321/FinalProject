from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models import menu_item_ingredients as model_link
from ..schemas import menu_item_ingredients as schema_link
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, link: schema_link.MenuItemIngredientCreate):
    new_link = model_link.MenuItemIngredient(**link.dict())
    try:
        db.add(new_link)
        db.commit()
        db.refresh(new_link)
        return new_link
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))


def read_all(db: Session):
    return db.query(model_link.MenuItemIngredient).all()


def read_by_menu_item(db: Session, menu_item_id: int):
    return db.query(model_link.MenuItemIngredient).filter_by(menu_item_id=menu_item_id).all()


def read_by_id(db: Session, link_id: int):
    link = db.query(model_link.MenuItemIngredient).filter_by(id=link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    return link


def update(db: Session, link_id: int, update_data: schema_link.MenuItemIngredientCreate):
    link = db.query(model_link.MenuItemIngredient).filter_by(id=link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    for key, value in update_data.dict().items():
        setattr(link, key, value)

    db.commit()
    db.refresh(link)
    return link


def delete(db: Session, link_id: int):
    link = db.query(model_link.MenuItemIngredient).filter_by(id=link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    db.delete(link)
    db.commit()
    return {"message": "Link deleted"}
