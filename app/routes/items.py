from typing import Union, List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from app.db.models import Item as ItemModel
from app.db.dependency import get_session

# Create a router instance
router = APIRouter()

# Define a Pydantic model for an Item with detailed validation and metadata
class Item(BaseModel):
    # DB unique id
    id: int = None
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
    # Configuration for the Pydantic model
    class Config:
        orm_mode = True
        extra = "forbid"

# Define an endpoint to read an item by its ID, with an optional query parameter
@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int, session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(select(ItemModel).where(ItemModel.id == item_id))
        item = result.scalars().one()
        return item
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Item not found")

# Define an endpoint to create an item with Pydantic validation
@router.post("/", response_model=Item)
async def create_item(item: Item, session: AsyncSession = Depends(get_session)):
    new_item = ItemModel(name=item.name, price=item.price, in_stock=item.in_stock)
    session.add(new_item)
    await session.commit()
    await session.refresh(new_item)
    return new_item
