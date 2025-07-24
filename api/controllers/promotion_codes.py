from sqlalchemy.orm import Session
from api.models.promotion_codes import PromotionCode
from api.schemas.promotion_codes import PromotionCodeCreate
import random, string, datetime


def generate_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def create_promotion_code(db: Session, request: PromotionCodeCreate):
    code = generate_code()
    db_code = PromotionCode(
        code=code,
        expiration_date=request.expiration_date
    )
    db.add(db_code)
    db.commit()
    db.refresh(db_code)
    return db_code 