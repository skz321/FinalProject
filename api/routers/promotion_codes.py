from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from api.schemas.promotion_codes import PromotionCode, PromotionCodeCreate
from api.controllers import promotion_codes as controller
from api.dependencies.database import get_db

router = APIRouter(
    tags=["Promotion Codes"],
    prefix="/promotions"
)

@router.post("/generate", response_model=PromotionCode)
def generate_promotion_code(request: PromotionCodeCreate, db: Session = Depends(get_db)):
    return controller.create_promotion_code(db, request) 