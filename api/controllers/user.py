from sqlalchemy.orm import Session
from fastapi import Response, status
from ..models import user as models
from ..schemas import user as schemas

def create(db: Session, user: schemas.UserCreate):
    new_user = models.User(
        name=user.name,
        email=user.email,
        phone_number=user.phone_number,
        address=user.address,
        password=user.password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def read_all(db: Session):
    return db.query(models.User).all()

def read_one(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def update(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = db.query(models.User).filter(models.User.id == user_id)
    update_data = user.dict(exclude_unset=True)
    db_user.update(update_data, synchronize_session=False)
    db.commit()
    return db_user.first()

def delete(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id)
    db_user.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
