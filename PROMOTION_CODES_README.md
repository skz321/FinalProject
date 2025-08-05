# Promotion Codes System

This document describes the promotion codes system implemented for the payment processing feature.

## Overview

The promotion codes system allows you to create, validate, and apply discount codes to orders. It includes features like:

- Percentage-based discounts
- Minimum order amount requirements
- Usage limits and tracking
- Expiration dates
- Active/inactive status
- **Auto-generation of codes** (recommended)

## Code Generation Options

### 🔄 Auto-Generation (Recommended)

The system can automatically generate unique promotion codes for you:

```python
# Auto-generate code (recommended)
promotion_data = {
    "discount_percentage": 15.50,
    "minimum_order_amount": 25.00,
    "max_uses": 100,
    "is_active": True,
    "expiration_date": "2024-12-31T23:59:59"
    # No "code" field - will be auto-generated!
}

response = requests.post("http://localhost:8000/promotion-codes/", json=promotion_data)
# Response: {"code": "A7B2K9M4", "discount_percentage": 15.50, ...}
```

**Auto-generated codes:**

- 8 characters long
- Uppercase letters (A-Z) + digits (0-9)
- Randomly generated for uniqueness
- Examples: `A7B2K9M4`, `X9K2M5N8`, `P3Q7R1S4`

### ✏️ Custom Codes

You can also specify your own custom codes:

```python
# Custom code
promotion_data = {
    "code": "SAVE15",  # Your custom code
    "discount_percentage": 15.50,
    "minimum_order_amount": 25.00,
    "max_uses": 100,
    "is_active": True,
    "expiration_date": "2024-12-31T23:59:59"
}
```

## Database Schema

### Promotion Codes Table

```sql
CREATE TABLE promotion_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(32) UNIQUE NOT NULL,
    discount_percentage DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    minimum_order_amount DECIMAL(10,2),
    max_uses INTEGER,
    current_uses INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    expiration_date DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Orders Table (Updated)

The orders table has been enhanced with promotion code fields:

```sql
ALTER TABLE orders ADD COLUMN promotion_code VARCHAR(32);
ALTER TABLE orders ADD COLUMN discount_amount DECIMAL(10,2);
ALTER TABLE orders ADD COLUMN final_price DECIMAL(10,2);
```

## API Endpoints

### Promotion Codes Management

#### Create Promotion Code (Auto-Generated)

```http
POST /promotion-codes/
Content-Type: application/json

{
    "discount_percentage": 15.50,
    "minimum_order_amount": 25.00,
    "max_uses": 100,
    "is_active": true,
    "expiration_date": "2024-12-31T23:59:59"
}
```

#### Create Promotion Code (Custom)

```http
POST /promotion-codes/
Content-Type: application/json

{
    "code": "SAVE15",
    "discount_percentage": 15.50,
    "minimum_order_amount": 25.00,
    "max_uses": 100,
    "is_active": true,
    "expiration_date": "2024-12-31T23:59:59"
}
```

#### Get All Promotion Codes

```http
GET /promotion-codes/?skip=0&limit=100
```

#### Get Promotion Code by ID

```http
GET /promotion-codes/{code_id}
```

#### Update Promotion Code

```http
PUT /promotion-codes/{code_id}
Content-Type: application/json

{
    "discount_percentage": 20.00,
    "is_active": false
}
```

#### Delete Promotion Code

```http
DELETE /promotion-codes/{code_id}
```

#### Validate Promotion Code

```http
POST /promotion-codes/validate
Content-Type: application/json

{
    "code": "SAVE15",
    "order_amount": 50.00
}
```

#### Get Promotion Code by Code String

```http
GET /promotion-codes/code/{code}
```

### Order Promotion Code Integration

#### Apply Promotion Code to Order

```http
POST /orders/{order_id}/apply-promotion?promotion_code=SAVE15
```

#### Remove Promotion Code from Order

```http
DELETE /orders/{order_id}/remove-promotion
```

## Usage Examples

### Creating Auto-Generated Promotion Codes

```python
import requests
from datetime import datetime, timedelta

# Auto-generate code (recommended)
promotion_data = {
    "discount_percentage": 15.50,
    "minimum_order_amount": 25.00,
    "max_uses": 100,
    "is_active": True,
    "expiration_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
}

response = requests.post("http://localhost:8000/promotion-codes/", json=promotion_data)
result = response.json()
print(f"Auto-generated code: {result['code']}")  # e.g., "A7B2K9M4"
```

### Creating Custom Promotion Codes

```python
# Custom code
promotion_data = {
    "code": "SAVE15",
    "discount_percentage": 15.50,
    "minimum_order_amount": 25.00,
    "max_uses": 100,
    "is_active": True,
    "expiration_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
}

response = requests.post("http://localhost:8000/promotion-codes/", json=promotion_data)
```

### Validating a Promotion Code

```python
# Validate without applying
validation_data = {
    "code": "SAVE15",
    "order_amount": 50.00
}

response = requests.post("http://localhost:8000/promotion-codes/validate", json=validation_data)
result = response.json()

if result["is_valid"]:
    print(f"Discount: ${result['discount_amount']}")
    print(f"Final price: ${50.00 - result['discount_amount']}")
else:
    print(f"Invalid: {result['message']}")
```

### Applying Promotion Code to Order

```python
# Apply to existing order
order_id = 123
promotion_code = "SAVE15"

response = requests.post(
    f"http://localhost:8000/orders/{order_id}/apply-promotion",
    params={"promotion_code": promotion_code}
)

result = response.json()
print(f"Original: ${result['original_total']}")
print(f"Discount: ${result['discount_amount']}")
print(f"Final: ${result['final_price']}")
```

## Validation Rules

The system validates promotion codes based on the following rules:

1. **Code Exists**: The promotion code must exist in the database
2. **Active Status**: The code must be marked as active
3. **Not Expired**: The current date must be before the expiration date
4. **Usage Limit**: Current uses must be less than max uses (if set)
5. **Minimum Order**: Order amount must meet minimum requirement (if set)

## Discount Calculation

Discounts are calculated as percentage-based reductions:

```
discount_amount = (order_amount × discount_percentage) / 100
final_price = order_amount - discount_amount
```

## Error Handling

The system provides clear error messages for various scenarios:

- `"Invalid promotion code"` - Code doesn't exist
- `"Promotion code is inactive"` - Code is disabled
- `"Promotion code has expired"` - Past expiration date
- `"Promotion code usage limit reached"` - Max uses exceeded
- `"Minimum order amount of $X required"` - Order too small

## Testing

Run the test suite to verify functionality:

```bash
pytest api/tests/test_orders.py -v
```

Or run the example script:

```bash
python promotion_codes_example.py
```

## Security Considerations

1. **Rate Limiting**: Consider implementing rate limiting on validation endpoints
2. **Code Generation**: Promotion codes are auto-generated with random characters
3. **Usage Tracking**: Each application increments the usage counter
4. **Validation**: All validation happens server-side

## Future Enhancements

Potential improvements to consider:

1. **Stackable Codes**: Allow multiple codes per order
2. **Category Restrictions**: Limit codes to specific product categories
3. **User-Specific Codes**: Codes that only work for specific customers
4. **Bulk Operations**: Create multiple codes at once
5. **Analytics**: Track code performance and usage patterns
6. **Email Integration**: Send codes via email campaigns
