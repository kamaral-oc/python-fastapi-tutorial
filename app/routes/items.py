from typing import Union
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

# Create a router instance
router = APIRouter()

# Define a Pydantic model for an Item with detailed validation and metadata
class Item(BaseModel):
    # Required field with a maximum length of 50 characters
    name: str = Field(
        ..., 
        title="Name of the item", 
        max_length=50, 
        description="The name must be at most 50 characters long"
    )
    # Required field with a value greater than zero
    price: float = Field(
        ..., 
        gt=0, 
        description="Price must be greater than zero"
    )
    # Optional field with a default value of None
    in_stock: Union[bool, None] = Field(
        None, 
        description="Stock availability"
    )
    # Configuration for the Pydantic model to forbid extra fields
    class Config:
        extra = "forbid"

# Define an endpoint to read an item by its ID, with an optional query parameter
@router.get("/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Define an endpoint to create an item with Pydantic validation
@router.post("/")
async def create_item(item: Item):
    if item.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than zero")
    return item
