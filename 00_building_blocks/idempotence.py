from fastapi import FastAPI

app = FastAPI()

# Simulated counter
counter = 0

# Increment counter
@app.put("/increment")
def increment_counter():
    global counter
    counter += 1
    return {"message": "Counter incremented", "value": counter}

# Reset counter
@app.delete("/reset")
def reset_counter():
    global counter
    counter = 0
    return {"message": "Counter reset", "value": counter}
