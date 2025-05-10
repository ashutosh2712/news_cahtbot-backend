from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


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

# Include routes
app.include_router( prefix="/r1", tags=["R1"])



@app.get("/")
def root():
    return {"message": "Welcome to chatbot first api"}
