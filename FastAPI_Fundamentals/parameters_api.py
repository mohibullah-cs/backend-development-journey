from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="FastAPI Parameters API",
    description="Learning FastAPI parameters and Pydantic models",
    version="1.0"
)


class Product(BaseModel):
    name: str
    price: float = Field(gt=0)
    category: str
    in_stock: bool = True


products = {
    1: {
        "name": "Chocolate Cookies",
        "price": 500,
        "category": "Bakery",
        "in_stock": True
    }
}


# Path Parameter
@app.get("/products/{product_id}")
def get_product(product_id: int):
    return {
        "product_id": product_id,
        "product": products.get(product_id, "Product not found")
    }


# Query Parameter
@app.get("/search")
def search_products(category: str, max_price: float = 1000):
    return {
        "category": category,
        "maximum_price": max_price
    }


# Request Body and Pydantic Model
@app.post("/products")
def create_product(product: Product):
    return {
        "message": "Product created successfully",
        "product": product
    }
