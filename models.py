from pydantic import BaseModel
from typing import List, Dict
from datetime import datetime

class Session(BaseModel):
    session_id: str
    started_at: str
    pending_steps: List[str]
    completed_steps: List[str] = []
    answers: Dict[str, str] = {}

class SessionResponse(BaseModel):
    session_id: str
    status: str
    started_at: str

class AnswerRequest(BaseModel):
    session_id: str
    answer: str

class ProgressResponse(BaseModel):
    completed_steps: List[str]
    pending_steps: List[str]

class SuggestActionResponse(BaseModel):
    suggested_action: str
    status: str
    reason: str

class SessionDetailResponse(Session):
    pass
