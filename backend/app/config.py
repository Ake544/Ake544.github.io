import os
from pathlib import Path
from dotenv import load_dotenv

# Try multiple .env locations to handle different run contexts
backend_dir = Path(__file__).resolve().parent.parent  # backend/
dotenv_paths = [
    backend_dir / ".env",                          # Portifolio/backend/.env
    Path.cwd() / ".env",                           # cwd/.env
    Path.cwd().parent / ".env",                    # parent dir/.env
]

loaded = False
for p in dotenv_paths:
    if p.exists():
        load_dotenv(p)
        loaded = True
        print(f"[Config] Loaded .env from: {p}")
        break

if not loaded:
    print(f"[Config] WARNING: No .env file found. Checked: {[str(p) for p in dotenv_paths]}")


class Settings:
    groq_api_key: str = os.getenv("GROQ_API_KEY", "")
    email_address: str = os.getenv("EMAIL_ADDRESS", "")
    email_password: str = os.getenv("EMAIL_APP_PASSWORD", "")


settings = Settings()
