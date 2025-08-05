from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import menu_items as model_menu_items
from ..models import orders as model_orders
from ..models import order_details as model_order_details
from . import ingredients as ingredient_controller
from . import menu_item_ingredients as link_controller
from ..models import ingredients as model_ingredients
from ..schemas import orders as order_schema
from ..schemas import order_details as order_details_schema
from . import order_details as order_details_controller
from . import user as user_controller
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timezone, time
from sqlalchemy import and_, func

def create(db: Session, order: order_schema.OrderCreate):

    tracking_number = "TRACK-" + datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    customer_name = order.customer_name
    order_type = order.order_type
    if not customer_name or customer_name == "string":
        if order.user_id:
            customer_name = user_controller.read_one(db, order.user_id).name
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Please order as a user or enter name if guest")
    if not order_type or order_type == "string":
        if order.user_id:
            # customer_name = user_controller.read_one(db, order.user_id).name
            order_type = user_controller.read_one(db, order.user_id).order_type_preference # todo: implement in users
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Please order as a user or manually enter order type if guest")

    new_order = model_orders.Order(
        customer_name=customer_name,
        order_type = order_type,
        description=order.description,
        tracking_number=tracking_number,
        total_price=0.00,
        is_paid=False,
        card="",
    )

    if order.user_id:
        new_order.user_id = order.user_id

    total_price = 0
    ingredient_usage = {}

    try:
        db.add(new_order)
        db.flush()

        for detail in order.order_details:
            menu_item = db.query(model_menu_items.MenuItem).filter_by(id=detail.menu_item_id).first()
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
        db.query(model_order_details.OrderDetail).filter(model_order_details.OrderDetail.order_id == order_id).delete(synchronize_session=False)
        order.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['or`ig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



def pay_for_order(db: Session, order_id: int, amount_paid: float, card: str):
    try:
        order = read_one(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        if order.is_paid:
            raise HTTPException(status_code=400, detail="Order already paid")

        total_price = order.total_price

        if amount_paid < total_price:
            raise HTTPException(status_code=400, detail=f"Insufficient payment. Total is ${total_price:.2f}")

        if len(card) < 16 or not card.isdigit():
            raise HTTPException(status_code=400, detail="Invalid card number")

        protected_card = f"xxxx-xxxx-xxxx-{card[-4:]}"

        order.card = protected_card
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

    if not order.is_paid:
        raise HTTPException(status_code=400, detail="Order is not paid for")

    if order.status == "Completed":
        raise HTTPException(status_code=400, detail="Order is already completed")

    order.status = "Completed"
    db.commit()
    db.refresh(order)
    return {"message": f"Order {order_id} marked as completed"}


def get_status(db: Session, tracking_number: str):
    try:
        order = db.query(model_orders.Order).filter(model_orders.Order.tracking_number == tracking_number).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return {"status": order.status}
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)



def get_orders_by_date(db: Session, date: datetime):
    try:
        start_of_day = datetime.combine(date.date(), time.min)
        end_of_day = datetime.combine(date.date(), time.max)

        orders = db.query(model_orders.Order).filter(
            and_(
                model_orders.Order.order_date >= start_of_day,
                model_orders.Order.order_date <= end_of_day
            )
        ).all()
        if not orders:
            raise HTTPException(status_code=404, detail="No orders found")

        return orders

    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

def get_orders_by_time_range(db: Session, start: datetime, end: datetime):
    try:
        orders = db.query(model_orders.Order).filter(
            model_orders.Order.order_date.between(start, end)
        ).all()
        if not orders:
            raise HTTPException(status_code=404, detail="No orders found")
        return orders

    except SQLAlchemyError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))




def get_sales_report_for_day(db: Session, date: datetime):
    try:
        start_of_day = datetime.combine(date.date(), time.min)
        end_of_day = datetime.combine(date.date(), time.max)

        total_revenue = db.query(func.coalesce(func.sum(model_orders.Order.total_price), 0)).filter(
            and_(
                model_orders.Order.order_date >= start_of_day,
                model_orders.Order.order_date <= end_of_day,
                model_orders.Order.is_paid == True
            )
        ).scalar()

        # query to get menu item amounts for the day
        base_query = db.query(
            model_order_details.OrderDetail.menu_item_id,
            func.sum(model_order_details.OrderDetail.amount).label("total_quantity"),
            model_menu_items.MenuItem.name
        ).join(
            model_orders.Order,
            model_order_details.OrderDetail.order_id == model_orders.Order.id
        ).join(
            model_menu_items.MenuItem,
            model_order_details.OrderDetail.menu_item_id == model_menu_items.MenuItem.id
        ).filter(
            and_(
                model_orders.Order.order_date >= start_of_day,
                model_orders.Order.order_date <= end_of_day,
                model_orders.Order.is_paid == True
            )
        ).group_by(
            model_order_details.OrderDetail.menu_item_id,
            model_menu_items.MenuItem.name
        )

        # the most popular item
        most_popular_item = base_query.order_by(func.sum(model_order_details.OrderDetail.amount).desc()).first()
        if most_popular_item:
            most_popular = {
                "menu_item_id": most_popular_item.menu_item_id,
                "name": most_popular_item.name,
                "total_quantity": most_popular_item.total_quantity
            }
        else:
            most_popular = None

        # the least popular item
        least_popular_item = base_query.order_by(func.sum(model_order_details.OrderDetail.amount).asc()).first()
        if least_popular_item:
            least_popular = {
                "menu_item_id": least_popular_item.menu_item_id,
                "name": least_popular_item.name,
                "total_quantity": least_popular_item.total_quantity
            }
        else:
            least_popular = None

        return {
            "date": date.date(),
            "total_revenue": total_revenue,
            "most_popular_menu_item": most_popular,
            "least_popular_menu_item": least_popular
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# COMMENTED OUT PROMOTION APPLICATION LOGIC
# def validate_and_apply_promotion_code(db: Session, order_id: int, promotion_code: str):
#     """Validate and apply a promotion code to an order"""
#def create(db: Session, request):
   # new_item = model.Order(
        # customer_name=request.customer_name,
        # description=request.description,
        # promotion_code=request.promotion_code,
        # discount_amount=request.discount_amount,
        # final_price=request.final_price
    #)
#     try:
#         # Get the order
#         order = read_one(db, order_id)
#         if not order:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
#         
#         # Calculate current total price
#         total_info = calculate_total_price(db, order_id)
#         current_total = Decimal(str(total_info["total_price"]))
#         
#         # Validate the promotion code
#         validation_request = PromotionCodeValidation(
#             code=promotion_code,
#             order_amount=current_total
#         )
#         
#         validation_result = promotion_controller.validate_promotion_code(db, validation_request)
#         
#         if not validation_result.is_valid:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST, 
#                 detail=validation_result.message
#             )
#         
#         # Apply the promotion code
#         promotion_controller.apply_promotion_code(db, promotion_code)
#         
#         # Update the order with discount information
#         discount_amount = validation_result.discount_amount
#         final_price = current_total - discount_amount
#         
#         update_data = {
#             "promotion_code": promotion_code,
#             "discount_amount": float(discount_amount),
#             "final_price": float(final_price),
#             "total_price": float(current_total)
#         }
#         
#         # Update the order
#         item = db.query(model.Order).filter(model.Order.id == order_id)
#         item.update(update_data, synchronize_session=False)
#         db.commit()
#         
#         return {
#             "order_id": order_id,
#             "original_total": float(current_total),
#             "discount_amount": float(discount_amount),
#             "final_price": float(final_price),
#             "promotion_code": promotion_code,
#             "message": validation_result.message
#         }
#         
#     except SQLAlchemyError as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))


# def remove_promotion_code(db: Session, order_id: int):
#     """Remove promotion code from an order"""
#     try:
#         order = read_one(db, order_id)
#         if not order:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
#         
#         # Reset promotion code fields
#         update_data = {
#             "promotion_code": None,
#             "discount_amount": None,
#             "final_price": None
#         }
#         
#         item = db.query(model.Order).filter(model.Order.id == order_id)
#         item.update(update_data, synchronize_session=False)
#         db.commit()
#         
#         return {
#             "order_id": order_id,
#             "message": "Promotion code removed successfully"
#         }
#         
#     except SQLAlchemyError as e:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__['orig']))


