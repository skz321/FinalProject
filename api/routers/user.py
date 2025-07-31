from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..controllers import user as controller
from ..schemas import user as schemas
from ..dependencies.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return controller.create(db, user)

@router.get("/", response_model=list[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{user_id}", response_model=schemas.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = controller.read_one(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = controller.read_one(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return controller.delete(db, user_id)

