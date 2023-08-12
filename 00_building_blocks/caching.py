from fastapi import FastAPI, Depends, HTTPException
from fastapi.cache import caches, Cache
from datetime import datetime, timedelta

app = FastAPI()

# In-memory cache instance
cache = caches.get_cache("default")

# Cache expiration time
CACHE_EXPIRE_SECONDS = 60

# Custom dependency to fetch data
def fetch_data_from_database():
    # Simulated data retrieval from a database
    return {"data": "This is some data from the database."}

# Route to fetch and cache data
@app.get("/cached-data")
def get_cached_data(cache: Cache = Depends(cache), fresh: bool = False):
    cache_key = "cached_data"
    
    if fresh:
        data = fetch_data_from_database()
        cache.set(cache_key, data, expire=CACHE_EXPIRE_SECONDS)
        return {"message": "Data fetched from database and cached.", "data": data}
    
    cached_data = cache.get(cache_key)
    if cached_data is None:
        data = fetch_data_from_database()
        cache.set(cache_key, data, expire=CACHE_EXPIRE_SECONDS)
        return {"message": "Data fetched from database and cached.", "data": data}
    
    return {"message": "Data fetched from cache.", "data": cached_data}
