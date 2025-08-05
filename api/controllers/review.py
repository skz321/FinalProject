from sqlalchemy.orm import Session
from fastapi import Response, status
from ..models import reviews as models
from ..schemas import reviews as schemas
from sqlalchemy import func
from ..models import menu_items as menu_models

def create(db: Session, review: schemas.ReviewCreate):
    new_review = models.Review(
        rating=review.rating,
        review_text=review.review_text,
        menu_item_id=review.menu_item_id,
        customer_id=review.customer_id
    )
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

def read_all(db: Session):
    return db.query(models.Review).all()

def read_for_menu_item(db: Session, menu_item_id: int):
    return db.query(models.Review).filter(models.Review.menu_item_id == menu_item_id).all()

def read_one(db: Session, review_id: int):
    return db.query(models.Review).filter(models.Review.id == review_id).first()

def delete(db: Session, review_id: int):
    db_review = db.query(models.Review).filter(models.Review.id == review_id)
    db_review.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def get_low_rated_menu_items(db: Session, threshold: float = 3.0):
    results = (
        db.query(
            menu_models.MenuItem.id,
            menu_models.MenuItem.name,
            func.avg(models.Review.rating).label("average_rating"),
            func.count(models.Review.id).label("review_count")
        )
        .join(models.Review)
        .group_by(menu_models.MenuItem.id)
        .having(func.avg(models.Review.rating) < threshold)
        .order_by(func.avg(models.Review.rating))
        .all()
    )
    return results


