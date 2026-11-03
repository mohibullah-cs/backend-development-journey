from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str = Field(min_length=2, max_length=50)
    price: float = Field(gt=0)
    quantity: int = Field(ge=1)
    description: str | None = None
