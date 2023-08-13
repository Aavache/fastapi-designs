"""The idea of singleton is to have only one instance of a class 
in the entire application. It is particularly useful when you want
to have a single connection to a database or a single logger instance
"""
from fastapi import FastAPI
from typing import Optional

app = FastAPI()


class DatabaseConnection:
    """Singleton class for database connection"""
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
    """Execute a query using a database connection"""
    if conn is None:
        conn = DatabaseConnection()
    
    result = conn.execute_query(query)
    return {"result": result}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)