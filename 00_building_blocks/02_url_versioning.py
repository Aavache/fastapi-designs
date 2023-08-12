from fastapi import FastAPI


app = FastAPI()


@app.get("/v1/items/")
def get_items_v1():
    """Response when version is v1"""
    # The response is hardcoded for simplicity
    return {"version": "v1", "items": ["item1", "item2"]}


@app.get("/v2/items/")
def get_items_v2():
    """Response when version is v2"""
    # The response is hardcoded for simplicity
    return {"version": "v2", "items": [{"name": "item1"}, {"name": "item2"}]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)