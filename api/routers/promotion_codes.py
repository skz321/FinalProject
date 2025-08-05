from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..dependencies.database import get_db
from ..controllers import promotion_codes as controller
from ..schemas.promotion_codes import (
    PromotionCode, 
    PromotionCodeCreate, 
    PromotionCodeUpdate,
    PromotionCodeValidation,
    PromotionCodeValidationResponse
)

router = APIRouter(prefix="/promotion-codes", tags=["Promotion Codes"])


@router.post("/", response_model=PromotionCode, status_code=status.HTTP_201_CREATED)
def create_promotion_code(
    request: PromotionCodeCreate,
    db: Session = Depends(get_db)
):
    """Create a new promotion code"""
    return controller.create_promotion_code(db, request)


@router.get("/", response_model=List[PromotionCode])
def get_promotion_codes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get all promotion codes"""
    return controller.get_all_promotion_codes(db, skip=skip, limit=limit)


@router.get("/{code_id}", response_model=PromotionCode)
def get_promotion_code(
    code_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific promotion code by ID"""
    promotion_code = db.query(controller.PromotionCode).filter(controller.PromotionCode.id == code_id).first()
    if not promotion_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion code not found")
    return promotion_code


@router.put("/{code_id}", response_model=PromotionCode)
def update_promotion_code(
    code_id: int,
    request: PromotionCodeUpdate,
    db: Session = Depends(get_db)
):
    """Update a promotion code"""
    promotion_code = controller.update_promotion_code(db, code_id, request)
    if not promotion_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion code not found")
    return promotion_code


@router.delete("/{code_id}")
def delete_promotion_code(
    code_id: int,
    db: Session = Depends(get_db)
):
    """Delete a promotion code"""
    success = controller.delete_promotion_code(db, code_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion code not found")
    return {"message": "Promotion code deleted successfully"}


@router.post("/validate", response_model=PromotionCodeValidationResponse)
def validate_promotion_code(
    request: PromotionCodeValidation,
    db: Session = Depends(get_db)
):
    """Validate a promotion code without applying it"""
    return controller.validate_promotion_code(db, request)


@router.get("/code/{code}", response_model=PromotionCode)
def get_promotion_code_by_code(
    code: str,
    db: Session = Depends(get_db)
):
    """Get a promotion code by its code string"""
    promotion_code = controller.get_promotion_code_by_code(db, code)
    if not promotion_code:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promotion code not found")
    return promotion_code 