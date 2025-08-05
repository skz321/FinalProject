from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from ..models import order_details as model_details
from ..models import sandwiches as model_sandwich
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
# from decimal import Decimal
# from . import promotion_codes as promotion_controller
# from ..schemas.promotion_codes import PromotionCodeValidation


def create(db: Session, request):
    new_item = model.Order(
        customer_name=request.customer_name,
        description=request.description,
        # promotion_code=request.promotion_code,
        # discount_amount=request.discount_amount,
        # final_price=request.final_price
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


# COMMENTED OUT PROMOTION APPLICATION LOGIC
# def validate_and_apply_promotion_code(db: Session, order_id: int, promotion_code: str):
#     """Validate and apply a promotion code to an order"""
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

