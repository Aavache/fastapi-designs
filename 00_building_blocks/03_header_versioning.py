"""Header versioning, this a better approach than URL versioning
as the actual address doesn't change
"""
from fastapi import FastAPI, Header, HTTPException


app = FastAPI()


@app.get("/items/")
def get_items(version: str = Header(None)):
    """Version is given by a query parameter"""
    if version == "v1":
        # v1 returns a list of strings
        return {"version": "v1", "items": ["item1", "item2"]}
    elif version == "v2":
        # v2 returns a list of dictionaries
        return {"version": "v2", "items": [{"name": "item1"}, {"name": "item2"}]}
    else:
        raise HTTPException(status_code=400, detail="Invalid version specified")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)