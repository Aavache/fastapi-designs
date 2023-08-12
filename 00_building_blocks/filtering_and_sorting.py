from enum import Enum
from fastapi import FastAPI, HTTPException, Query
from typing import List

app = FastAPI()

# Example data (replace this with your actual data source)
fake_data = [{"id": i, "name": f"Item {i}", "category": f"Category {i % 3 + 1}"} for i in range(1, 101)]

class SortField(str, Enum):
    id = "id"
    name = "name"
    category = "category"

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"

@app.get("/items/", response_model=List[dict])
def get_items(skip: int = Query(0, description="Number of items to skip"),
              limit: int = Query(10, description="Number of items to retrieve"),
              filter_category: str = Query(None, description="Filter items by category"),
              sort_field: SortField = Query(SortField.id, description="Field to sort by"),
              sort_order: SortOrder = Query(SortOrder.asc, description="Sorting order")):
    if skip < 0:
        raise HTTPException(status_code=400, detail="Skip parameter must be non-negative")
    
    if limit <= 0:
        raise HTTPException(status_code=400, detail="Limit parameter must be positive")
    
    start_idx = skip
    end_idx = skip + limit
    
    filtered_items = fake_data
    if filter_category:
        filtered_items = [item for item in filtered_items if item["category"] == filter_category]
    
    reverse_sort = False
    if sort_order == SortOrder.desc:
        reverse_sort = True
    
    sorted_items = sorted(filtered_items, key=lambda x: x[sort_field], reverse=reverse_sort)
    paginated_items = sorted_items[start_idx:end_idx]
    return paginated_items
