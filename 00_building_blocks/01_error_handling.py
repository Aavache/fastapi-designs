"""Implementation of a custom exception handler"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse


app = FastAPI()


# Dummy items that are not available
UNAVAILABLE_ITEMS = {42, 43, 44, 45}


class CustomException(HTTPException):
    """Definition of the Exception class"""
    def __init__(self, status_code: int, detail: str, error_code: str):
        self.error_code = error_code
        super().__init__(status_code=status_code, detail=detail)


@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc):
    """Exception from the CustomException is handled here"""
    return JSONResponse(
        status_code=exc.status_code,
        # Error code comes from our custom exception
        content={"error": exc.error_code, 
                 "message": exc.detail
        },
    )


@app.get("/items/{item_id}")
def read_item(item_id: int):
    """GET endpoint that raises the CustomException when
    item_id is the UNAVAILABLE_ITEMS set
    """
    if item_id in UNAVAILABLE_ITEMS:
        raise CustomException(status_code=400, detail="Item not found", error_code="item_not_found")
    return {"item_id": item_id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)