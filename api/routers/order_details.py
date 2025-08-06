from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.dependencies.database import get_db
from api.controllers import order_details as controller
from ..schemas import order_details as schema


router = APIRouter(prefix="/order-details", tags=["Order Details"])

@router.post("/", response_model=schema.OrderDetail)
def create_order_detail(request: schema.OrderDetailCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request, order_id=request.order_id)


@router.get("/order/{order_id}")
def get_order_details_by_order(order_id: int, db: Session = Depends(get_db)):
    return controller.read_by_order(db=db, order_id=order_id)


@router.get("/{detail_id}", response_model=schema.OrderDetail)
def get_order_detail(detail_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db=db, detail_id=detail_id)


@router.delete("/{detail_id}")
def delete_order_detail(detail_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, detail_id=detail_id)
