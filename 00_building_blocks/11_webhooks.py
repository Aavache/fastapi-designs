"""We can attach a webhook URL to a specific event, and when that 
event occurs, we can send a payload to the webhook URL. This is
similar to callbacks, but instead of the client notifying the server,
the server notifies the client.
"""
from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

# Store registered webhook URLs
webhook_urls = []


class WebhookPayload(BaseModel):
    """Webhook payload model"""
    event: str
    data: dict


def send_payload(url, event, data):
    """Send payload to a webhook URL (simulate by printing here)"""
    print(f"Sending {event} payload to {url}: {data}")


@app.post("/register")
def register_webhook(url: str):
    """Register a webhook URL"""
    webhook_urls.append(url)
    return {"message": "Webhook registered successfully"}


@app.post("/trigger")
def trigger_webhook(payload: WebhookPayload):
    """Trigger a webhook event"""
    event = payload.event
    data = payload.data
    
    for url in webhook_urls:
        send_payload(url, event, data)
    
    return {"message": "Webhook event triggered"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
