from fastapi.testclient import TestClient
from ..controllers import orders as controller
from ..main import app
import pytest
from ..models import orders as model
from ..models import promotion_codes as promotion_model
from decimal import Decimal
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_order(db_session):
    # Create a sample order
    order_data = {
        "customer_name": "John Doe",
        "description": "Test order"
    }

    order_object = model.Order(**order_data)

    # Call the create function
    created_order = controller.create(db_session, order_object)

    # Assertions
    assert created_order is not None
    assert created_order.customer_name == "John Doe"
    assert created_order.description == "Test order"


def test_create_promotion_code(db_session):
    """Test creating a promotion code"""
    from ..controllers import promotion_codes as promotion_controller
    from ..schemas.promotion_codes import PromotionCodeCreate
    
    promotion_data = PromotionCodeCreate(
        code="TEST123",
        discount_percentage=Decimal("15.50"),
        minimum_order_amount=Decimal("25.00"),
        max_uses=100,
        is_active=True,
        expiration_date=datetime.utcnow() + timedelta(days=30)
    )
    
    created_code = promotion_controller.create_promotion_code(db_session, promotion_data)
    
    assert created_code is not None
    assert created_code.code == "TEST123"
    assert created_code.discount_percentage == Decimal("15.50")
    assert created_code.minimum_order_amount == Decimal("25.00")
    assert created_code.max_uses == 100
    assert created_code.is_active is True


def test_validate_promotion_code_valid(db_session):
    """Test validating a valid promotion code"""
    from ..controllers import promotion_codes as promotion_controller
    from ..schemas.promotion_codes import PromotionCodeValidation
    
    # Create a mock promotion code
    mock_code = promotion_model.PromotionCode(
        id=1,
        code="VALID123",
        discount_percentage=Decimal("10.00"),
        minimum_order_amount=Decimal("20.00"),
        max_uses=50,
        current_uses=0,
        is_active=True,
        expiration_date=datetime.utcnow() + timedelta(days=30)
    )
    
    # Mock the database query
    db_session.query.return_value.filter.return_value.first.return_value = mock_code
    
    validation_request = PromotionCodeValidation(
        code="VALID123",
        order_amount=Decimal("50.00")
    )
    
    result = promotion_controller.validate_promotion_code(db_session, validation_request)
    
    assert result.is_valid is True
    assert result.discount_amount == Decimal("5.00")  # 10% of 50.00
    assert result.discount_percentage == Decimal("10.00")
    assert "successfully" in result.message


def test_validate_promotion_code_invalid(db_session):
    """Test validating an invalid promotion code"""
    from ..controllers import promotion_codes as promotion_controller
    from ..schemas.promotion_codes import PromotionCodeValidation
    
    # Mock the database query to return None (code not found)
    db_session.query.return_value.filter.return_value.first.return_value = None
    
    validation_request = PromotionCodeValidation(
        code="INVALID123",
        order_amount=Decimal("50.00")
    )
    
    result = promotion_controller.validate_promotion_code(db_session, validation_request)
    
    assert result.is_valid is False
    assert result.message == "Invalid promotion code"


def test_validate_promotion_code_expired(db_session):
    """Test validating an expired promotion code"""
    from ..controllers import promotion_codes as promotion_controller
    from ..schemas.promotion_codes import PromotionCodeValidation
    
    # Create a mock expired promotion code
    mock_code = promotion_model.PromotionCode(
        id=1,
        code="EXPIRED123",
        discount_percentage=Decimal("10.00"),
        minimum_order_amount=None,
        max_uses=None,
        current_uses=0,
        is_active=True,
        expiration_date=datetime.utcnow() - timedelta(days=1)  # Expired yesterday
    )
    
    # Mock the database query
    db_session.query.return_value.filter.return_value.first.return_value = mock_code
    
    validation_request = PromotionCodeValidation(
        code="EXPIRED123",
        order_amount=Decimal("50.00")
    )
    
    result = promotion_controller.validate_promotion_code(db_session, validation_request)
    
    assert result.is_valid is False
    assert result.message == "Promotion code has expired"


def test_validate_promotion_code_minimum_amount(db_session):
    """Test validating a promotion code with minimum order amount requirement"""
    from ..controllers import promotion_codes as promotion_controller
    from ..schemas.promotion_codes import PromotionCodeValidation
    
    # Create a mock promotion code with minimum order amount
    mock_code = promotion_model.PromotionCode(
        id=1,
        code="MIN123",
        discount_percentage=Decimal("15.00"),
        minimum_order_amount=Decimal("100.00"),
        max_uses=None,
        current_uses=0,
        is_active=True,
        expiration_date=datetime.utcnow() + timedelta(days=30)
    )
    
    # Mock the database query
    db_session.query.return_value.filter.return_value.first.return_value = mock_code
    
    validation_request = PromotionCodeValidation(
        code="MIN123",
        order_amount=Decimal("50.00")  # Below minimum
    )
    
    result = promotion_controller.validate_promotion_code(db_session, validation_request)
    
    assert result.is_valid is False
    assert "Minimum order amount" in result.message


def test_apply_promotion_code(db_session):
    """Test applying a promotion code and incrementing usage"""
    from ..controllers import promotion_codes as promotion_controller
    
    # Create a mock promotion code
    mock_code = promotion_model.PromotionCode(
        id=1,
        code="APPLY123",
        discount_percentage=Decimal("10.00"),
        minimum_order_amount=None,
        max_uses=100,
        current_uses=5,
        is_active=True,
        expiration_date=datetime.utcnow() + timedelta(days=30)
    )
    
    # Mock the database query
    db_session.query.return_value.filter.return_value.first.return_value = mock_code
    
    result = promotion_controller.apply_promotion_code(db_session, "APPLY123")
    
    assert result is not None
    assert result.current_uses == 6  # Should be incremented
    db_session.commit.assert_called_once()
    db_session.refresh.assert_called_once_with(result)
