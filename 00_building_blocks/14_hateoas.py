"""Hypermedia as the Engine of Application State (HATEOAS) 
is a principle in RESTful API design that involves including 
links and relevant information within API responses. 
These links guide clients on the available actions they 
can take next
"""
from fastapi import FastAPI


app = FastAPI()

# Define fake resource data
resources = [
    {"id": 1, "name": "Resource 1"},
    {"id": 2, "name": "Resource 2"},
    {"id": 3, "name": "Resource 3"}
]


def generate_links(resource_id):
    """Generate resource links to itself"""
    links = {
        "self": {"href": f"/resources/{resource_id}"}
    }
    return links


@app.get("/resources/{resource_id}")
def get_resource(resource_id: int):
    """Get resource by ID"""
    resource = next((r for r in resources if r["id"] == resource_id), None)
    if resource is None:
        return {"message": "Resource not found"}
    
    links = generate_links(resource_id)
    resource["links"] = links
    return resource


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)