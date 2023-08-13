"""Limiting the number of requests a client can make to an endpoint"""
from fastapi import FastAPI, HTTPException
from fastapi.security import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from datetime import datetime, timedelta


app = FastAPI()
# API Key Header
api_key_header = APIKeyHeader(name="X-API-Key")

# Simulated API keys and usage tracking
api_keys = {"supersecretapikey": {"rate_limit": 5, "reset_interval": timedelta(minutes=1)}}
api_usage = {}


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate Limiting Middleware"""
    async def dispatch(self, request, call_next):
        api_key = request.headers.get("x-api-key")
        if api_key:
            key_info = api_keys.get(api_key)
            if key_info:
                now = datetime.now()
                if api_key not in api_usage or now > api_usage[api_key]["reset_time"]:
                    api_usage[api_key] = {"count": 0, "reset_time": now + key_info["reset_interval"]}
                if api_usage[api_key]["count"] < key_info["rate_limit"]:
                    api_usage[api_key]["count"] += 1
                    response = await call_next(request)
                    return response
                else:
                    reset_time = api_usage[api_key]["reset_time"]
                    wait_time = (reset_time - now).seconds
                    raise HTTPException(status_code=429, detail=f"Rate limit exceeded. Please try again in {wait_time} seconds.")
            else:
                raise HTTPException(status_code=401, detail="Invalid API key")
        else:
            raise HTTPException(status_code=401, detail="API key required")


# Apply Rate Limiting Middleware
app.add_middleware(RateLimitMiddleware)


@app.get("/limited-endpoint")
def limited_endpoint():
    return {"message": "This is a limited endpoint."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)