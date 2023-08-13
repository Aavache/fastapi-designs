"""Repository pattern tries to separate the data access 
layer from the business logic layer
"""
from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional


app = FastAPI()


class Item:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description


class ItemRepository:
    def __init__(self):
        self.items = {}
        self.next_id = 1
    
    def create_item(self, item: Item) -> int:
        item_id = self.next_id
        self.items[item_id] = item
        self.next_id += 1
        return item_id
    
    def get_item(self, item_id: int) -> Optional[Item]:
        return self.items.get(item_id)
    
    def get_all_items(self) -> List[Item]:
        return list(self.items.values())


item_repository = ItemRepository()


@app.post("/items/")
async def create_item(item: Item):
    item_id = item_repository.create_item(item)
    return {"message": "Item created", "item_id": item_id}


@app.get("/items/{item_id}")
async def get_item(item_id: int = Query(..., description="ID of the item to retrieve")):
    item = item_repository.get_item(item_id)
    if item:
        return item.__dict__
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@app.get("/items/")
async def get_all_items():
    items = item_repository.get_all_items()
    return {"items": [item.__dict__ for item in items]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)