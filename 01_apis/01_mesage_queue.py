from fastapi import FastAPI, HTTPException
import pika


app = FastAPI()

# Connect to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='message_queue')


@app.post("/send_message/{message}")
async def send_message(message: str):
    """Send message to the message queue"""
    channel.basic_publish(exchange='', routing_key='message_queue', body=message)
    return {"message": "Message sent"}


@app.get("/receive_messages")
async def receive_messages():
    """Receive messages from the message queue"""
    method_frame, _, body = channel.basic_get(queue='message_queue')
    if method_frame:
        message = body.decode("utf-8")
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        return {"message": message}
    else:
        raise HTTPException(status_code=404, detail="No messages available")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
