"""Here we show how to implement authentication in FastAPI using JWT tokens.
There are 2 types of authentication:
    - API Key Header: a simple API key based authentication mechanism
    - OAuth2 Password: a token based authentication mechanism
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta


app = FastAPI()

# Simulated database of users and hashed passwords
fake_users_db = {
    "testuser": {
        "username": "testuser",
        "password": "$2b$12$02vBQ5MfG/LbXGBUc7BevejQdQR3FLJ/aS1oA/61d7jibzK3R0nL.",
        "disabled": False,
    }
}

# Security configuration, ideally you could store 
# these in environment variables
SECRET_KEY = "secret_key_here"
ALGORITHM = "HS256"
API_KEY = "supersecretapikey"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# API Key Header
api_key_header = APIKeyHeader(name="X-API-Key")
# OAuth2 Password Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expires_delta: timedelta):
    """Generate JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class User(BaseModel):
    """User model"""
    username: str


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """OAuth2 Password Bearer dependency"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = {"username": username}
    except JWTError:
        raise credentials_exception
    return User(**token_data)


async def get_api_key(api_key: str = Depends(api_key_header)):
    """API Key dependency"""
    if api_key != API_KEY:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return api_key


@app.get("/api-key-protected")
def api_key_protected(api_key: str = Depends(get_api_key)):
    """Endpoint with API key authorization"""
    return {"message": "API key authorized"}


@app.get("/token-protected")
def token_protected(current_user: User = Depends(get_current_user)):
    """Endpoint with OAuth2 token authorization"""
    return {"message": f"Hello, {current_user.username}"}


@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Token endpoint"""
    user = fake_users_db.get(form_data.username)
    if user is None or not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)