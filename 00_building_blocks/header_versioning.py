from fastapi import FastAPI, Header, HTTPException

app = FastAPI()

@app.get("/items/")
def get_items(version: str = Header(None)):
    if version == "v1":
        return {"version": "v1", "items": ["item1", "item2"]}
    elif version == "v2":
        return {"version": "v2", "items": [{"name": "item1"}, {"name": "item2"}]}
    else:
        raise HTTPException(status_code=400, detail="Invalid version specified")
