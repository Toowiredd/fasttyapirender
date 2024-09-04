from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="AI Scaffolding Strategist API",
    description="This API allows users to interact with the AI Scaffolding Strategist, guiding non-programmers step-by-step through the process of building automated systems.",
    version="1.0.0"
)

# Simulated in-memory storage for questions and user progress
questions = [
    {"id": 1, "question": "What kind of system are you looking to build?", "options": ["A) Web app", "B) Automation", "C) Data processing"]},
    {"id": 2, "question": "What type of automation are you thinking of?", "options": ["A) Email automation", "B) Social media automation", "C) Data transfer"]},
    {"id": 3, "question": "What programming language are you most comfortable with?", "options": ["A) Python", "B) JavaScript", "C) No preference"]}
]

user_progress = {}

# Schemas for request/response models
class Answer(BaseModel):
    answer: str

class QuestionResponse(BaseModel):
    question: str
    options: List[str]

class ProgressResponse(BaseModel):
    completedSteps: List[str]
    pendingSteps: List[str]

# Endpoint to fetch the next question
@app.get("/questions", response_model=QuestionResponse)
async def get_question(user_id: str):
    if user_id not in user_progress:
        user_progress[user_id] = {"current_step": 0, "answers": []}

    step = user_progress[user_id]["current_step"]
    if step >= len(questions):
        raise HTTPException(status_code=404, detail="No more questions available")

    current_question = questions[step]
    return {"question": current_question["question"], "options": current_question["options"]}

# Endpoint to submit an answer and move to the next question
@app.post("/answers")
async def post_answer(user_id: str, answer: Answer):
    if user_id not in user_progress:
        user_progress[user_id] = {"current_step": 0, "answers": []}

    step = user_progress[user_id]["current_step"]
    if step >= len(questions):
        raise HTTPException(status_code=404, detail="No more questions available")

    # Save the answer
    user_progress[user_id]["answers"].append(answer.answer)
    user_progress[user_id]["current_step"] += 1  # Move to the next step

    # Provide feedback
    if user_progress[user_id]["current_step"] < len(questions):
        return {"status": "next_question"}
    else:
        return {"status": "completed"}

# Endpoint to get current progress
@app.get("/progress", response_model=ProgressResponse)
async def get_progress(user_id: str):
    if user_id not in user_progress:
        raise HTTPException(status_code=404, detail="No progress found for this user")

    step = user_progress[user_id]["current_step"]
    completed = [q["question"] for q in questions[:step]]
    pending = [q["question"] for q in questions[step:]]
    return {"completedSteps": completed, "pendingSteps": pending}

# Endpoint to get a summary of progress
@app.get("/review", response_model=QuestionResponse)
async def get_review(user_id: str):
    if user_id not in user_progress:
        raise HTTPException(status_code=404, detail="No review found for this user")

    answers = user_progress[user_id]["answers"]
    summary = f"Your answers so far: {answers}"
    return {"question": summary, "options": []}  # Returning as question field for consistency
