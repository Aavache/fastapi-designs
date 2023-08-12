from fastapi import FastAPI, Request, Response

app = FastAPI()

# Sample data
sample_data = {"name": "John Doe", "age": 30}

@app.get("/data")
async def get_data(request: Request):
    """The content format is determined by the Accept header"""
    accept_header = request.headers.get("accept")
    
    if "application/json" in accept_header:
        return sample_data  # Return JSON data by default
    
    if "application/xml" in accept_header:
        xml_data = "<data>\n"
        for key, value in sample_data.items():
            xml_data += f"    <{key}>{value}</{key}>\n"
        xml_data += "</data>"
        return Response(content=xml_data, media_type="application/xml")
    
    return sample_data  # If no
