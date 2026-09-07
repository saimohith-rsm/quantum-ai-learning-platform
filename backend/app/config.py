import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'quantum_learning.db'}")

# AI API Keys (Optional: fallbacks to internal verified quantum knowledge engine if unset)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
DEFAULT_AI_PROVIDER = os.getenv("DEFAULT_AI_PROVIDER", "gemini")

# Project Information
PROJECT_TITLE = "AI-Based Interactive Quantum Algorithm Learning Platform"
PROJECT_CODE = "26140"
HACKATHON = "Smart India Hackathon 2026"
TEAM_NAME = "Human X"
TEAM_ID = "TEAM-186"
THEME = "Smart Education"

# CORS Configuration
raw_cors = os.getenv("CORS_ORIGINS", "")
if raw_cors:
    CORS_ORIGINS = [origin.strip() for origin in raw_cors.split(",") if origin.strip()]
else:
    CORS_ORIGINS = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
    ]

# Regex for tunnel, local network, and cloud deployments
CORS_ORIGIN_REGEX = os.getenv(
    "CORS_ORIGIN_REGEX",
    r"^https?://(localhost|127\.0\.0\.1|192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|.*\.vercel\.app|.*\.onrender\.com|.*\.ngrok-free\.(app|dev))(:\d+)?$"
)
