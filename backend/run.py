import uvicorn
import os
import sys

# Ensure UTF-8 output encoding for Windows consoles
if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Ensure backend directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_banner():
    banner = """
    ========================================================================
     ⚛️  QUANTUMAI: AI-BASED INTERACTIVE QUANTUM ALGORITHM LEARNING PLATFORM
    ========================================================================
     🏆 Hackathon:          Smart India Hackathon 2026 (SIH 2026)
     🎯 Problem Statement:  #26140 - AI-Based Interactive Quantum Algorithm
                            Learning Platform
     👥 Team Name:          Human X
     🆔 Team ID:            TEAM-186
     📚 Theme:              Smart Education
    ------------------------------------------------------------------------
     🌐 Backend Server:     http://127.0.0.1:8000
     📖 Interactive Docs:   http://127.0.0.1:8000/docs
     📑 OpenAPI Specs:      http://127.0.0.1:8000/redoc
     💾 Database:           quantum_learning.db (SQLite)
    ========================================================================
    """
    try:
        print(banner)
    except UnicodeEncodeError:
        print(banner.encode("ascii", errors="replace").decode("ascii"))

if __name__ == "__main__":
    print_banner()
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0" if "PORT" in os.environ else "127.0.0.1"
    reload = "PORT" not in os.environ
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=reload
    )
