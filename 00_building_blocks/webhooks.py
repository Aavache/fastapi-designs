from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Store registered webhook URLs
webhook_urls = []

# Webhook payload model
class WebhookPayload(BaseModel):
    event: str
    data: dict

# Register a webhook URL
@app.post("/register")
def register_webhook(url: str):
    webhook_urls.append(url)
    return {"message": "Webhook registered successfully"}

# Trigger a webhook event
@app.post("/trigger")
def trigger_webhook(payload: WebhookPayload):
    event = payload.event
    data = payload.data
    
    for url in webhook_urls:
        # Send the payload to the registered webhook URLs (simulate by printing here)
        print(f"Sending {event} event to {url}: {data}")
    
    return {"message": "Webhook event triggered"}
