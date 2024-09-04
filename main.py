from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

app = FastAPI(
    title="AI Scaffolding Strategist API",
    description="This API allows users to interact with the AI Scaffolding Strategist, guiding non-programmers step-by-step through the process of building automated systems.",
    version="1.0.0"
)

# Simulated in-memory storage for sessions, questions, and user progress
sessions = {}
questions = [
    {"id": 1, "question": "What kind of system are you looking to build?", "options": ["A) Web app", "B) Automation", "C) Data processing"]},
    {"id": 2, "question": "What type of automation are you thinking of?", "options": ["A) Email automation", "B) Social media automation", "C) Data transfer"]},
    {"id": 3, "question": "What programming language are you most comfortable with?", "options": ["A) Python", "B) JavaScript", "C) No preference"]}
]

user_data = {}

# Schemas for request/response models
class StartSessionResponse(BaseModel):
    session_id: str
    status: str
    started_at: str

class Answer(BaseModel):
    answer: str

class QuestionResponse(BaseModel):
    question: str
    options: List[str]

class ProgressResponse(BaseModel):
    completedSteps: List[str]
    pendingSteps: List[str]

class SuggestActionRequest(BaseModel):
    session_id: str

class SuggestActionResponse(BaseModel):
    suggested_action: str
    status: str
    reason: Optional[str]

# Endpoint to start a new session
@app.post("/api/startSession", response_model=StartSessionResponse)
async def start_session():
    session_id = str(uuid.uuid4())
    started_at = datetime.utcnow().isoformat()
    sessions[session_id] = {"started_at": started_at, "current_step": 0, "answers": []}
    return StartSessionResponse(session_id=session_id, status="success", started_at=started_at)

# Endpoint to fetch the next question
@app.get("/api/questions", response_model=QuestionResponse)
async def get_question(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    step = sessions[session_id]["current_step"]
    if step >= len(questions):
        raise HTTPException(status_code=404, detail="No more questions available")

    current_question = questions[step]
    return {"question": current_question["question"], "options": current_question["options"]}

# Endpoint to submit an answer and move to the next question
@app.post("/api/answers")
async def post_answer(session_id: str, answer: Answer):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    step = sessions[session_id]["current_step"]
    if step >= len(questions):
        raise HTTPException(status_code=404, detail="No more questions available")

    # Save the answer
    sessions[session_id]["answers"].append(answer.answer)
    sessions[session_id]["current_step"] += 1  # Move to the next step

    # Provide feedback
    if sessions[session_id]["current_step"] < len(questions):
        return {"status": "next_question"}
    else:
        return {"status": "completed"}

# Endpoint to get current progress
@app.get("/api/progress", response_model=ProgressResponse)
async def get_progress(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    step = sessions[session_id]["current_step"]
    completed = [q["question"] for q in questions[:step]]
    pending = [q["question"] for q in questions[step:]]
    return {"completedSteps": completed, "pendingSteps": pending}

# Endpoint to get a summary of progress
@app.get("/api/review", response_model=QuestionResponse)
async def get_review(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    answers = sessions[session_id]["answers"]
    summary = f"Your answers so far: {answers}"
    return {"question": summary, "options": []}  # Returning as question field for consistency

# Endpoint to suggest the next action based on user context
@app.post("/api/suggestAction", response_model=SuggestActionResponse)
async def suggest_action(request: SuggestActionRequest):
    if request.session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")

    session_data = sessions.get(request.session_id, {})
    
    # Enhanced decision logic for suggesting actions
    if "A) Web app" in session_data["answers"]:
        suggested_action = "startWebAppTutorial"
        reason = "The user chose to build a Web app."
    elif "B) Automation" in session_data["answers"]:
        suggested_action = "startAutomationGuide"
        reason = "The user is interested in Automation."
    elif "C) Data processing" in session_data["answers"]:
        suggested_action = "startDataProcessingGuide"
        reason = "The user is interested in Data processing."
    else:
        suggested_action = "exploreFeatures"
        reason = "The user's preferences are being processed."

    return SuggestActionResponse(suggested_action=suggested_action, status="success", reason=reason)
