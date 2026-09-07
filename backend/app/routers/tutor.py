from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database
from app.database import get_db, get_next_sequence
from app.schemas import (
    TutorExplainRequest,
    TutorDebugRequest,
    TutorHintRequest,
    TutorChatRequest,
    TutorResponse
)
from app.tutor.ai_tutor import AITutorEngine

router = APIRouter(prefix="/api/tutor", tags=["AI Quantum Tutor"])
tutor_engine = AITutorEngine()

@router.post("/explain", response_model=TutorResponse)
def explain_circuit(req: TutorExplainRequest, db: Database = Depends(get_db)):
    """AI explains the quantum mechanics, superposition, and entanglement of the current circuit."""
    try:
        response = tutor_engine.explain_circuit(req.circuit, req.user_level)
        
        # Log to MongoDB
        try:
            lid = get_next_sequence("tutor_log_id", db)
            db.tutor_interactions.insert_one({
                "id": lid,
                "user_id": 1,
                "circuit_id": None,
                "query_type": "explain",
                "prompt": f"Explain circuit with {len(req.circuit.gates)} gates across {req.circuit.qubits} qubits",
                "response": response.explanation,
                "created_at": datetime.now(timezone.utc)
            })
        except Exception:
            pass

        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/debug", response_model=TutorResponse)
def debug_circuit(req: TutorDebugRequest, db: Database = Depends(get_db)):
    """AI diagnoses bugs, missing gates, and ordering anomalies for a specific target goal."""
    try:
        response = tutor_engine.debug_circuit(req.circuit, req.goal, req.user_level)
        
        # Log to MongoDB
        try:
            lid = get_next_sequence("tutor_log_id", db)
            db.tutor_interactions.insert_one({
                "id": lid,
                "user_id": 1,
                "circuit_id": None,
                "query_type": "debug",
                "prompt": f"Debug goal '{req.goal}' with circuit: {len(req.circuit.gates)} gates",
                "response": response.explanation,
                "created_at": datetime.now(timezone.utc)
            })
        except Exception:
            pass

        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/hint", response_model=TutorResponse)
def get_challenge_hint(req: TutorHintRequest, db: Database = Depends(get_db)):
    """Provides tiered hints for challenges (Tier 1: Nudge, Tier 2: Math clue, Tier 3: Direct solution)."""
    try:
        response = tutor_engine.generate_hint(req.challenge_id, req.circuit, req.tier)
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/chat", response_model=TutorResponse)
def chat_with_tutor(req: TutorChatRequest, db: Database = Depends(get_db)):
    """Conversational quantum computing tutor Q&A."""
    try:
        response = tutor_engine.answer_chat(
            message=req.message,
            circuit=req.circuit,
            user_level=req.user_level,
            provider=req.provider or "auto",
            socratic_mode=req.socratic_mode
        )
        
        # Log to MongoDB
        try:
            lid = get_next_sequence("tutor_log_id", db)
            db.tutor_interactions.insert_one({
                "id": lid,
                "user_id": 1,
                "circuit_id": None,
                "query_type": "chat",
                "prompt": req.message,
                "response": response.explanation,
                "created_at": datetime.now(timezone.utc)
            })
        except Exception:
            pass

        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

