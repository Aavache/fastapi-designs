from fastapi import FastAPI

app = FastAPI()

# Define resource data
resources = [
    {"id": 1, "name": "Resource 1"},
    {"id": 2, "name": "Resource 2"},
    {"id": 3, "name": "Resource 3"}
]

# Generate resource links
def generate_links(resource_id):
    links = {
        "self": {"href": f"/resources/{resource_id}"}
    }
    return links

# Get resource by ID
@app.get("/resources/{resource_id}")
def get_resource(resource_id: int):
    resource = next((r for r in resources if r["id"] == resource_id), None)
    if resource is None:
        return {"message": "Resource not found"}
    
    links = generate_links(resource_id)
    resource["links"] = links
    return resource

'''
When sending a POST request to /bulk/items/ with a JSON array of items, like this:

json
Copy code
[
    {"id": 1, "name": "Item 1"},
    {"id": 2, "name": "Item 2"},
    {"id": 3, "name": "Item 3"}
]

The response will be:

json
Copy code
[
    {"id": 1, "action": "created/updated"},
    {"id": 2, "action": "created/updated"},
    {"id": 3, "action": "created/updated"}
]

'''