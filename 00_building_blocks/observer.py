from fastapi import FastAPI
from typing import List

app = FastAPI()

class Observer:
    def update(self, message):
        pass

class User(Observer):
    def __init__(self, name):
        self.name = name

    def update(self, message):
        print(f"{self.name} received message: {message}")

class NewsPublisher:
    def __init__(self):
        self._observers = []

    def add_observer(self, observer):
        self._observers.append(observer)

    def remove_observer(self, observer):
        self._observers.remove(observer)

    def notify_observers(self, message):
        for observer in self._observers:
            observer.update(message)

@app.get("/")
async def publish_news(news: str, subscribers: List[str]):
    publisher = NewsPublisher()

    for subscriber in subscribers:
        user = User(subscriber)
        publisher.add_observer(user)

    publisher.notify_observers(news)
    return {"message": f"News '{news}' published to subscribers: {subscribers}"}
