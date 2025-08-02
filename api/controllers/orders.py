from json import JSONDecodeError
from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends, Request
from ..models import orders as model_orders
from ..models import menu_items as model_menu_item
from ..schemas import orders as order_schema
from ..schemas import order_details as order_details_schema
from . import order_details as order_details_controller
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone

def create(db: Session, order: order_schema.OrderCreate):
    tracking_number = "TRACK-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    new_order = model_orders.Order(
        customer_name=order.customer_name,
        description=order.description,
        tracking_number=tracking_number,
        total_price=0.00,
        is_paid=False,
    )

    total_price = 0

    try:
        db.add(new_order)
        db.flush()
        for detail in order.order_details:
            menu_item = (db.query(model_menu_item.MenuItem)
                         .filter(model_menu_item.MenuItem.id == detail.menu_item_id)
                         .first())
            if not menu_item:
                raise HTTPException(status_code=404, detail=f"Menu item {detail.menu_item_id} not found")

            item_total = menu_item.price * detail.amount
            total_price += item_total

            detail_request = order_details_schema.OrderDetailCreate(
                menu_item_id=detail.menu_item_id,
                amount=detail.amount
            )
            order_details_controller.create(
                db=db,
                request=order_details_schema.OrderDetailUpdate(
                    order_id=new_order.id,
                    menu_item_id=detail_request.menu_item_id,
                    amount=detail_request.amount
                )
            )
        new_order.total_price = total_price
        db.commit()
        db.refresh(new_order)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_order


def read_all(db: Session):
    try:
        result = db.query(model_orders.Order).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result


def read_one(db: Session, order_id: int):
    try:
        order = db.query(model_orders.Order).filter(model_orders.Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order


def update(db: Session, order_id, request):
    try:
        order = db.query(model_orders.Order).filter(model_orders.Order.id == order_id)
        if not order.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        update_data = request.dict(exclude_unset=True)
        order.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return order.first()


def delete(db: Session, order_id):
    try:
        order = db.query(model_orders.Order).filter(model_orders.Order.id == order_id)
        if not order.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Id not found!")
        order_details_controller.delete(db, order_id)
        order.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



def pay_for_order(db: Session, order_id: int, amount_paid: float):
    try:
        order = read_one(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if order.is_paid:
            raise HTTPException(status_code=400, detail="Order already paid")

        total_price = order.total_price

        if amount_paid < total_price:
            raise HTTPException(status_code=400, detail=f"Insufficient payment. Total is ${total_price:.2f}")

        order.is_paid = True
        order.paid_at = datetime.now(timezone.utc)

        db.commit()
        db.refresh(order)

        change = amount_paid - order.total_price
        return {
            "message": "Payment successful",
            "total_price": round(total_price, 2),
            "amount_paid": round(amount_paid, 2),
            "change": round(change, 2),
            "paid_at": order.paid_at
        }


    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)




def mark_order_completed(db: Session, order_id: int):
    order = read_one(db, order_id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status == "Completed":
        raise HTTPException(status_code=400, detail="Order is already completed")

    order.status = "Completed"
    db.commit()
    db.refresh(order)
    return {"message": f"Order {order_id} marked as completed"}