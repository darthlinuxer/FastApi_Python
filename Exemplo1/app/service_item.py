from typing import List
from app.models import Item, ItemDto
from app.exceptions import ItemNotFoundException, ItemAlreadyExistsException, InvalidItemDataException

class ItemService:
    def __init__(self):
        self.items: dict[int, Item] = {}
        self.next_id = 1

    def create_item(self, item_data: ItemDto) -> Item:
        if any(item.name == item_data.name for item in self.items.values()):
            raise ItemAlreadyExistsException("Item with this name already exists")
        
        new_item = Item(id=self.next_id, **item_data.model_dump())
        self.items[self.next_id] = new_item
        self.next_id += 1
        return new_item

    def get_item(self, item_id: int) -> Item:
        item = self.items.get(item_id)
        if not item:
            raise ItemNotFoundException(f"Item with id {item_id} not found")
        return item

    def update_item(self, item_id: int, item_data: ItemDto) -> Item:
        if item_id not in self.items:
            raise ItemNotFoundException(f"Item with id {item_id} not found")
        
        current_item = self.items[item_id]
        update_data = item_data.model_dump(exclude_unset=True) # Extract only the provided fields
         # Merge current item data with update data
        updated_data = current_item.model_dump()
        updated_data.update(update_data)
        updated_item = Item(**updated_data)
        
        if updated_item.qtty < 0 or updated_item.price <= 0:
            raise InvalidItemDataException("Quantity cannot be less than zero and price must be greater than zero")

        self.items[item_id] = updated_item
        return updated_item

    def delete_item(self, item_id: int) -> bool:
        if item_id not in self.items:
            raise ItemNotFoundException(f"Item with id {item_id} not found")
        del self.items[item_id]
        return True

    def get_all_items(self) -> List[Item]:
        return list(self.items.values())