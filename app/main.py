from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.session import start_session
from app.config import save_message, get_history
from app.utils.qdrant_utils import create_qdrant_collection
from app.api.articles_api import router as articles_router
# from app.api.rag_pipeline import router as rag_pipeline_router

# Initialize FastAPI app
app = FastAPI(title="Chatbod news", version="1.0")

# Allow CORS (Required for frontend communication)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for security (use frontend URL in production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_qdrant_collection()
# Include routes

# Include the routes from session.py
app.add_api_route("/start-session", start_session)

# Include the RAG pipeline routes
# app.include_router(rag_pipeline_router)

# Include the articles API router
app.include_router(articles_router)

# Include the routes from config.py
app.add_api_route("/save-message/{session_id}", save_message, methods=["POST"])
app.add_api_route("/get-history/{session_id}", get_history, methods=["GET"])



@app.get("/")
def root():
    return {"message": "Welcome to chatbot first api"}
