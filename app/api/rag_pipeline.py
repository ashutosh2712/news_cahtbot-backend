# rag_pipeline.py
import redis
import json
import os
import requests
#from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, NamedVector


from dotenv import load_dotenv

#from app.utils.qdrant_utils import create_qdrant_collection
# Load environment variables from .env file
load_dotenv()

# redis_client = redis.Redis(host="localhost", port=6379, db=0)
redis_client = redis.Redis(host="redis", port=6379, db=0)

# Initialize Qdrant client
# qdrant_client = QdrantClient(host="localhost", port=6333)
qdrant_client = QdrantClient(host="qdrant", port=6333)


model = SentenceTransformer('all-MiniLM-L6-v2')  # Load the sentence transformer model


TTL = 1 * 60 * 60  # 1 hours
# Qdrant collection name
collection_name = "news_articles_chatbot"

# 1. Function to Scrape Articles (or get them via API)
def get_news_articles(api_key=None):
    """
    This function fetches articles either using an API (e.g., NewsAPI) or web scraping.
    If you are using API, pass `api_key`, otherwise, use web scraping.
    """
    if api_key is None:
        # If no API key is passed, load it from the .env file
        api_key = os.getenv("NEWSAPI_API_KEY")
        
    # Check if the articles are cached in Redis
    cached_articles = redis_client.get("cached_articles")
    if cached_articles:
        print("Returning cached articles from Redis.")
        return json.loads(cached_articles)

    if api_key:
        url = f"https://newsapi.org/v2/everything?q=AI&apiKey={api_key}"
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code != 200:
            raise Exception(f"Error fetching data: {response.status_code} - {response.text}")
        
        articles = response.json()["articles"]
        article_data = []
        
        for article in articles:
            # Extract the title and content (you can also extract more metadata if needed)
            title = article.get("title", "")
            content = article.get("content", "")
            article_data.append({"title": title, "content": content})
            
        # Cache the articles in Redis (TTL of 1 hour)
        redis_client.setex("cached_articles", TTL, json.dumps(articles))  # Cache for 1 hour
        print("Fetching articles from NewsAPI and caching them.")
        
        return article_data
    else:
        # If no API key is found or provided, you can implement web scraping logic here
        pass

# 2. Function to Embed Articles into Vectors
def embed_articles(articles):
    """
    This function embeds the article content using a pre-trained transformer model.
    """
    
    # Check if the embeddings are cached in Redis
    cached_embeddings = redis_client.get("cached_embeddings")
    if cached_embeddings:
        print("Returning cached embeddings from Redis.")
        return json.loads(cached_embeddings)
    
    embeddings = []
    
    for article in articles:
        content = article.get("content")  # Safely get the content from the article
        #content = article.content  # Accessing content directly
        
        # Skip articles with empty or missing content
        if not content:
            continue
        
        # Generate the embedding for the article content
        embedding = model.encode([content])  # The model expects a list of texts
        
        # Append the first (and only) element of the embedding (it's a list of embeddings)
        embeddings.append(embedding[0].tolist())  # We take the first element since we passed a list
        
        # Cache the embeddings in Redis (TTL of 1 hour)
        redis_client.setex("cached_embeddings", TTL, json.dumps(embeddings))  # Cache for 1 hour
        print("Embedding articles and caching embeddings.")
        
    return embeddings

# 3. Function to Insert Articles into Qdrant
def insert_embeddings_into_qdrant(articles, embeddings):
    """
    This function inserts article embeddings into the Qdrant collection.
    """
    for i, article in enumerate(articles):
        # Use a unique ID for each article
        article_id = i + 1  # Simple unique ID (could also use a more complex ID)

        # Insert the vector along with metadata (title, content) into Qdrant
        point = PointStruct(
            id=article_id,
            vector=embeddings[i],  # The embedding vector
            payload={"title": article.title, "content": article.content}  # Metadata
        )

        # Upsert the point into Qdrant
        qdrant_client.upsert(
            collection_name=collection_name,  # Collection name
            points=[point]  # Insert the point
        )
        print(f"Article {article_id} inserted into Qdrant.")

# 4. Function to Search for Relevant Articles in Qdrant
def search_relevant_articles(query, limit=3):
    """
    This function takes a query, embeds it, and performs a search in Qdrant
    to retrieve the top-k most relevant articles.
    """
    # Step 1: Convert the query to an embedding
    query_embedding = model.encode([query])

    # Step 2: Create NamedVector (field name is "vector" in Qdrant by default)
    
    search_results = qdrant_client.query_points(
        collection_name=collection_name,
        query=query_embedding[0],  # Use the query vector directly (it should be a list of floats)
        limit=limit  # Retrieve top-k most similar articles
    )
    #print(f"Search results: {search_results}")
    
    
    return search_results

# 5. Full RAG Pipeline to Ingest and Query Articles
def run_rag_pipeline(api_key=None, query=None):
    """
    Run the complete RAG pipeline to ingest news articles and search for relevant content.
    """
    try:
        # Step 1: Ingest articles (scrape or use API)
        print("Fetching articles...")
        articles = get_news_articles(api_key=api_key)

        # Step 2: Embed the articles into vectors
        print("Embedding articles...")
        embeddings = embed_articles(articles)

        # Step 3: Check if the Qdrant collection exists or create one (Optional, only if you need)
        # create_qdrant_collection() 

        # Step 4: Insert embeddings into Qdrant
        print("Inserting embeddings into Qdrant...")
        insert_embeddings_into_qdrant(articles, embeddings)

        # Step 5: Search for relevant articles based on the user query (if provided)
        if query:
            print("Searching for relevant articles based on the query...")
            search_results = search_relevant_articles(query)
            print("Search Results:", search_results)
            return search_results
        else:
            print("No query provided. Ingesting and embedding completed.")
            return {"message": "Ingestion and embedding completed, but no query provided for search."}

    except Exception as e:
        print(f"An error occurred during the RAG pipeline: {str(e)}")
        return {"error": str(e)}

