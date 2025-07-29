from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import restaurants as restaurant_model
from ..models import food_items as food_model
from sqlalchemy.exc import SQLAlchemyError




def add_food_item(db: Session, restaurant_id: int, name: str, price: float):
    restaurant = db.query(restaurant_model.Restaurant).filter(restaurant_model.Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Restaurant not found")


    new_food_item = food_model.FoodItem(
        food_item_name=name,
        price=price,
        restaurant_id=restaurant_id
    )

    try:
        db.add(new_food_item)
        db.commit()
        db.refresh(new_food_item)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_food_item

def read_all_food_items(db: Session, restaurant_id: int):
    try:
        food_items = db.query(food_model.FoodItem).filter(food_model.FoodItem.restaurant_id == restaurant_id).all()
        if not food_items:
            return []
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return food_items


def update_food_item(db: Session, food_item_id: int, request):
    try:
        item_query = db.query(food_model.FoodItem).filter(food_model.FoodItem.id == food_item_id)
        if not item_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found")

        update_data = request.dict(exclude_unset=True)
        item_query.update(update_data, synchronize_session=False)
        db.commit()
        updated_item = item_query.first()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return updated_item




def delete_food_item(db: Session, food_item_id: int):
    try:
        item_query = db.query(food_model.FoodItem).filter(food_model.FoodItem.id == food_item_id)
        if not item_query.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food item not found")
        item_query.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return Response(status_code=status.HTTP_204_NO_CONTENT)