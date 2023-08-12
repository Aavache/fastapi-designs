from fastapi import FastAPI, HTTPException, Request

app = FastAPI()

@app.post("/rpc")
async def rpc_endpoint(request: Request):
    content = await request.json()

    method = content.get("method")
    params = content.get("params")

    if method == "add":
        if "a" not in params or "b" not in params:
            raise HTTPException(status_code=400, detail="Invalid params")
        result = params["a"] + params["b"]
    elif method == "subtract":
        if "a" not in params or "b" not in params:
            raise HTTPException(status_code=400, detail="Invalid params")
        result = params["a"] - params["b"]
    else:
        raise HTTPException(status_code=400, detail="Invalid method")

    response = {"result": result}
    return response
