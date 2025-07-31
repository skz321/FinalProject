from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..dependencies.database import get_db
from ..schemas import reviews as schemas
from ..controllers import review as controller

router = APIRouter(prefix="/reviews", tags=["Reviews"])

@router.post("/", response_model=schemas.Review)
def create_review(review: schemas.ReviewCreate, db: Session = Depends(get_db)):
    return controller.create(db, review)

@router.get("/", response_model=List[schemas.Review])
def get_all_reviews(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/menu-item/{menu_item_id}", response_model=List[schemas.Review])
def get_reviews_for_menu_item(menu_item_id: int, db: Session = Depends(get_db)):
    return controller.read_for_menu_item(db, menu_item_id)

@router.get("/{review_id}", response_model=schemas.Review)
def get_review(review_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, review_id)

@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, review_id)


