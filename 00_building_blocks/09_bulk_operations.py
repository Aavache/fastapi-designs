"""
The route supports bulk operations for creating 
or updating item

Send the following request to the API:
[
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
    {"id": 3, "name": "Item 3"}
]

The response will be as follows: 

[
    {"id": 1, "action": "created/updated"},
    {"id": 2, "action": "created/updated"},
    {"id": 3, "action": "created/updated"}
]
"""
from fastapi import FastAPI, HTTPException, Body
from typing import List

app = FastAPI()

# Simulated data storage
items_db = {}


@app.post("/bulk/items/")
def bulk_create_update_items(items: List[dict] = Body(...)):
    """Create or update items using bulk operations"""
    response = []
    
    for item in items:
        item_id = item.get("id")
        if item_id is None:
            raise HTTPException(status_code=400, detail="Item ID is required")
        
        items_db[item_id] = item
        response.append({"id": item_id, "action": "created/updated"})
    
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
