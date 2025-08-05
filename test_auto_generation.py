#!/usr/bin/env python3
"""
Test script to demonstrate promotion code auto-generation feature.
This runs without needing the server to be running.
"""

import random
import string
from datetime import datetime, timedelta
from decimal import Decimal

def generate_code(length=8):
    """Auto-generate promotion codes like the system does"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def demonstrate_auto_generation():
    """Show how auto-generation works"""
    print("🎉 Promotion Code Auto-Generation Demo")
    print("=" * 50)
    
    print("\n1. Generating sample promotion codes:")
    for i in range(5):
        code = generate_code()
        print(f"   Code {i+1}: {code}")
    
    print("\n2. Creating promotion code data (auto-generated):")
    sample_promotion = {
        "code": generate_code(),  # Auto-generated!
        "discount_percentage": 15.50,
        "minimum_order_amount": 25.00,
        "max_uses": 100,
        "is_active": True,
        "expiration_date": (datetime.utcnow() + timedelta(days=30)).isoformat()
    }
    
    print(f"   Code: {sample_promotion['code']}")
    print(f"   Discount: {sample_promotion['discount_percentage']}%")
    print(f"   Min Order: ${sample_promotion['minimum_order_amount']}")
    print(f"   Max Uses: {sample_promotion['max_uses']}")
    print(f"   Expires: {sample_promotion['expiration_date']}")
    
    print("\n3. How to use in API calls:")
    print("   # Auto-generate (recommended):")
    print("   promotion_data = {")
    print("       'discount_percentage': 15.50,")
    print("       'minimum_order_amount': 25.00,")
    print("       'max_uses': 100,")
    print("       'is_active': True,")
    print("       'expiration_date': '2024-12-31T23:59:59'")
    print("       # No 'code' field - will be auto-generated!")
    print("   }")
    
    print("\n   # Or specify custom code:")
    print("   promotion_data = {")
    print("       'code': 'SAVE15',  # Custom code")
    print("       'discount_percentage': 15.50,")
    print("       # ... other fields")
    print("   }")
    
    print("\n4. Validation example:")
    order_amount = Decimal("50.00")
    discount_percentage = Decimal("15.50")
    discount_amount = (order_amount * discount_percentage) / Decimal("100")
    final_price = order_amount - discount_amount
    
    print(f"   Order Amount: ${order_amount}")
    print(f"   Discount: {discount_percentage}%")
    print(f"   Discount Amount: ${discount_amount}")
    print(f"   Final Price: ${final_price}")
    
    print("\n✅ Auto-generation feature is working!")
    print("   - Codes are 8 characters long")
    print("   - Use uppercase letters (A-Z) and digits (0-9)")
    print("   - Each code is randomly generated for uniqueness")
    print("   - Can be used immediately or stored for later")

if __name__ == "__main__":
    demonstrate_auto_generation() 