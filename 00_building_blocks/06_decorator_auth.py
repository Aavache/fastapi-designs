from fastapi import FastAPI


app = FastAPI()


def authenticate(func):
    """Custom decorator to authenticate requests"""
    def wrapper(*args, **kwargs):
        token = kwargs.get("token")
        if token == "secret_token":
            return func(*args, **kwargs)
        else:
            return {"message": "Authentication failed"}
    return wrapper


@app.get("/secure_data")
@authenticate
async def secure_data(token: str):
    """This endpoint is secured with a decorator"""
    return {"data": "This is secure data"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
