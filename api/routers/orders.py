from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)


@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)

@router.get("/{item_id}/total")
def get_order_total(order_id: int, db: Session = Depends(get_db)):
    return controller.calculate_total_price(db, order_id)


# COMMENTED OUT PROMOTION APPLICATION ENDPOINTS
# @router.post("/{order_id}/apply-promotion")
# def apply_promotion_code(
#     order_id: int,
#     promotion_code: str,
#     db: Session = Depends(get_db)
# ):
#     """Apply a promotion code to an order"""
#     return controller.validate_and_apply_promotion_code(db, order_id, promotion_code)


# @router.delete("/{order_id}/remove-promotion")
# def remove_promotion_code(
#     order_id: int,
#     db: Session = Depends(get_db)
# ):
#     """Remove promotion code from an order"""
#     return controller.remove_promotion_code(db, order_id)