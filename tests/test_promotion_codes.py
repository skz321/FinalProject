import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.models.promotion_codes import Base, PromotionCode
from api.controllers import promotion_codes as controller
from api.schemas.promotion_codes import PromotionCodeValidation
from decimal import Decimal
import datetime

# Setup in-memory SQLite for isolated testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()

def create_test_coupon(db):
    promo = PromotionCode(
        code="TESTCODE",
        discount_percentage=Decimal("15.0"),
        minimum_order_amount=Decimal("20.0"),
        max_uses=2,
        current_uses=0,
        is_active=True,
        expiration_date=datetime.datetime(2030, 1, 1),
        created_at=datetime.datetime.utcnow()
    )
    db.add(promo)
    db.commit()
    db.refresh(promo)
    return promo

def test_validate_valid_coupon(db):
    create_test_coupon(db)

    request = PromotionCodeValidation(code="TESTCODE", order_amount=Decimal("25.0"))
    result = controller.validate_promotion_code(db, request)

    assert result.is_valid is True
    assert result.discount_amount == Decimal("3.75")
    assert result.message == "Promotion code applied successfully"

def test_validate_invalid_coupon(db):
    request = PromotionCodeValidation(code="FAKECODE", order_amount=Decimal("25.0"))
    result = controller.validate_promotion_code(db, request)

    assert result.is_valid is False
    assert result.message == "Invalid promotion code"
