# ⚛️ QuantumAI Backend - Interactive Quantum Algorithm Learning Platform
**Smart India Hackathon 2026 (SIH 2026)**  
**Problem Statement #26140**: AI-Based Interactive Quantum Algorithm Learning Platform  
**Team**: Human X (`TEAM-186`) | **Theme**: Smart Education  

---

## Overview
This is the complete, production-ready backend engine for the **QuantumAI Interactive Quantum Algorithm Learning Platform**. Built with **FastAPI**, **SQLAlchemy**, and **NumPy**, it provides:

1. **Statevector Quantum Simulator Engine**:
   - Exact tensor-based matrix mechanics for $1$ to $8$ qubits.
   - Computes reduced density matrices $\rho_k$ and extracts single-qubit $(x, y, z)$ coordinates for 3D Bloch sphere visualization.
   - Step-by-step statevector evolution tracking for timeline scrubber debugging.
   - Monte-Carlo shot simulation (e.g. 1024 shots).
   - Instant export to runnable **IBM Qiskit 1.0+** Python code and **OpenQASM 2.0**.
2. **AI Quantum Tutor Engine**:
   - Circuit Explainer: Translates state transformations and gates into intuitive physical explanations.
   - Circuit Debugger: Identifies missing gates, ordering bugs, or phase kickback issues.
   - Socratic Hint System: Tier 1 (intuition nudge), Tier 2 (mathematical formula), Tier 3 (concrete circuit action).
   - Conversational Q&A: Grounded in verified quantum physics principles (supports optional Gemini API via `GEMINI_API_KEY`).
3. **Curriculum & Algorithm Library**:
   - Structured learning modules with lessons, interactive starter circuits, and embedded quizzes.
   - Pre-built landmark algorithms: Bell States, Grover's 2-Qubit Search, Deutsch-Jozsa, Quantum Teleportation, Superdense Coding, 3-Qubit QFT, and Quantum Random Number Generator.
4. **Challenge & Assessment Arena**:
   - Automated grading of user circuits against quantum target states using classical fidelity and variation distance.
   - Real-time scoring, XP progression, and badge awards.
5. **Database (SQLite + SQLAlchemy)**:
   - Persists user profiles, custom saved circuits, lesson progress, challenge submissions, and AI tutor interaction logs.

---

## Directory Structure
```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py                 # Configuration, CORS, environment variables
│   ├── database.py               # SQLite engine, sessionmaker, init_db seed
│   ├── models.py                 # SQLAlchemy models (User, Circuit, Progress, Submission, TutorLog)
│   ├── schemas.py                # Pydantic request/response validation models
│   ├── quantum/
│   │   ├── gates.py              # Quantum gate matrices & tensor operations
│   │   ├── simulator.py          # Statevector & Bloch vector simulator
│   │   ├── qiskit_export.py      # Qiskit Python & OpenQASM generator
│   │   └── presets.py            # Pre-built standard quantum algorithms
│   ├── tutor/
│   │   ├── ai_tutor.py           # Multi-mode AI tutor (Explain, Debug, Hint, Chat)
│   │   └── quantum_kb.py         # Grounded quantum knowledge base & bug rules
│   ├── curriculum/
│   │   └── lessons.py            # Modules, lessons, markdown content & quizzes
│   ├── challenges/
│   │   ├── challenge_defs.py     # Challenge specifications & criteria
│   │   └── evaluator.py          # Automated circuit verification & grader
│   ├── routers/
│   │   ├── quantum.py            # /api/quantum endpoints
│   │   ├── tutor.py              # /api/tutor endpoints
│   │   ├── curriculum.py         # /api/curriculum endpoints
│   │   ├── challenges.py         # /api/challenges endpoints
│   │   └── circuits.py           # /api/circuits & user profile endpoints
│   └── main.py                   # FastAPI application instance & lifespan
├── tests/
│   ├── test_backend.py           # Quantum simulation & evaluator unit tests
│   └── test_api_endpoints.py     # FastAPI REST API integration tests
├── requirements.txt
├── run.py                        # Standalone runner with banner
└── quantum_learning.db           # SQLite database
```

---

## How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Backend Server
```bash
python run.py
```
Or with Uvicorn directly:
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 3. Open Interactive API Documentation
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
- **System Health**: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

### 4. Run Test Suite
```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## Key API Endpoints

### 🔬 Quantum Simulation
- `POST /api/quantum/simulate`
  - Input: Circuit JSON (`qubits`, `gates` with target, control, step, params) + `shots`
  - Output: Final statevector, probabilities, shot distribution, step-by-step history, Bloch vectors $(x, y, z)$, Qiskit code, OpenQASM.
- `POST /api/quantum/export/qiskit`
  - Returns runnable Python Qiskit code.
- `POST /api/quantum/export/qasm`
  - Returns OpenQASM 2.0 circuit definition.
- `GET /api/quantum/presets`
  - Returns list of pre-built standard algorithms.

### 🤖 AI Quantum Tutor
- `POST /api/tutor/explain`
  - Analyzes circuit and provides step-by-step physical breakdown.
- `POST /api/tutor/debug`
  - Diagnoses why a circuit fails to achieve a specific target algorithm.
- `POST /api/tutor/hint`
  - Returns Tier 1 (Nudge), Tier 2 (Math clue), or Tier 3 (Circuit solution) hints.
- `POST /api/tutor/chat`
  - Conversational Q&A on quantum mechanics.

### 📚 Curriculum & Challenges
- `GET /api/curriculum/modules` - Learning paths & lessons.
- `GET /api/challenges` - Interactive challenge list.
- `POST /api/challenges/{challenge_id}/submit` - Automated circuit grading & XP reward.

### 💾 Database & User Profile
- `GET /api/circuits/saved` - List saved circuits.
- `POST /api/circuits/saved` - Save new circuit.
- `GET /api/user/profile` - Get learner profile, badges, level, and stats.
