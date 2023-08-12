from fastapi import FastAPI, HTTPException, Query
from typing import List

app = FastAPI()

# Example data (replace this with your actual data source)
fake_data = [{"id": i, "name": f"Item {i}"} for i in range(1, 101)]

@app.get("/items/", response_model=List[dict])
def get_items(skip: int = Query(0, description="Number of items to skip"),
              limit: int = Query(10, description="Number of items to retrieve")):
    if skip < 0:
        raise HTTPException(status_code=400, detail="Skip parameter must be non-negative")
    
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit parameter must be positive")
    
    start_idx = skip
    end_idx = skip + limit
    
    items = fake_data[start_idx:end_idx]
    return items
