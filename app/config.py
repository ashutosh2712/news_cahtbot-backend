import redis
from fastapi import FastAPI, Depends
from pydantic import BaseModel

app = FastAPI()

# Connect to Redis
redis_client = redis.Redis(host="localhost", port=6379, db=0)

class Message(BaseModel):
    user_message: str
    bot_response: str

@app.post("/save-message/{session_id}")
async def save_message(session_id: str, message: Message):
    redis_client.rpush(session_id, f"User: {message.user_message}")
    redis_client.rpush(session_id, f"Bot: {message.bot_response}")
    return {"message": "Saved to session history"}

@app.get("/get-history/{session_id}")
async def get_history(session_id: str):
    history = redis_client.lrange(session_id, 0, -1)  # Retrieve the entire session history
    return {"session_history": [msg.decode("utf-8") for msg in history]}
