"""There are many options for caching, in this script we go for a
simple approach using in-memory LRU cache. For more options, see:
- https://github.com/tkem/cachetools/
- https://github.com/long2ice/fastapi-cache
- https://github.com/comeuplater/fastapi_cache
"""
from fastapi import FastAPI
from functools import lru_cache

app = FastAPI()

def fetch_data(item_id: int):
    """Function to fetch data (simulated)"""
    print("Fetching data...")
    return f"Data for item {item_id}"


@app.get("/get_data/{item_id}")
@lru_cache(maxsize=100)
async def get_data(item_id: int):
    """Cached endpoint using lru_cache"""
    return fetch_data(item_id)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)