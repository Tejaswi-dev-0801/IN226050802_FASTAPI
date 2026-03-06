# FastAPI Day 1 Assignment - Product API
from fastapi import FastAPI

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