from pydantic import BaseModel
from typing import List

# Define a Pydantic model for the request body
class QueryRequest(BaseModel):
    query: str
    
class Message(BaseModel):
    user_message: str
    bot_response: str
    
# Pydantic model for incoming article data
class Article(BaseModel):
    title: str
    content: str
    
# Pydantic model for the embeddings (list of vectors)
class Embedding(BaseModel):
    vector: List[float]  # This represents a single embedding vector
    
# Pydantic model for the request body containing both articles and embeddings
class ArticlesRequest(BaseModel):
    articles: List[Article]
    embeddings: List[List[float]]