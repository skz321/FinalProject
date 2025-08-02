from sqlalchemy.orm import Session
from fastapi import Response, status, HTTPException
from ..models import menu_items as models
from ..schemas import menu_items as schemas
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, item: schemas.MenuItemCreate):
    new_item = models.MenuItem(
        name=item.name,
        price=item.price,
        calories=item.calories,
        category=item.category,
        amount_in_stock = item.amount_in_stock,
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return new_item

def read_all(db: Session):
    return db.query(models.MenuItem).all()

def read_one(db: Session, item_id: int):
    try:
        menu_item = db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()
        if not menu_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return menu_item


def update(db: Session, item_id: int, item: schemas.MenuItemCreate):
    try:
        db_item = db.query(models.MenuItem).filter(models.MenuItem.id == item_id)
        if not db_item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Menu item not found")

        update_data = item.dict(exclude_unset=True)
        db_item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return db_item.first()

def delete(db: Session, item_id: int):
    try:
        db_item = db.query(models.MenuItem).filter(models.MenuItem.id == item_id)
        db_item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return Response(status_code=status.HTTP_204_NO_CONTENT)
