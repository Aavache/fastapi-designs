from fastapi import FastAPI
from typing import Optional

app = FastAPI()

class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.initialize()
        return cls._instance
    
    def initialize(self):
        self.connection_string = "your_database_connection_string"
    
    def execute_query(self, query: str) -> str:
        # Simulated query execution
        return f"Executing query: {query} using connection: {self.connection_string}"

@app.get("/")
async def execute_query(query: str, conn: Optional[DatabaseConnection] = None):
    if conn is None:
        conn = DatabaseConnection()
    
    result = conn.execute_query(query)
    return {"result": result}
