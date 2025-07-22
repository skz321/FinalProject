from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from ..models import order_details as model_details
from ..models import sandwiches as model_sandwich
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func



def create(db: Session, request):
    new_item = model.Order(
        customer_name=request.customer_name,
        description=request.description
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
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item


def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item.first()


def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def calculate_total_price(db: Session, item_id: int):
    try:
        # Query order details filtered by item_id
        order_details_query = db.query(model_details.OrderDetail).filter(model_details.OrderDetail.order_id == item_id)

        # Join with sandwiches to get price for each sandwich
        joined_query = order_details_query.join(
            model_sandwich.Sandwich,
            model_details.OrderDetail.sandwich_id == model_sandwich.Sandwich.id
        )

        # Calculate total by summing amount * price for each detail
        total_price = joined_query.with_entities(
            func.sum(model_details.OrderDetail.amount * model_sandwich.Sandwich.price)
        ).scalar()

        # If no order details found, total_price will be None
        if total_price is None:
            total_price = 0.0

        return {"item_id": item_id, "total_price": float(total_price)}

    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))

