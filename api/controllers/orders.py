from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import orders as model_orders
from ..models import menu_items as model_menu_item
from . import ingredients as ingredient_controller
from . import menu_item_ingredients as link_controller
from ..models import ingredients as model_ingredients
from ..schemas import orders as order_schema
from ..schemas import order_details as order_details_schema
from . import order_details as order_details_controller
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone

def create(db: Session, order: order_schema.OrderCreate):
    from sqlalchemy.exc import SQLAlchemyError
    from datetime import datetime, timezone

    tracking_number = "TRACK-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    new_order = model_orders.Order(
        customer_name=order.customer_name,
        description=order.description,
        tracking_number=tracking_number,
        total_price=0.00,
        is_paid=False,
    )

    total_price = 0
    ingredient_usage = {}

    try:
        db.add(new_order)
        db.flush()

        for detail in order.order_details:
            menu_item = db.query(model_menu_item.MenuItem).filter_by(id=detail.menu_item_id).first()
            if not menu_item:
                raise HTTPException(status_code=404, detail=f"Menu item {detail.menu_item_id} not found")

            item_links = link_controller.read_by_menu_item(db, menu_item.id)
            for link in item_links:
                total_required = link.required_quantity * detail.amount
                ingredient_usage[link.ingredient_id] = ingredient_usage.get(link.ingredient_id, 0) + total_required

            total_price += menu_item.price * detail.amount

        # checks if there are enough ingredients
        for ingredient_id, required_qty in ingredient_usage.items():
            ingredient = ingredient_controller.read_one(db, ingredient_id)
            if ingredient.quantity < required_qty:
                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough {ingredient.name}. Needed: {required_qty}, Available: {ingredient.quantity}"
                )


        for detail in order.order_details:
            order_details_controller.create(
                db=db,
                request=order_details_schema.OrderDetailUpdate(
                    order_id=new_order.id,
                    menu_item_id=detail.menu_item_id,
                    amount=detail.amount
                )
            )

        # removes ingredients from quantity
        for ingredient_id, used_qty in ingredient_usage.items():
            ingredient = db.query(model_ingredients.Ingredient).filter_by(id=ingredient_id).first()
            ingredient.quantity -= used_qty

        new_order.total_price = total_price
        db.commit()
        db.refresh(new_order)

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

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

# todo: def get_status
