from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

# Initialize the Qdrant client
qdrant_client = QdrantClient(host="localhost", port=6333)

# Define the collection name
collection_name = "news_articles_chatbot"

def create_qdrant_collection():
    try:
        # Get all collections to check if the collection already exists
        collections = qdrant_client.get_collections()
        
        # Print the fetched collections for debugging
        # print("Existing collections:", collections.collections)
        

        if collection_name not in [collection.name for collection in collections.collections]:
            print(f"Creating collection: {collection_name}")
            
            # Create the collection with vector parameters
            qdrant_client.create_collection(
                collection_name="news_articles_chatbot",
                vectors_config=VectorParams(
                    size=384,  # The size of your embeddings (e.g., 384 for all-MiniLM-L6-v2)
                    distance=Distance.COSINE  # Use cosine similarity
                )
            )
            print(f"Collection '{collection_name}' created.")
        else:
            # print(f"Collection '{collection_name}' already exists. Deleting it.")
            # qdrant_client.delete_collection(collection_name)  # Delete the collection first
            #print(f"Collection '{collection_name}' deleted.")
            print(f"Collection '{collection_name}' already exists.")

    except Exception as e:
        print(f"Error creating collection: {e}")

