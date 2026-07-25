from pydantic import BaseModel
from typing import List, Optional


class ContactRequest(BaseModel):
    first_name: str
    last_name: str
    email: str
    subject: str
    message: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[dict]] = []


class HealthResponse(BaseModel):
    status: str
    groq_configured: bool
    email_configured: bool


class ChatResponse(BaseModel):
    reply: str


class ContactResponse(BaseModel):
    status: str
    detail: str = ""