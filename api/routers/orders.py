from fastapi import APIRouter, Depends, FastAPI, status, Response, Body, HTTPException
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Orders-OrderDetails'],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, order=request)


@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)


@router.get("/{order_id}", response_model=schema.Order)
def read_one(order_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, order_id=order_id)


@router.put("/{order_id}", response_model=schema.Order)
def update(order_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, order_id=order_id)


@router.delete("/{order_id}")
def delete(order_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, order_id=order_id)

@router.post("/{order_id}/pay", tags=["Orders"])
def pay(order_id: int, payment_amount: int, card: str, db: Session = Depends(get_db)):
    # amount_paid = payment.get("amount_paid")
    if payment_amount is None:
        raise HTTPException(status_code=400, detail="Payment amount is required")
    return controller.pay_for_order(db, order_id, payment_amount, card)

@router.put("/{order_id}/complete", status_code=200)
def complete_order(order_id: int, db: Session = Depends(get_db)):
    return controller.mark_order_completed(db, order_id)

@router.get("/status/{tracking_number}", response_model=schema.OrderStatus)
def get_status(tracking_number: str, db: Session = Depends(get_db)):
    return controller.get_status(db, tracking_number=tracking_number)
