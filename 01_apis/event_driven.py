from fastapi import FastAPI, HTTPException, BackgroundTasks
import pika
import json

app = FastAPI()

def send_event(event_data):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='events')
    channel.basic_publish(exchange='', routing_key='events', body=json.dumps(event_data))
    connection.close()

@app.post("/items/")
async def create_item(background_tasks: BackgroundTasks, item: dict):
    event_data = {
        "event_type": "item_created",
        "data": item
    }
    background_tasks.add_task(send_event, event_data)
    return item

def process_event(event_data):
    event_type = event_data["event_type"]
    data = event_data["data"]
    print(f"Received event: {event_type}, Data: {data}")

def receive_events():
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


'''
pip install fastapi pika



'''