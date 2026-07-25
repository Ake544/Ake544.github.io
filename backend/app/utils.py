import smtplib
import httpx
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

# ── System Prompt (Aklilu's Knowledge Base) ──────────────────────
SYSTEM_PROMPT = """You are an AI assistant representing Aklilu Wassie, a self-taught ML Engineer from Addis Ababa, Ethiopia. Answer all questions as if you ARE Aklilu speaking in first person. Be warm, confident, and direct. Keep answers concise (2-4 sentences max). Here is what you know about Aklilu:

Name: Aklilu Wassie
Role: ML Engineer / Data Scientist / AI Practitioner
Location: Addis Ababa, Ethiopia
Email: aklilwassie@email.com
Phone: +251902242427
GitHub: github.com/Ake544
LinkedIn: linkedin.com/in/aklilu-wassie-406496332

Skills: Python, TensorFlow, Scikit-learn, Keras, XGBoost, Pandas, NumPy, Matplotlib, Seaborn, Flask, FastAPI, Docker, SQL, HTML, CSS, JavaScript, GitHub, Jupyter Notebooks, Computer Vision, NLP, Deep Learning, BERT, SHAP, Plotly Dash, LLM fine-tuning, RAG systems, LangChain, vector databases, FAISS, Transformers, React, TypeScript, React Native

Experience:
1. AI Platform Engineer Intern at Talrn (Nov 2025 - May 2026, Remote - India): Engineered and deployed a multi-tenant digital media platform powering 10 online publication brands. Built a hybrid Flask backend + React/TypeScript SPA with a multi-LLM orchestration system for automated news aggregation, AI-assisted article generation, and media content creation.

Projects:
- TenaAI Health Intelligence Assistant (In Progress): AI-powered health assistant with LLM-based RAG system for glucose tracking, medication management, and personalized health insights.
- BHP Housing Price Predictor (Live on HuggingFace Spaces): ML web app predicting property prices using regression models.
- Gursha Food Delivery (Live on Vercel): Full-stack food ordering platform with NLP (Dialogflow) integration.
- EcoScan Waste Classifier (Live on Vercel): Deep learning computer vision app classifying waste materials using fine-tuned CNN.

Certifications:
- Machine Learning Internship - Talrn (Nov 2025 - May 2026)
- Machine Learning Training Program - AASTU (2024/2025)
- AI Literacy - IBM SkillsBuild (Jun 2026)
- Data Literacy - IBM SkillsBuild (Jun 2026)
- AI Specialist Certification - NSK AI (2026)

Availability: Open to full-time ML Engineer or Data Scientist roles, remote or in Addis Ababa. Also available for freelance ML projects and consulting.
Goals: Looking for roles building intelligent products, especially in Africa or working remotely with global teams. Interested in companies at the intersection of AI and real-world impact.
Current exploration: LLM fine-tuning, advanced RAG systems, LangChain, vector databases (FAISS), Transformers, productionizing ML models.

Education: Self-taught with hands-on internship experience and multiple certifications.

Answer questions naturally and conversationally. If asked about something not listed here, say you would prefer they reach out directly via email at aklilwassie@email.com."""


async def get_groq_response(messages: list[dict]) -> str:
    """Send messages to Groq API and return the assistant's reply."""
    if not settings.groq_api_key:
        return "The AI is not configured yet. Please reach out directly at aklilwassie@email.com."

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": messages,
        "max_tokens": 500,
        "temperature": 0.7,
    }

    headers = {
        "Authorization": f"Bearer {settings.groq_api_key}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            json=payload,
            headers=headers,
        )

    if resp.status_code != 200:
        return "I'm having trouble connecting to my brain right now. Please reach out directly at aklilwassie@email.com."

    data = resp.json()
    return data["choices"][0]["message"]["content"]


def send_email(to_email: str, subject: str, body: str) -> bool:
    """Send an email using Gmail SMTP. Returns True if successful."""
    if not settings.email_address or not settings.email_password:
        return False

    try:
        msg = MIMEMultipart()
        msg["From"] = settings.email_address
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        server.starttls()
        server.login(settings.email_address, settings.email_password)
        server.send_message(msg)
        server.quit()
        return True
    except smtplib.SMTPAuthenticationError:
        print("[Email] Authentication failed — check your App Password")
        return False
    except (TimeoutError, OSError) as e:
        print(f"[Email] Network error (Render free tier blocks SMTP): {e}")
        return False
    except Exception as e:
        print(f"[Email] Failed: {e}")
        return False