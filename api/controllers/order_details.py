from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import order_details as model
from sqlalchemy.exc import SQLAlchemyError


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
    db.delete(item)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def update(db: Session, detail_id: int, request):
    item = db.query(model.OrderDetail).filter(model.OrderDetail.id == detail_id).first()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Detail not found")

    update_data = request.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    try:
        db.commit()
        db.refresh(item)
    except SQLAlchemyError as e:
        db.rollback()
        print("PUT ERROR:", str(e))  # 👈 This line shows the real error in your terminal
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return item
