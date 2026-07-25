from fastapi import APIRouter, HTTPException
from app.models import ContactRequest, ChatRequest, HealthResponse, ChatResponse, ContactResponse
from app.utils import SYSTEM_PROMPT, get_groq_response, send_email
from app.config import settings

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def get_health():
    return HealthResponse(
        status="ok",
        groq_configured=bool(settings.groq_api_key),
        email_configured=bool(settings.email_address and settings.email_password),
    )


@router.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    # Build messages array: system prompt + history + new user message
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for msg in req.history:
        messages.append(msg)
    messages.append({"role": "user", "content": req.message})

    reply = await get_groq_response(messages)
    return ChatResponse(reply=reply)


@router.post("/contact", response_model=ContactResponse)
async def contact(req: ContactRequest):
    if not all([req.first_name, req.last_name, req.email, req.subject, req.message]):
        raise HTTPException(status_code=400, detail="All fields are required.")

    # Build email
    to_email = settings.email_address or req.email
    subject = f"Portfolio Contact: {req.subject} — from {req.first_name} {req.last_name}"
    body = f"""
New Contact Form Submission
──────────────────────────
From: {req.first_name} {req.last_name}
Email: {req.email}
Subject: {req.subject}

Message:
{req.message}
"""

    success = send_email(to_email, subject, body)

    if success:
        return ContactResponse(status="sent", detail="Message sent successfully.")
    else:
        return ContactResponse(
            status="received",
            detail="Email not configured, but message was received. Contact Aklilu directly at aklilwassie@email.com."
        )