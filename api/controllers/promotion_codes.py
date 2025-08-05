from sqlalchemy.orm import Session
from api.models.promotion_codes import PromotionCode
from api.schemas.promotion_codes import PromotionCodeCreate, PromotionCodeUpdate, PromotionCodeValidation, PromotionCodeValidationResponse
import random, string, datetime
from decimal import Decimal
from typing import Optional


def generate_code(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))


def create_promotion_code(db: Session, request: PromotionCodeCreate):
    code = generate_code()
    db_code = PromotionCode(
        code=code,
        discount_percentage=request.discount_percentage,
        minimum_order_amount=request.minimum_order_amount,
        max_uses=request.max_uses,
        is_active=request.is_active,
        expiration_date=request.expiration_date
    )
    db.add(db_code)
    db.commit()
    db.refresh(db_code)
    return db_code


def get_promotion_code_by_code(db: Session, code: str) -> Optional[PromotionCode]:
    return db.query(PromotionCode).filter(PromotionCode.code == code).first()


def validate_promotion_code(db: Session, validation_request: PromotionCodeValidation) -> PromotionCodeValidationResponse:
    """Validate a promotion code and return discount information"""
    promotion_code = get_promotion_code_by_code(db, validation_request.code)
    
    if not promotion_code:
        return PromotionCodeValidationResponse(
            is_valid=False,
            message="Invalid promotion code"
        )
    
    # Check if code is active
    if not promotion_code.is_active:
        return PromotionCodeValidationResponse(
            is_valid=False,
            message="Promotion code is inactive"
        )
    
    # Check if code has expired
    if promotion_code.expiration_date < datetime.datetime.utcnow():
        return PromotionCodeValidationResponse(
            is_valid=False,
            message="Promotion code has expired"
        )
    
    # Check if maximum uses reached
    if promotion_code.max_uses and promotion_code.current_uses >= promotion_code.max_uses:
        return PromotionCodeValidationResponse(
            is_valid=False,
            message="Promotion code usage limit reached"
        )
    
    # Check minimum order amount
    if promotion_code.minimum_order_amount and validation_request.order_amount < promotion_code.minimum_order_amount:
        return PromotionCodeValidationResponse(
            is_valid=False,
            message=f"Minimum order amount of ${promotion_code.minimum_order_amount} required"
        )
    
    # Calculate discount amount
    discount_amount = (validation_request.order_amount * promotion_code.discount_percentage) / Decimal('100')
    
    return PromotionCodeValidationResponse(
        is_valid=True,
        discount_amount=discount_amount,
        discount_percentage=promotion_code.discount_percentage,
        message="Promotion code applied successfully"
    )


def apply_promotion_code(db: Session, code: str) -> Optional[PromotionCode]:
    """Apply a promotion code and increment its usage count"""
    promotion_code = get_promotion_code_by_code(db, code)
    
    if promotion_code:
        promotion_code.current_uses += 1
        db.commit()
        db.refresh(promotion_code)
    
    return promotion_code


def get_all_promotion_codes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(PromotionCode).offset(skip).limit(limit).all()


def update_promotion_code(db: Session, code_id: int, update_data: PromotionCodeUpdate):
    promotion_code = db.query(PromotionCode).filter(PromotionCode.id == code_id).first()
    if not promotion_code:
        return None
    
    update_dict = update_data.dict(exclude_unset=True)
    for field, value in update_dict.items():
        setattr(promotion_code, field, value)
    
    db.commit()
    db.refresh(promotion_code)
    return promotion_code


def delete_promotion_code(db: Session, code_id: int):
    promotion_code = db.query(PromotionCode).filter(PromotionCode.id == code_id).first()
    if promotion_code:
        db.delete(promotion_code)
        db.commit()
        return True
    return False 