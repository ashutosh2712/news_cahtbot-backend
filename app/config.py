import redis
from fastapi import FastAPI, HTTPException
from app.models import Message

app = FastAPI()

# Connect to Redis
# redis_client = redis.Redis(host="localhost", port=6379, db=0)
redis_client = redis.Redis(host="redis", port=6379, db=0)

# Setting TTL to 24 hours for each session data (in seconds)
TTL = 1 * 60 * 60  # 1 hours

@app.post("/save-message/{session_id}")
async def save_message(session_id: str, message: Message):
    """
    Saves the user and bot messages in the session history in Redis.
    """
    
    try:
        redis_client.rpush(session_id, f"User: {message.user_message}")
        redis_client.rpush(session_id, f"Bot: {message.bot_response}")
        
        # Set TTL for session data in Redis
        redis_client.expire(session_id, TTL)
    
        return {"message": "Saved to session history"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving message: {str(e)}")

@app.get("/get-history/{session_id}")
async def get_history(session_id: str):
    """
    Retrieves the history of the session from Redis.
    """
    
    history = redis_client.lrange(session_id, 0, -1)  # Retrieve the entire session history
    return {"session_history": [msg.decode("utf-8") for msg in history]}

# Endpoint to clear the session history in Redis
@app.delete("/clear-session/{session_id}")
async def clear_session(session_id: str):
    """
    Clears the session history from Redis.
    """
    try:
        redis_client.delete(session_id)  # Delete all data for this session
        return {"message": f"Session {session_id} cleared."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing session: {str(e)}")
