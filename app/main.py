from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Create an instance of the FastAPI application
app = FastAPI()

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
    is_offer: Union[bool, None] = Field(
        None, 
        description="Whether the item is an offer"
    )

# Define a root endpoint that returns a greeting message
@app.get("/")
def read_root():
    return {"Hello": "World"}

# Define an endpoint to read an item by its ID, with an optional query parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Define an endpoint to create an item with Pydantic validation
@app.post("/items/")
async def create_item(item: Item):
    # Perform additional validation (this is redundant since Pydantic already checks this)
    if item.price <= 0:
        raise HTTPException(status_code=400, detail="Price must be greater than zero")
    # Return the validated item
    return item
