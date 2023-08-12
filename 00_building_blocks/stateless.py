'''
- Simplicity: Stateless APIs are straightforward to design, implement, and maintain. They don't require the server to keep track of session states or context.
- Scalability: Stateless APIs are inherently more scalable because each request can be processed independently. Servers can distribute requests across multiple instances without needing to share session data.
- Reliability: Since there is no server-side state to manage, the chances of bugs related to state management are minimized, leading to a more reliable API.
- Caching: Stateless APIs are ideal for caching responses, as each request contains all the information needed to generate the response. This can improve performance and reduce server load
- Redundancy: Stateless APIs are more resilient to server failures. If one server instance fails, another can take over seamlessly because it doesn't rely on shared state.
- Load Balancing: Load balancers can distribute requests evenly among server instances, without needing to consider session affinity.
'''
from fastapi import FastAPI

app = FastAPI()

# Store user data (simulated database)
users_db = {}

class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email

@app.post("/register-user")
def register_user(username: str, email: str):
    if username in users_db:
        return {"message": "Username already taken"}
    
    user = User(username=username, email=email)
    users_db[username] = user
    
    return {"message": "User registered successfully", "user": user.__dict__}

@app.get("/users/{username}")
def get_user(username: str):
    user = users_db.get(username)
    if user:
        return user.__dict__
    else:
        return {"message": "User not found"}
