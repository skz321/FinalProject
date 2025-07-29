from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import restaurants as restaurant_model

from sqlalchemy.exc import SQLAlchemyError




def create(db: Session, request):
    new_restaurant = restaurant_model.Restaurant(
        restaurant_name= request.restaurant_name,
        owner=request.owner,
    )

    try:
        # todo: verify that owner_id is in Users table
        db.add(new_restaurant)
        db.commit()
        db.refresh(new_restaurant)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_restaurant


def read_all(db: Session):
    try:
        all_restaurants = db.query(restaurant_model.Restaurant).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return all_restaurants


def read_one(db: Session, restaurant_id):
    try:
        restaurant = db.query(restaurant_model.Restaurant).filter(restaurant_model.Restaurant.id == restaurant_id).first()
        if not restaurant:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return restaurant


def update(db: Session, restaurant_id, request):
    try:
        restaurant = db.query(restaurant_model.Restaurant).filter(restaurant_model.Restaurant.id == restaurant_id)
        if not restaurant.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        restaurant.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return restaurant.first()


def delete(db: Session, restaurant_id):
    try:
        restaurant = db.query(restaurant_model.Restaurant).filter(restaurant_model.Restaurant.id == restaurant_id)
        if not restaurant.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        restaurant.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

