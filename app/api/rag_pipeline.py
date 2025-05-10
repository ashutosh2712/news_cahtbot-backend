from fastapi import APIRouter
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import httpx

router = APIRouter()

# Initialize SentenceTransformer model and Qdrant client
model = SentenceTransformer('all-MiniLM-L6-v2')
qdrant_client = QdrantClient(host="localhost", port=6333)  # Adjust to match your Qdrant setup

# Function to generate a final response from LLM (Gemini API or others)
async def generate_answer(passages):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.gemini.example/generate",  # Replace with actual Gemini API endpoint
            json={"passages": passages}
        )
    return response.json()

@router.post("/generate-response")
async def generate_response(query: str):
    try:
        # Step 1: Convert the query to an embedding
        query_embedding = model.encode([query])

        # Step 2: Retrieve top-k relevant articles from Qdrant
        search_results = qdrant_client.search(
            collection_name="news_articles",  # Ensure this collection exists
            query_vector=query_embedding,
            limit=3  # Retrieve top 3 most similar articles
        )

        # Extract the relevant passages
        passages = [result["payload"] for result in search_results]

        # Step 3: Use Gemini (or any LLM) for final response generation
        answer = await generate_answer(passages)

        # Return the generated response
        return {"response": answer.get("text", "No answer generated")}

    except Exception as e:
        return {"error": str(e)}
