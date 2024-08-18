from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ItemDto(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=1000)
    price: Optional[float] = Field(None, gt=0, description="The price must be greater than zero")
    qtty: Optional[float] = Field(None, ge=0, description="The quantity must be zero or greater")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Sample Item",
                "description": "This is a sample item description",
                "price": 19.99,
                "qtty": 5
            }
        }
    )

class Item(ItemDto):
    id: int = Field(..., gt=0)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Sample Item",
                "description": "This is a sample item description",
                "price": 19.99,
                "qtty": 5
            }
        }
    )