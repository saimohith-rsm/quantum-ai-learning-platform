from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import (
    PROJECT_TITLE,
    PROJECT_CODE,
    HACKATHON,
    TEAM_NAME,
    TEAM_ID,
    THEME,
    CORS_ORIGINS,
    CORS_ORIGIN_REGEX
)
from app.database import init_db
from app.routers import (
    auth,
    quantum,
    tutor,
    curriculum,
    challenges,
    circuits
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database and seed starter data
    print("🚀 Initializing QuantumAI Database & Models...")
    init_db()
    print("✅ Database initialized successfully!")
    yield
    print("🛑 Shutting down QuantumAI Backend...")

app = FastAPI(
    title=f"QuantumAI - {PROJECT_TITLE}",
    description=(
        f"API Backend for {HACKATHON} (Problem Statement #{PROJECT_CODE}, Team: {TEAM_NAME} [{TEAM_ID}]). "
        "Provides exact statevector quantum simulation, step-by-step 3D Bloch sphere vector calculations, "
        "an AI Quantum Tutor with diagnostic capabilities, curriculum modules, and interactive challenges."
    ),
    version="1.0.0",
    lifespan=lifespan
)

# Security Headers Middleware
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    return response

# Configure CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_origin_regex=CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(auth.router)
app.include_router(quantum.router)
app.include_router(tutor.router)
app.include_router(curriculum.router)
app.include_router(challenges.router)
app.include_router(circuits.router)

@app.get("/")
def root():
    return {
        "status": "online",
        "platform": PROJECT_TITLE,
        "hackathon": HACKATHON,
        "problem_statement_id": PROJECT_CODE,
        "team_name": TEAM_NAME,
        "team_id": TEAM_ID,
        "theme": THEME,
        "documentation": "/docs",
        "interactive_openapi": "/redoc"
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "quantum_engine": "ready",
        "supported_gates": [
            "H", "X", "Y", "Z", "S", "SDG", "T", "TDG",
            "RX", "RY", "RZ", "PHASE",
            "CNOT", "CZ", "SWAP", "CCX (Toffoli)", "CPHASE"
        ],
        "features": [
            "Exact Statevector Simulation",
            "3D Bloch Sphere Vector Computation",
            "Step-by-Step Gate Execution Timeline",
            "Monte Carlo Measurement Shot Simulator",
            "AI Quantum Tutor & Explainer",
            "Circuit Bug Detective & Tiered Hints",
            "Automated Challenge Grader & State Fidelity Verification",
            "Export to IBM Qiskit & OpenQASM 2.0"
        ]
    }
