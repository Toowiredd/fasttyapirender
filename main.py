from fastapi import FastAPI, HTTPException, Request
from typing import List, Optional
from sse_starlette import EventSourceResponse
import asyncio
import json

from models import (
    SessionResponse,
    AnswerRequest,
    ProgressResponse,
    SuggestActionResponse,
    SessionDetailResponse,
)
from session_manager import session_manager

app = FastAPI(title="AI Scaffolding Strategist API")

@app.get("/")
def read_root():
    """Root endpoint providing a welcome message."""
    return {"message": "Welcome to the AI Scaffolding Strategist API"}


@app.post("/api/startSession", response_model=SessionResponse)
async def start_session(questions: Optional[List[str]] = None):
    """Create a new session with optional initial questions."""
    session = session_manager.create_session(questions)
    return SessionResponse(
        session_id=session.session_id,
        status="Session started",
        started_at=session.started_at,
    )


@app.get("/api/questions")
async def get_next_question(session_id: str):
    """Return the next pending question for a session."""
    session = session_manager.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if not session.pending_steps:
        return {"question": "All questions completed", "options": []}

    next_question = session.pending_steps[0]
    options = ["Option A", "Option B", "Option C"]
    return {"question": next_question, "options": options}


@app.post("/api/answers")
async def submit_answer(answer_request: AnswerRequest):
    """Submit an answer for the current question."""
    question = session_manager.submit_answer(
        answer_request.session_id, answer_request.answer
    )
    if question is None:
        raise HTTPException(status_code=404, detail="Session not found or no pending questions")
    return {"status": "Answer submitted", "question": question}


@app.get("/api/progress", response_model=ProgressResponse)
async def get_progress(session_id: str):
    """Get progress for a session."""
    session = session_manager.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return ProgressResponse(
        completed_steps=session.completed_steps,
        pending_steps=session.pending_steps,
    )


@app.get("/api/review")
async def get_review(session_id: str):
    """Provide a summary of completed steps."""
    session = session_manager.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"question": "Summary of completed steps", "options": session.completed_steps}


@app.post("/api/suggestAction", response_model=SuggestActionResponse)
async def suggest_action(session_id: str):
    """Suggest the next action based on pending questions."""
    session = session_manager.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if not session.pending_steps:
        suggested_action = "All questions answered"
        status = "Completed"
        reason = "No pending questions left."
    else:
        suggested_action = "Answer the next question"
        status = "Pending"
        reason = "Questions are still remaining in the session."
    return SuggestActionResponse(
        suggested_action=suggested_action,
        status=status,
        reason=reason,
    )


@app.get("/api/session", response_model=SessionDetailResponse)
async def session_details(session_id: str):
    """Retrieve all data for a given session."""
    session = session_manager.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return SessionDetailResponse(**session.dict())


@app.get("/api/stream/{session_id}")
async def stream_session(session_id: str, request: Request):
    """Stream session progress using Server-Sent Events."""
    session = session_manager.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    async def event_generator():
        while True:
            current = session_manager.get(session_id)
            yield {"data": json.dumps(current.dict()), "event": "progress"}
            if not current.pending_steps or await request.is_disconnected():
                break
            await asyncio.sleep(1)

    return EventSourceResponse(event_generator(), headers={"Cache-Control": "no-cache"})
