from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Message(BaseModel):
    content: str

class MessageQueue:
    def __init__(self):
        self.messages = []

    def send_message(self, message: Message):
        self.messages.append(message.content)
        return f"Message '{message.content}' sent to the queue"

    def get_messages(self):
        return self.messages

message_queue = MessageQueue()

@app.post("/send-message/")
async def send_message(message: Message):
    return message_queue.send_message(message)

@app.get("/get-messages/", response_model=List[str])
async def get_messages():
    return message_queue.get_messages()
