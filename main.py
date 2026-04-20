"""
api/main.py — FastAPI endpoint for the AWS Cloud Assistant
Run: uvicorn api.main:api_app --reload
"""
import os, sys
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import ask

api_app = FastAPI(title="AWS Cloud Assistant API", version="1.0.0")

class QuestionRequest(BaseModel):
    question: str
    thread_id: str = "default"

class AnswerResponse(BaseModel):
    answer: str
    route: str
    faithfulness: float
    sources: list

@api_app.get("/")
def root():
    return {"message": "AWS Cloud Assistant API is running. POST to /ask"}

@api_app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    try:
        result = ask(request.question, thread_id=request.thread_id)
        return AnswerResponse(
            answer=result.get("answer", ""),
            route=result.get("route", "retrieve"),
            faithfulness=result.get("faithfulness", 0.0),
            sources=result.get("sources", [])
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
