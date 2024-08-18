from fastapi import APIRouter, HTTPException
from app.service_item import ItemService
from app.models import Item, ItemDto
from app.exceptions import ItemNotFoundException, ItemAlreadyExistsException, InvalidItemDataException
from typing import List

router = APIRouter()

item_service = ItemService()

@router.post("/items/", response_model=Item)
def create_item(item: ItemDto):
    try:
        new_item = item_service.create_item(item)
        return new_item
    except ItemAlreadyExistsException as e:
        raise HTTPException(status_code=400, detail=str(e))
    except InvalidItemDataException as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    try:
        return item_service.get_item(item_id)
    except ItemNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/items/", response_model=List[Item])
def get_all_items():
    return item_service.get_all_items()

@router.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemDto):
    try:
        return item_service.update_item(item_id, item)
    except ItemNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except InvalidItemDataException as e:
        raise HTTPException(status_code=422, detail=str(e))

@router.delete("/items/{item_id}", response_model=bool)
def delete_item(item_id: int):
    try:
        return item_service.delete_item(item_id)
    except ItemNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))