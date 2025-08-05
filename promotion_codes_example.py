#!/usr/bin/env python3
"""
Example script demonstrating the promotion codes system for payments.
This script shows how to create, validate, and apply promotion codes to orders.
"""

import requests
import json
from datetime import datetime, timedelta
from decimal import Decimal

# Base URL for the API
BASE_URL = "http://localhost:8000"

def create_promotion_code_auto():
    """Create a new promotion code with auto-generated code"""
    url = f"{BASE_URL}/promotion-codes/"
    
    # Create a promotion code WITHOUT specifying code (auto-generated)
    promotion_data = {
        # No "code" field - will be auto-generated!
        "discount_percentage": 15.50,  # 15.5% discount
        "minimum_order_amount": 25.00,  # Minimum $25 order
        "max_uses": 100,  # Can be used up to 100 times
        "is_active": True,
        "expiration_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
    }
    
    response = requests.post(url, json=promotion_data)
    
    if response.status_code == 201:
        result = response.json()
        print("✅ Auto-generated promotion code created successfully!")
        print(f"Auto-generated Code: {result['code']}")
        print(f"Discount: {result['discount_percentage']}%")
        print(f"Minimum order: ${result['minimum_order_amount']}")
        return result
    else:
        print(f"❌ Failed to create auto-generated promotion code: {response.text}")
        return None

def create_promotion_code_custom():
    """Create a new promotion code with custom code"""
    url = f"{BASE_URL}/promotion-codes/"
    
    # Create a promotion code with custom code
    promotion_data = {
        "code": "SAVE15",  # Custom code
        "discount_percentage": 20.00,  # 20% discount
        "minimum_order_amount": 30.00,  # Minimum $30 order
        "max_uses": 50,  # Can be used up to 50 times
        "is_active": True,
        "expiration_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
    }
    
    response = requests.post(url, json=promotion_data)
    
    if response.status_code == 201:
        result = response.json()
        print("✅ Custom promotion code created successfully!")
        print(f"Custom Code: {result['code']}")
        print(f"Discount: {result['discount_percentage']}%")
        print(f"Minimum order: ${result['minimum_order_amount']}")
        return result
    else:
        print(f"❌ Failed to create custom promotion code: {response.text}")
        return None

def validate_promotion_code(code, order_amount):
    """Validate a promotion code without applying it"""
    url = f"{BASE_URL}/promotion-codes/validate"
    
    validation_data = {
        "code": code,
        "order_amount": float(order_amount)
    }
    
    response = requests.post(url, json=validation_data)
    
    if response.status_code == 200:
        result = response.json()
        if result["is_valid"]:
            print(f"✅ Code '{code}' is valid!")
            print(f"Discount: ${result['discount_amount']}")
            print(f"Message: {result['message']}")
        else:
            print(f"❌ Code '{code}' is invalid: {result['message']}")
        return result
    else:
        print(f"❌ Validation failed: {response.text}")
        return None

def create_order_with_promotion():
    """Create an order and apply a promotion code"""
    # First create an order
    order_url = f"{BASE_URL}/orders/"
    order_data = {
        "customer_name": "John Doe",
        "description": "Order with promotion code",
        "total_price": 50.00
    }
    
    response = requests.post(order_url, json=order_data)
    
    if response.status_code == 200:
        order = response.json()
        order_id = order["id"]
        print(f"✅ Order created with ID: {order_id}")
        
        # Apply promotion code to the order
        promotion_url = f"{BASE_URL}/orders/{order_id}/apply-promotion"
        promotion_code = "SAVE15"  # Use the custom code we created
        
        response = requests.post(promotion_url, params={"promotion_code": promotion_code})
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Promotion code applied successfully!")
            print(f"Original total: ${result['original_total']}")
            print(f"Discount amount: ${result['discount_amount']}")
            print(f"Final price: ${result['final_price']}")
            print(f"Applied code: {result['promotion_code']}")
        else:
            print(f"❌ Failed to apply promotion code: {response.text}")
    else:
        print(f"❌ Failed to create order: {response.text}")

def list_promotion_codes():
    """List all available promotion codes"""
    url = f"{BASE_URL}/promotion-codes/"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        codes = response.json()
        print(f"📋 Found {len(codes)} promotion codes:")
        for code in codes:
            print(f"  - {code['code']}: {code['discount_percentage']}% off")
            print(f"    Min order: ${code['minimum_order_amount']}")
            print(f"    Uses: {code['current_uses']}/{code['max_uses']}")
            print(f"    Active: {code['is_active']}")
            print(f"    Expires: {code['expiration_date']}")
            print()
    else:
        print(f"❌ Failed to get promotion codes: {response.text}")

def main():
    """Main function to demonstrate the promotion codes system"""
    print("🎉 Promotion Codes System Demo")
    print("=" * 40)
    
    # Step 1: Create auto-generated promotion code
    print("\n1. Creating auto-generated promotion code...")
    auto_code = create_promotion_code_auto()
    
    # Step 2: Create custom promotion code
    print("\n2. Creating custom promotion code...")
    custom_code = create_promotion_code_custom()
    
    if auto_code and custom_code:
        auto_code_str = auto_code["code"]
        custom_code_str = custom_code["code"]
        
        # Step 3: Validate both codes
        print(f"\n3. Validating auto-generated code '{auto_code_str}'...")
        validate_promotion_code(auto_code_str, 50.00)
        
        print(f"\n4. Validating custom code '{custom_code_str}'...")
        validate_promotion_code(custom_code_str, 50.00)
        
        # Step 5: Try with insufficient order amount
        print(f"\n5. Testing minimum order amount...")
        validate_promotion_code(custom_code_str, 10.00)
        
        # Step 6: Create order and apply promotion
        print(f"\n6. Creating order and applying promotion...")
        create_order_with_promotion()
        
        # Step 7: List all promotion codes
        print(f"\n7. Listing all promotion codes...")
        list_promotion_codes()

if __name__ == "__main__":
    main() 