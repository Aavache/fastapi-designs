"""Deprecation warning example"""
from fastapi import FastAPI, HTTPException, status


app = FastAPI()

# Simulated database
data = {1: "1", 2: "2"}


@app.get("/v1/items/{item_id}")
async def read_item_v1(item_id: int):
    if item_id not in data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return {"item": data[item_id], "version": "v1 (Deprecated)"}


@app.get("/v2/items/{item_id}")
async def read_item_v2(item_id: int):
    if item_id not in data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return {"item": data[item_id], "version": "v2"}


@app.on_event("startup")
async def startup_event():
    print("API is starting up")


@app.on_event("shutdown")
async def shutdown_event():
    print("API is shutting down")


@app.middleware("http")
async def deprecation_warning(request, call_next):
    """Add a warning header to all requests to deprecated endpoints"""
    response = await call_next(request)
    if "/v1/" in request.url.path:
        warning_message = "This version is deprecated and will be removed soon. Please use the latest version."
        response.headers["Warning"] = f"299 - \"Deprecation Warning: {warning_message}\""
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)