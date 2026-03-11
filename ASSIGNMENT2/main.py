# FastAPI Day 1 Assignment - Product API
from fastapi import FastAPI
from fastapi import Query
from pydantic import BaseModel, Field
from typing import Optional, List

# Create FastAPI application
app = FastAPI(title="E-Commerce Product API", version="1.0")

# -----------------------------
# Product Database
# -----------------------------
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 599, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "Notebook", "price": 120, "category": "Stationery", "in_stock": True},
    {"id": 3, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": False},
    {"id": 4, "name": "USB Charger", "price": 399, "category": "Electronics", "in_stock": True},

    # Added Products with ids 5,6,7
    {"id": 5, "name": "Laptop Stand", "price": 999, "category": "Electronics", "in_stock": True},
    {"id": 6, "name": "Mechanical Keyboard", "price": 2499, "category": "Electronics", "in_stock": True},
    {"id": 7, "name": "Webcam", "price": 1299, "category": "Electronics", "in_stock": False},
]


# -----------------------------
# Home Route
# -----------------------------
@app.get("/")
def home():
    return {"message": "FastAPI Store Running"}


# -----------------------------
# Q1 - Get All Products
# -----------------------------
@app.get("/products")
def get_products():
    return {"products": products, "total": len(products)}


# -----------------------------
# Q2 - Filter by Category
# -----------------------------
@app.get("/products/category/{category}")
def category_filter(category: str):
    result = [p for p in products if p["category"].lower() == category.lower()]
    return {"products": result, "count": len(result)} if result else {"error": "No products found in this category"}


# -----------------------------
# Q3 - In Stock Products
# -----------------------------
@app.get("/products/instock")
def instock_products():
    instock = [p for p in products if p["in_stock"]]
    return {"in_stock_products": instock, "count": len(instock)}


# -----------------------------
# Q4 - Store Summary
# -----------------------------
@app.get("/store/summary")
def store_summary():
    instock = [p for p in products if p["in_stock"]]

    return {
        "store_name": "My E-commerce Store",
        "total_products": len(products),
        "in_stock": len(instock),
        "out_of_stock": len(products) - len(instock),
        "categories": list({p["category"] for p in products})
    }


# -----------------------------
# Q5 - Search Products
# -----------------------------
@app.get("/products/search/{keyword}")
def search(keyword: str):
    matches = [p for p in products if keyword.lower() in p["name"].lower()]
    return {"matches": matches, "count": len(matches)} if matches else {"message": "No products matched your search"}


# -----------------------------
# Product Deals
# -----------------------------
@app.get("/products/deals")
def deals():
    return {
        "best_deal": min(products, key=lambda x: x["price"]),
        "premium_pick": max(products, key=lambda x: x["price"])
    }

# Filter Products by Query

@app.get("/products/filter")
def filter_products(
    category: Optional[str] = None,
    max_price: Optional[int] = None,
    min_price: Optional[int] = None
):
    filtered = products

    if category:
        filtered = [p for p in filtered if p["category"].lower() == category.lower()]

    if max_price is not None:
        filtered = [p for p in filtered if p["price"] <= max_price]

    if min_price is not None:
        filtered = [p for p in filtered if p["price"] >= min_price]

    return {"products": filtered, "count": len(filtered)}


#Get Only Product Price
@app.get("/products/{product_id}/price")
def get_product_price(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return {
                "name": p["name"],
                "price": p["price"]
            }

    return {"error": "Product not found"}


# Customer Feedback
class CustomerFeedback(BaseModel):
    customer_name: str = Field(..., min_length=2)
    product_id: int = Field(..., gt=0)
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = Field(None, max_length=300)


feedback = []


@app.post("/feedback")
def submit_feedback(data: CustomerFeedback):
    feedback.append(data.dict())

    return {
        "message": "Feedback submitted successfully",
        "feedback": data,
        "total_feedback": len(feedback)
    }


#Product Summary Dashboard
@app.get("/products/summary")
def product_summary():

    instock = [p for p in products if p["in_stock"]]
    outstock = [p for p in products if not p["in_stock"]]

    cheapest = min(products, key=lambda x: x["price"])
    expensive = max(products, key=lambda x: x["price"])

    return {
        "total_products": len(products),
        "in_stock_count": len(instock),
        "out_of_stock_count": len(outstock),
        "most_expensive": {
            "name": expensive["name"],
            "price": expensive["price"]
        },
        "cheapest": {
            "name": cheapest["name"],
            "price": cheapest["price"]
        },
        "categories": list({p["category"] for p in products})
    }

# Bulk Orders
class OrderItem(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1, le=50)


class BulkOrder(BaseModel):
    company_name: str = Field(..., min_length=2)
    contact_email: str = Field(..., min_length=5)
    items: List[OrderItem] = Field(..., min_items=1)


@app.post("/orders/bulk")
def bulk_order(order: BulkOrder):

    confirmed = []
    failed = []
    grand_total = 0

    for item in order.items:

        product = next((p for p in products if p["id"] == item.product_id), None)

        if not product:
            failed.append({
                "product_id": item.product_id,
                "reason": "Product not found"
            })
            continue

        if not product["in_stock"]:
            failed.append({
                "product_id": item.product_id,
                "reason": f"{product['name']} is out of stock"
            })
            continue

        subtotal = product["price"] * item.quantity
        grand_total += subtotal

        confirmed.append({
            "product": product["name"],
            "qty": item.quantity,
            "subtotal": subtotal
        })

    return {
        "company": order.company_name,
        "confirmed": confirmed,
        "failed": failed,
        "grand_total": grand_total
    }


#Order Status Tracker

orders = []


class SimpleOrder(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., ge=1)


@app.post("/orders")
def create_order(order: SimpleOrder):

    new_order = {
        "order_id": len(orders) + 1,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "status": "pending"
    }

    orders.append(new_order)

    return new_order


@app.get("/orders/{order_id}")
def get_order(order_id: int):

    for order in orders:
        if order["order_id"] == order_id:
            return order

    return {"error": "Order not found"}


@app.patch("/orders/{order_id}/confirm")
def confirm_order(order_id: int):

    for order in orders:
        if order["order_id"] == order_id:
            order["status"] = "confirmed"
            return order

    return {"error": "Order not found"}