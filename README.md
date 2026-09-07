# ⚛️ QuantumAI: Interactive Quantum Algorithm Learning Platform

[![Smart India Hackathon 2026](https://img.shields.io/badge/SIH-2026-blue.svg)](https://www.sih.gov.in/)
[![Problem Statement](https://img.shields.io/badge/Problem%20Statement-26140-green.svg)](https://www.sih.gov.in/)
[![Theme](https://img.shields.io/badge/Theme-Smart%20Education-orange.svg)](https://www.sih.gov.in/)
[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3-61dafb.svg)](https://react.dev/)
[![Three.js](https://img.shields.io/badge/Three.js-0.162-black.svg)](https://threejs.org/)
[![Tests](https://img.shields.io/badge/Tests-25%2F25%20Passing-success.svg)](backend/tests/)

> **Smart India Hackathon 2026 (SIH 2026)**  
> - **Problem Statement ID**: `26140`  
> - **Problem Statement Title**: AI-Based Interactive Quantum Algorithm Learning Platform  
> - **Team**: Human X (`TEAM-186`)  
> - **Category**: Software | **Theme**: Smart Education  

---

## 📖 Executive Overview

The **QuantumAI Platform** turns abstract, mathematically intimidating quantum computing concepts into an interactive, visual, and AI-guided learning journey.

Democratizing quantum computing education in alignment with India's **National Quantum Mission (NQM)**, the platform enables students, educators, and researchers to:
- **Build**: Design quantum circuits on a multi-qubit visual timeline grid with live drag-and-drop gates.
- **Simulate**: Execute exact statevector linear algebra ($2^n$ complex Hilbert space) with step-by-step gate evolution and Monte Carlo measurement shot sampling.
- **Visualize**: Orbit an interactive **3D Bloch Sphere** (Three.js WebGL), inspect complex statevector amplitudes and phase wheels, and view live measurement histograms.
- **Consult AI**: An intelligent **AI Quantum Tutor** explains circuit mechanics, diagnoses circuit bugs, and provides Socratic hints.
- **NISQ Noise Simulation**: Simulate realistic quantum hardware noise (T1 energy relaxation, T2 dephasing, depolarizing gate errors, and readout SPAM error).
- **Universal Transpilation**: Export visual circuits into runnable code for **IBM Qiskit 1.0+**, **Google Cirq**, **PennyLane**, **Amazon Braket**, and **OpenQASM 2.0/3.0**.
- **Interactive Protocols**: Simulate quantum cryptographic protocols like **BB84 Quantum Key Distribution (QKD)** with eavesdropping detection and QBER calculation.
- **Gamified Curriculum**: Complete structured curriculum modules with embedded quizzes, and validate algorithms in the **Challenge Arena** with automated fidelity grading.

---

## 🏗️ System Architecture

```
sihh/
├── backend/                      # Python 3.12 + FastAPI + SQLite + NumPy
│   ├── app/
│   │   ├── main.py               # FastAPI application entrypoint & security middleware
│   │   ├── config.py             # Environment variables, CORS & SIH metadata
│   │   ├── database.py           # SQLAlchemy engine, connection pooling & auto-seeding
│   │   ├── models.py             # Database models (User, Circuit, Progress, Challenges)
│   │   ├── schemas.py            # Pydantic v2 validation models & ConfigDict
│   │   ├── auth.py               # PBKDF2 password hashing & signed bearer tokens
│   │   ├── quantum/              # Exact tensor statevector engine & Bloch vector math
│   │   ├── tutor/                # AI Tutor engine, circuit explainer, debugger & KB
│   │   ├── curriculum/           # Modules, lessons, and interactive quizzes
│   │   ├── challenges/           # Challenge definitions & automated test grader
│   │   └── routers/              # Modular REST API endpoints
│   ├── tests/                    # 25/25 Passing Unit & Integration tests (pytest)
│   ├── run.py                    # Standalone backend launcher with dynamic port binding
│   ├── requirements.txt          # Python dependencies
│   ├── view_db.py                # Terminal SQLite database inspector
│   └── .env.example              # Backend environment template
├── frontend/                     # React 18 + Vite + Three.js + Tailwind CSS
│   ├── src/
│   │   ├── components/           # UI components (CircuitBuilder, BlochSphere3D, etc.)
│   │   ├── context/              # Global reactive quantum state (QuantumContext)
│   │   └── services/api.js       # Backend REST API client with configurable base URL
│   ├── package.json              # Node dependencies
│   ├── vite.config.js            # Vite configuration with vendor chunking & proxy
│   ├── vercel.json               # Vercel deployment & SPA routing configuration
│   └── .env.example              # Frontend environment template
├── start_all.bat                 # ⭐ 1-Click Windows Full Platform Launcher
├── start_all.ps1                 # PowerShell Full Platform Launcher
├── setup_on_new_laptop.bat       # 1-Click First-Time Setup on New Machine
├── DEPLOYMENT.md                 # Cloud deployment guide (Render + Vercel)
└── README.md
```

---

## ⚡ Quick Start: How to Run the Platform

### Method 1: 1-Click Launch (Recommended)
Simply double-click **`start_all.bat`** in the root folder.  
It automatically:
1. Clears any stale processes holding ports `8000` or `5173`.
2. Starts the **FastAPI Backend** on `http://127.0.0.1:8000`.
3. Starts the **React Frontend** on `http://localhost:5173`.
4. Automatically opens your default browser to `http://localhost:5173`.

### Method 2: Inside VS Code
1. Open the folder in VS Code (`File` ➔ `Open Folder...`).
2. Press <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>B</kbd>.
3. Both servers boot in integrated split terminal panels.

### Method 3: Manual Commands
```powershell
# Terminal 1 - Backend:
cd backend
python run.py

# Terminal 2 - Frontend:
cd frontend
npm run dev
```

---

## 🌐 Endpoints & URLs

| Service | Local URL | Description |
| :--- | :--- | :--- |
| **Frontend Web App** | `http://localhost:5173` | Interactive React + Three.js application |
| **Backend API Docs** | `http://127.0.0.1:8000/docs` | Interactive Swagger UI for testing all endpoints |
| **Alternative OpenAPI** | `http://127.0.0.1:8000/redoc` | Redoc visual API documentation |
| **Health Check** | `http://127.0.0.1:8000/api/health` | Backend status, engine readiness & supported gates |

---

## ⚙️ Environment Variables

### Backend (`backend/.env.example`)
| Variable | Default | Description |
| :--- | :--- | :--- |
| `PORT` | `8000` | Server listening port (dynamically handled on cloud hosts like Render) |
| `HOST` | `127.0.0.1` | Server binding address (`0.0.0.0` in cloud environments) |
| `DATABASE_URL` | `sqlite:///quantum_learning.db` | SQLAlchemy database connection string |
| `JWT_SECRET` | `quantum-ai-sih-2026-...` | Secret salt for session signing (set custom value in production) |
| `CORS_ORIGINS` | Localhost origins | Comma-separated list of allowed frontend domains |
| `GEMINI_API_KEY` | *(Optional)* | Optional key for expanded LLM tutor answers (built-in quantum KB is used if unset) |

### Frontend (`frontend/.env.example`)
| Variable | Default | Description |
| :--- | :--- | :--- |
| `VITE_API_BASE` | `/api` | Base API route (set to cloud backend URL on production deployments) |

---

## 🧪 Testing & Code Quality

### Backend Automated Test Suite
```powershell
cd backend
pytest -v
```
**Results:**
- **25 / 25 Passing Tests (100% Pass Rate)** with **0 warnings**
- Tests cover: exact statevector evolution, Bell state entanglement, Grover search, Pauli gates, Qiskit/QASM export, AI tutor diagnostics, noisy simulation, BB84 protocol, multi-SDK transpilation, auth token validation, security headers, and database CRUD.

### Frontend Production Build & Code-Splitting
```powershell
cd frontend
npm run build
```
**Results:**
- Zero bundle warnings.
- Large vendor dependencies are cleanly isolated:
  - `vendor-three.js` (~465 kB WebGL rendering engine)
  - `vendor-react.js` (~133 kB framework)
  - `vendor-icons.js` (~36 kB icons & confetti)
  - `index.js` (~90 kB application logic)

---

## 🚀 Cloud Deployment

The platform is designed to be hosted for **100% free** on cloud infrastructure:
- **Frontend**: Deploy to **Vercel** (`npm run build`, output: `dist`, root: `frontend`).
- **Backend**: Deploy to **Render.com** as a free Web Service (`pip install -r requirements.txt`, start: `python run.py`, root: `backend`).

See [DEPLOYMENT.md](DEPLOYMENT.md) for step-by-step instructions.

---

## 👥 Team Human X (SIH 2026)
- **Problem Statement**: #26140 - AI-Based Interactive Quantum Algorithm Learning Platform
- **Theme**: Smart Education
- **Category**: Software
