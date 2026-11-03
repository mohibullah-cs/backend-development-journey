from fastapi import FastAPI
from schemas import Item

app = FastAPI()


# Path Parameters
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {
        "item_id": item_id,
        "message": "Item retrieved successfully"
    }


# Query Parameters
@app.get("/search")
def search_items(keyword: str, limit: int = 5):
    return {
        "keyword": keyword,
        "limit": limit
    }


# Request Body
@app.post("/items")
def create_item(item: Item):
    return {
        "message": "Item created successfully",
        "item": item
    }
