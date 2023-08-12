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

# Security configuration
SECRET_KEY = "secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# API Key Header
api_key_header = APIKeyHeader(name="X-API-Key")

# OAuth2 Password Bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Generate JWT token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# User model
class User(BaseModel):
    username: str

# OAuth2 Password Bearer dependency
async def get_current_user(token: str = Depends(oauth2_scheme)):
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

# API Key dependency
async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != "supersecretapikey":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return api_key

# Endpoint with API key authorization
@app.get("/api-key-protected")
def api_key_protected(api_key: str = Depends(get_api_key)):
    return {"message": "API key authorized"}

# Endpoint with OAuth2 token authorization
@app.get("/token-protected")
def token_protected(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello, {current_user.username}"}

# Token endpoint
@app.post("/token")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form_data.username)
    if user is None or not pwd_context.verify(form_data.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

