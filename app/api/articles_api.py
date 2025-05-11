from fastapi import APIRouter, HTTPException
from app.models import Article, ArticlesRequest
from typing import List

from app.api.rag_pipeline import (
    get_news_articles, 
    embed_articles, 
    insert_embeddings_into_qdrant, 
    search_relevant_articles
)

router = APIRouter()



# Endpoint to fetch articles using NewsAPI or scraping
@router.get("/fetch-articles/")
async def fetch_articles():
    """
    Fetches articles from NewsAPI or scraping
    """
    try:
        articles = get_news_articles()
        return {"articles": articles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching articles: {str(e)}")

# Endpoint to embed articles into vectors
@router.post("/embed-articles/")
async def embed_articles_endpoint(articles: list[Article]):
    """
    Embeds the articles into vectors using a pre-trained model
    """
    try:
        # Convert Pydantic models to dictionaries
        article_dicts = [article.model_dump() for article in articles]
        
        embeddings = embed_articles(article_dicts)
        
         # Ensure embeddings are lists (convert them if necessary)
        embeddings = [embedding.tolist() if hasattr(embedding, 'tolist') else embedding for embedding in embeddings]
        return {"embeddings": embeddings}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error embedding articles: {str(e)}")

# Endpoint to insert embeddings into Qdrant
@router.post("/insert-embeddings/")
async def insert_embeddings_endpoint(request: ArticlesRequest):
    """
    Inserts the embeddings of articles into Qdrant
    """
    try:
        # Extract articles and embeddings from the request
        articles = request.articles
        embeddings = request.embeddings  # List of lists (no need for further conversion)

        # Insert the embeddings into Qdrant
        insert_embeddings_into_qdrant(articles, embeddings)
        return {"message": "Embeddings inserted into Qdrant successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inserting embeddings: {str(e)}")

# Endpoint to search for relevant articles based on user query
@router.post("/search-relevant-articles/")
async def search_relevant_articles_endpoint(query: str, limit: int = 3):
    """
    Perform a search for relevant articles based on a user query
    """
    try:
        search_results = search_relevant_articles(query, limit)
        return {"search_results": search_results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error performing search: {str(e)}")
