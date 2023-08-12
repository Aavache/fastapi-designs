from fastapi import FastAPI, HTTPException

app = FastAPI()

class CustomException(HTTPException):
    def __init__(self, status_code: int, detail: str, error_code: str):
        self.error_code = error_code
        super().__init__(status_code=status_code, detail=detail)

@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.error_code, "message": exc.detail},
    )

@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id == 42:
        raise CustomException(status_code=400, detail="Item not found", error_code="item_not_found")
    return {"item_id": item_id}
