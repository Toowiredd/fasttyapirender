from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import uuid

app = FastAPI()

# In-memory session storage
sessions = {}

# Models for request and response bodies
class SessionResponse(BaseModel):
    session_id: str
    status: str
    started_at: str

class AnswerRequest(BaseModel):
    session_id: str
    answer: str

class ProgressResponse(BaseModel):
    completed_steps: list
    pending_steps: list

class SuggestActionResponse(BaseModel):
    suggested_action: str
    status: str
    reason: str


# Endpoint 1: Start Session
@app.post("/api/startSession", response_model=SessionResponse)
def start_session():
    session_id = str(uuid.uuid4())
    session_data = {
        "started_at": str(datetime.now()),
        "completed_steps": [],
        "pending_steps": ["Q1", "Q2", "Q3"],  # Example questions
    }
    sessions[session_id] = session_data

    return {
        "session_id": session_id,
        "status": "Session started",
        "started_at": session_data["started_at"]
    }


# Endpoint 2: Get Next Question
@app.get("/api/questions")
def get_next_question(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = sessions[session_id]
    if len(session_data["pending_steps"]) == 0:
        return {"question": "All questions completed", "options": []}
    
    next_question = session_data["pending_steps"][0]
    options = ["Option A", "Option B", "Option C"]  # Example options

    return {
        "question": next_question,
        "options": options
    }


# Endpoint 3: Submit Answer
@app.post("/api/answers")
def submit_answer(answer_request: AnswerRequest):
    if answer_request.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = sessions[answer_request.session_id]
    if len(session_data["pending_steps"]) == 0:
        raise HTTPException(status_code=400, detail="No pending questions")
    
    # Move question from pending to completed
    completed_question = session_data["pending_steps"].pop(0)
    session_data["completed_steps"].append(completed_question)
    
    return {"status": "Answer submitted"}


# Endpoint 4: Get Progress
@app.get("/api/progress", response_model=ProgressResponse)
def get_progress(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = sessions[session_id]
    
    return {
        "completed_steps": session_data["completed_steps"],
        "pending_steps": session_data["pending_steps"]
    }


# Endpoint 5: Get Review
@app.get("/api/review")
def get_review(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = sessions[session_id]
    completed_steps = session_data["completed_steps"]
    
    return {
        "question": "Summary of completed steps",
        "options": completed_steps
    }


# Endpoint 6: Suggest Action
@app.post("/api/suggestAction", response_model=SuggestActionResponse)
def suggest_action(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = sessions[session_id]
    if len(session_data["pending_steps"]) == 0:
        suggested_action = "All questions answered"
        status = "Completed"
        reason = "No pending questions left."
    else:
        suggested_action = "Answer the next question"
        status = "Pending"
        reason = "Questions are still remaining in the session."
    
    return {
        "suggested_action": suggested_action,
        "status": status,
        "reason": reason
    }

