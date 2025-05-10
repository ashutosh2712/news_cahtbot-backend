from fastapi import FastAPI, Depends
import uuid

app = FastAPI()

@app.get("/start-session")
async def start_session():
    session_id = str(uuid.uuid4())  # Generate a unique session ID
    return {"session_id": session_id}
