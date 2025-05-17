import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict

from models import Session

DATA_FILE = Path("sessions.json")

class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, Session] = {}
        self.load()

    def load(self):
        if DATA_FILE.exists():
            try:
                data = json.loads(DATA_FILE.read_text())
                for s_id, s_data in data.items():
                    self.sessions[s_id] = Session(**s_data)
            except json.JSONDecodeError:
                pass

    def save(self):
        DATA_FILE.write_text(json.dumps({sid: s.dict() for sid, s in self.sessions.items()}, indent=2))

    def create_session(self, questions=None) -> Session:
        session_id = str(uuid.uuid4())
        session = Session(
            session_id=session_id,
            started_at=str(datetime.now()),
            pending_steps=questions or ["Q1", "Q2", "Q3"],
        )
        self.sessions[session_id] = session
        self.save()
        return session

    def get(self, session_id: str) -> Session:
        return self.sessions.get(session_id)

    def submit_answer(self, session_id: str, answer: str):
        session = self.get(session_id)
        if not session or not session.pending_steps:
            return None
        question = session.pending_steps.pop(0)
        session.completed_steps.append(question)
        session.answers[question] = answer
        self.save()
        return question

session_manager = SessionManager()
