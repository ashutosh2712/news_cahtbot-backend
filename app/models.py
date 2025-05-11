from pydantic import BaseModel

# Define a Pydantic model for the request body
class QueryRequest(BaseModel):
    query: str