# ⚛️ QuantumAI Frontend - Interactive Quantum Learning Interface
**Smart India Hackathon 2026 (SIH 2026)**  
**Problem Statement #26140**: AI-Based Interactive Quantum Algorithm Learning Platform  
**Team**: Human X (`TEAM-186`) | **Theme**: Smart Education  

---

## Overview
A modern, responsive, high-performance web interface built with **React (Vite)**, **Tailwind CSS**, **Three.js**, and **Lucide Icons**. It gives learners hands-on access to quantum computing via:

1. **Interactive Multi-Qubit Circuit Studio**:
   - Visual timeline grid with drag-and-drop / click-to-place gates.
   - Single-qubit gates ($H, X, Y, Z, S, T, R_x, R_y, R_z$).
   - Two/Three-qubit entangling gates ($CNOT, CZ, SWAP, Toffoli, CPHASE$).
   - Step-by-step playback scrubber allowing gate-by-gate quantum state inspection.
2. **Interactive 3D Bloch Sphere (Three.js)**:
   - Full 3D orbital rotation controls (drag to rotate in 3D).
   - Real-time Bloch vector arrow, coordinate axes, and pole indicators ($|0\rangle, |1\rangle$).
   - Purity meter warning when individual qubits become entangled.
3. **Statevector & Measurement Visualizers**:
   - Statevector inspector showing complex amplitudes and polar phase hue badges.
   - Measurement histogram chart simulating 1024 shots with probabilities and percentages.
4. **AI Quantum Tutor Panel**:
   - Conversational assistant grounded in verified quantum mechanics.
   - One-click "Explain Circuit" and "Diagnose Circuit" buttons.
   - Quick prompt chips for fast learning inquiries.
5. **Interactive Curriculum & Quizzes**:
   - Guided modules and lessons with LaTeX mathematical formulas.
   - One-click "Open in Circuit Studio" button for starter exercises.
   - Checkpoint quizzes with immediate feedback, awarding XP and updating learner rank.
6. **Challenge Arena**:
   - Hands-on algorithm challenges (Bell State, GHZ State, Grover's Search).
   - Automated grading against target states with classical fidelity calculations.
   - Celebratory confetti effects and badge unlocks.
7. **Export & Database Integration**:
   - One-click export to runnable **IBM Qiskit 1.0+** Python code and **OpenQASM 2.0**.
   - Save circuits to local **SQLite** database and reload anytime.

---

## How to Run

### Development Mode
```bash
npm run dev
```
Opens on **[http://localhost:5173](http://localhost:5173)**. (Automatically proxies API calls to `http://127.0.0.1:8000`).

### Production Build
```bash
npm run build
```
Generates optimized static assets in `dist/`.
