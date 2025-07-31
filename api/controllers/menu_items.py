from sqlalchemy.orm import Session
from fastapi import Response, status
from ..models import menu_items as models
from ..schemas import menu_items as schemas

def create(db: Session, item: schemas.MenuItemCreate):
    new_item = models.MenuItem(
        name=item.name,
        price=item.price,
        calories=item.calories,
        category=item.category
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item

def read_all(db: Session):
    return db.query(models.MenuItem).all()

def read_one(db: Session, item_id: int):
    return db.query(models.MenuItem).filter(models.MenuItem.id == item_id).first()

def update(db: Session, item_id: int, item: schemas.MenuItemCreate):
    db_item = db.query(models.MenuItem).filter(models.MenuItem.id == item_id)
    update_data = item.dict(exclude_unset=True)
    db_item.update(update_data, synchronize_session=False)
    db.commit()
    return db_item.first()

def delete(db: Session, item_id: int):
    db_item = db.query(models.MenuItem).filter(models.MenuItem.id == item_id)
    db_item.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
