from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import order_details as model
from ..models import orders as order_model
from ..models import menu_items as menu_item_model
from sqlalchemy.exc import SQLAlchemyError


def calculate_order_total(db: Session, order_id: int):
    try:
        order_details = db.query(model.OrderDetail).join(
            menu_item_model.MenuItem
        ).filter(model.OrderDetail.order_id == order_id).all()

        total = 0.0
        for detail in order_details:
            total += detail.menu_item.price * detail.amount

        order = db.query(order_model.Order).filter(order_model.Order.id == order_id).first()
        if order:
            order.total_price = total
            db.commit()

        return total
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


def create(db: Session, request):
    new_item = model.OrderDetail(
        order_id=request.order_id,
        menu_item_id=request.menu_item_id,
        amount=request.amount,
        quantity=request.quantity
    )

    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)

        calculate_order_total(db, request.order_id)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return new_item


def read_all(db: Session):
    return db.query(model.OrderDetail).all()


def read_one(db: Session, detail_id):
    item = db.query(model.OrderDetail).filter(model.OrderDetail.id == detail_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detail not found")
    return item


def delete(db: Session, detail_id):
    item = db.query(model.OrderDetail).filter(model.OrderDetail.id == detail_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detail not found")
    order_id = item.order_id
    db.delete(item)
    db.commit()
    calculate_order_total(db, order_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def update(db: Session, detail_id: int, request):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == detail_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")

        order_id = item.first().order_id

        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()

        calculate_order_total(db, order_id)

        return item.first()
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

