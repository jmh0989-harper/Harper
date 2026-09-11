order = {
    "order_id": "ORD-1001",
    "quantity": 3,
    "unit_price": 20,
    "total_price": 60,
    "country_code": "US"
}

valid_countries = ["US", "CA", "MX", "GB"]
errors = []

try:
    #number 1
    # 1. Data type validation
    if not isinstance(order["quantity"], int):
        errors.append("Quantity must be an integer")

    # 2. Range and constraint validation (nested if)
    if isinstance(order["quantity"], int):
        if order["quantity"] <= 0:
            errors.append("Quantity must be greater than 0")

    # 3. Code and cross-reference validation
    if order["country_code"] not in valid_countries:
        errors.append("Invalid country code")

    # 4. Consistency validation
    if order["total_price"] != order["quantity"] * order["unit_price"]:
        errors.append("Total price doesn't match quantity x unit price")
#Number 2
except KeyError as e:
    errors.append(f"Missing field in order: {e}")
except TypeError as e:
    errors.append(f"Type error during validation: {e}")

# Number 3
if errors:
    print("Invalid order:", errors)
else:
    print("Valid order!")
#https://claude.ai/chat/19f1be3f-6b0f-4ee4-bc36-8ae29f1f7545