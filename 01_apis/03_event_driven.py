"""Simple event-driven API using RabbitMQ:
- When you create an item through a POST request to /items/, 
  k background task is added to send an event to RabbitMQ.
- The `send_event` function sends the event data to a RabbitMQ queue named 'events'.
- A separate thread (`receive_events`) is started to consume events from 
  the queue and process them using the process_event function.

NOTE: make sure to run the api on your terminal using the following command:

uvicorn main:app --host 0.0.0.0 --port 8000

"""
from fastapi import FastAPI, BackgroundTasks
import pika
import json


app = FastAPI()


def send_event(event_data):
    """Send event data to RabbitMQ queue"""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='events')
    channel.basic_publish(exchange='', routing_key='events', body=json.dumps(event_data))
    connection.close()


@app.post("/items/")
async def create_item(background_tasks: BackgroundTasks, item: dict):
    """Create an item and send an event to RabbitMQ"""
    event_data = {
        "event_type": "item_created",
        "data": item
    }
    background_tasks.add_task(send_event, event_data)
    return item


def process_event(event_data):
    """Process an event"""
    event_type = event_data["event_type"]
    data = event_data["data"]
    print(f"Received event: {event_type}, Data: {data}")


def receive_events():
    """Receive events from RabbitMQ"""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='events')
    channel.basic_consume(queue='events', on_message_callback=process_event, auto_ack=True)
    print('Waiting for events...')
    channel.start_consuming()


if __name__ == "__main__":
    import threading
    event_thread = threading.Thread(target=receive_events)
    event_thread.start()
