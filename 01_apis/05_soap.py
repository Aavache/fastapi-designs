from fastapi import FastAPI, Request
from xml.etree import ElementTree as ET


app = FastAPI()

# Simulated database
data = {}


@app.post("/soap")
async def soap_endpoint(request: Request):
    """A SOAP endpoint that can handle two types of requests:
    - CreateItem: Creates an item in the database
    - GetItem: Gets an item from the database
    """
    content = await request.body()
    xml_tree = ET.fromstring(content)

    if xml_tree.tag == "CreateItem":
        item_id = xml_tree.find("ItemID").text
        item_name = xml_tree.find("ItemName").text
        data[item_id] = item_name
        response = f"<CreateItemResponse>Item {item_name} created with ID {item_id}</CreateItemResponse>"
    elif xml_tree.tag == "GetItem":
        item_id = xml_tree.find("ItemID").text
        item_name = data.get(item_id, "Not Found")
        response = f"<GetItemResponse>Item {item_name} with ID {item_id}</GetItemResponse>"
    else:
        response = "<ErrorResponse>Invalid SOAP request</ErrorResponse>"
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
