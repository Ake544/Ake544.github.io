# Portfolio Backend Architecture

## Overview

This backend powers two features on Aklilu's portfolio website:
1. **AI Chatbot** — answers recruiter questions via Groq's free LLM API
2. **Contact Form** — receives messages and emails them via Gmail SMTP

All services are **free-tier** (Hugging Face Spaces + Groq API + Gmail SMTP).

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  Browser (Portifolio/index.html)                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  script.js  →  fetch() to backend API                    │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                           │
                           ▼  HTTPS
┌─────────────────────────────────────────────────────────────────┐
│  FastAPI Server (HF Space or localhost:8000)                    │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │  POST /chat    →  Groq API (llama-3.1-8b-instant)        │  │
│  │  POST /contact →  Gmail SMTP (free App Password)         │  │
│  │  GET  /health  →  Server status                          │  │
│  └───────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Project Structure

```
Portifolio/
├── index.html                 # Frontend page (your existing site)
├── style.css                  # Frontend styles
├── script.js                  # Frontend logic → calls backend API
├── images/                    # Assets
└── backend/                   # ★ Full backend (deploy to HF Spaces)
    ├── main.py                # FastAPI entry point
    ├── requirements.txt       # Python dependencies
    ├── .env                   # Local env vars (DO NOT commit)
    ├── architecture.md        # This file
    └── app/
        ├── __init__.py        # Package marker
        ├── config.py          # Settings from env vars
        ├── models.py          # Pydantic request/response models
        ├── routes.py          # /chat, /contact, /health endpoints
        └── utils.py           # Groq API caller + email sender
```

---

## API Endpoints

### `GET /health`
**Response:**
```json
{"status":"ok","groq_configured":true,"email_configured":true}
```

### `POST /chat`
**Request:**
```json
{
  "message": "What is your strongest skill?",
  "history": [{"role":"user","content":"Hi"}, {"role":"assistant","content":"Hey!"}]
}
```
**Response:**
```json
{"reply": "My strongest skill is building end-to-end ML systems..."}
```
**Flow:** System prompt (your full bio) + history + user message → Groq API → reply

### `POST /contact`
**Request:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "subject": "Job Opportunity",
  "message": "We'd love to interview you..."
}
```
**Response:**
```json
{"status":"sent","detail":"Message sent successfully."}
```
**Flow:** Validates input → sends email via Gmail SMTP App Password

---

## Environment Variables

Set these in your HF Space settings (or `.env` for local dev):

| Variable | Purpose | Get it at |
|---|---|---|
| `GROQ_API_KEY` | Free LLM access | [console.groq.com](https://console.groq.com) |
| `EMAIL_ADDRESS` | Your Gmail | Your Gmail inbox |
| `EMAIL_APP_PASSWORD` | Gmail App Password | Google Account → Security → App Passwords |

---

## How to Run Locally

```bash
cd Portifolio/backend
pip install -r requirements.txt
# Edit .env with your keys
uvicorn main:app --reload --port 8000 --app-dir .
```

Then open `Portifolio/index.html` in your browser — it will call `http://localhost:8000`.

---

## Deploy to Hugging Face Spaces

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces) → Create new Space
2. Name: `your-portfolio-backend`
3. SDK: **Docker**
4. Push the `Portifolio/backend/` folder contents to the Space
5. In Space Settings → Repository secrets → add `GROQ_API_KEY`, `EMAIL_ADDRESS`, `EMAIL_APP_PASSWORD`
6. Space auto-builds and deploys
7. Update `API_BASE_URL` in `Portifolio/script.js` to your Space URL

---

## Tech Stack

| Component | Technology | Cost |
|---|---|---|
| **Backend** | FastAPI + Uvicorn | Free (HF Spaces) |
| **LLM** | Groq (llama-3.1-8b-instant) | Free tier (30 req/min) |
| **Email** | smtplib + Gmail SMTP | Free (App Password) |
| **Frontend** | GitHub Pages | Free |
| **HTTP** | httpx | Free |

**Total: $0**