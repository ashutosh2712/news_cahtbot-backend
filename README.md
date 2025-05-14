# Chatbot Backend

This repository contains the backend for a chatbot application that uses a variety of APIs to generate responses based on a user's query. The backend is built using **FastAPI** and utilizes **Redis** for caching session history and conversation data, as well as **Qdrant** for storing embeddings and performing similarity search.

## Features

- Fetches and embeds articles using a pre-trained model.
- Inserts article embeddings into Qdrant for similarity search.
- Provides an endpoint for querying relevant articles based on user input.
- Caches session history in Redis with TTL (Time-to-Live) for automatic cache expiration.
- Allows users to start new sessions, reset the session, and fetch previous session history.

## Requirements

Make sure you have the following dependencies installed:

- Python 3.10 or higher
- Redis (for session management)
- Qdrant (for storing embeddings)
- Gemini API key (for generating responses)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd chatbot_backend
  
2. Create a virtual environment (optional, but recommended):
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use 'env\Scripts\activate'


3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
4. Create a .env file in the root of the chatbot_backend directory and configure the following environment variables:
   ```bash
   GEMINI_API_KEY=your_gemini_api_key_here
   NEWSAPI_API_KEY=your_newsapi_api_key_here
   

## Running the Backend
1. Make sure you have Redis and Qdrant running, either locally or in Docker containers. (You can use the docker-compose.yml provided in the root of the project to spin up these services).
2. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
The server will be accessible at http://localhost:8000.

## Caching & Performance

### Redis Caching
1. The backend uses Redis for caching session data (such as chat history).
2. Redis is configured with a TTL (Time-to-Live) for automatic cache expiration. The TTL is set to 1 hour by default, meaning data will expire after 60 minutes.

#### Running Redis and Qdrant with Docker
To run Redis and Qdrant in Docker, use the docker-compose.yml file provided. This will set up both Redis and Qdrant services locally.

1. Redis Setup:

Redis will be available on port 6379 and will store session data in-memory.

2. Qdrant Setup:

Qdrant will be available on port 6333 for the API, and it will store the article embeddings.

3.1 Docker Setup
Make sure you have Docker installed. Then, run the following command to start Redis and Qdrant containers:
```bash
docker-compose -f docker-compose.yml up --build
```

### Cache Configuration
```bash
TTL = 60 * 60 #1 Hour
# Cache the articles in Redis (TTL of 1 hour)
redis_client.setex("cached_articles", TTL, json.dumps(articles))  # Cache for 1 hours
```
## Notes
1. The backend supports multi-session handling, allowing users to maintain separate sessions.
2. Cache data will automatically expire based on the TTL configuration.

## License
This project is licensed under the MIT License - see the LICENSE file for details.




