from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..controllers import menu_items as controller
from ..schemas import menu_items as schemas
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/menu-items",
    tags=["Menu Items"]
)

@router.post("/", response_model=schemas.MenuItem)
def create_item(item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    return controller.create(db, item)

@router.get("/", response_model=list[schemas.MenuItem])
def list_items(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{item_id}", response_model=schemas.MenuItem)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = controller.read_one(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return item

@router.put("/{item_id}", response_model=schemas.MenuItem)
def update_item(item_id: int, item: schemas.MenuItemCreate, db: Session = Depends(get_db)):
    return controller.update(db, item_id, item)

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = controller.read_one(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Menu item not found")
    return controller.delete(db, item_id)

@router.get("/category/", status_code=200)
def get_by_category(category: str, db: Session = Depends(get_db)):
    return controller.get_category(db=db, category=category)