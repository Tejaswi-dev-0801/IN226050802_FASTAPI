# FastAPI Product API Assignment

## Project Overview

This project is a **FastAPI-based E-Commerce Product API**.
The API simulates a small online store where users can:

* View products
* Filter products by category or price
* Check stock availability
* Submit customer feedback
* View store/product summaries
* Place bulk corporate orders
* Track order status

---

# Tech Stack

* **Python 3**
* **FastAPI**
* **Pydantic**
* **Uvicorn**

---

# How to Run the Project

### 1. Install Dependencies

```bash
pip install fastapi uvicorn pydantic
```

### 2. Run the Server

```bash
uvicorn main:app --reload
```

### 3. Open API Documentation

Swagger UI:

```
http://127.0.0.1:8000/docs
```

This interface is used to test all **POST, PATCH, and GET endpoints**.

---

# API Endpoints

## Basic Endpoints

### Home

```
GET /
```

Returns a message confirming the API is running.

---

### Get All Products

```
GET /products
```

Returns all products in the store.

---

### Filter Products by Category

```
GET /products/category/{category}
```

Example:

```
/products/category/Electronics
```

---

### Get In-Stock Products

```
GET /products/instock
```

Returns only products currently available.

---

### Store Summary

```
GET /store/summary
```

Returns:

* Total products
* In-stock count
* Out-of-stock count
* Product categories

---

### Search Products

```
GET /products/search/{keyword}
```

Example:

```
/products/search/mouse
```

---

### Product Deals

```
GET /products/deals
```

Returns:

* Cheapest product
* Most expensive product

---


## Filter Products by Price

```
GET /products/filter
```

Query Parameters:

* `category`
* `max_price`
* `min_price`

---

## Get Product Price Only

```
GET /products/{product_id}/price
```

---

## Customer Feedback

```
POST /feedback
```

## Product Summary Dashboard

```
GET /products/summary
```

Returns:

* Total products
* In-stock products
* Out-of-stock products
* Cheapest product
* Most expensive product
* Categories

---

## Bulk Order API

```
POST /orders/bulk
```

---

## Order Status Tracker

### Create Order

```
POST /orders
```

New orders start with status:

```
pending
```

---

### Get Order by ID

```
GET /orders/{order_id}
```

---

### Confirm Order

```
PATCH /orders/{order_id}/confirm
```

Changes status:

```
pending → confirmed
```

---