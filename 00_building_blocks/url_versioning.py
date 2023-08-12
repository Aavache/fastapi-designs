from fastapi import FastAPI

app = FastAPI()

@app.get("/v1/items/")
def get_items_v1():
    return {"version": "v1", "items": ["item1", "item2"]}

@app.get("/v2/items/")
def get_items_v2():
    return {"version": "v2", "items": [{"name": "item1"}, {"name": "item2"}]}
