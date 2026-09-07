import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
import app.models as models
from app.schemas import (
    SavedCircuitCreate,
    SavedCircuitResponse,
    UserResponse,
    ProgressUpdate
)

router = APIRouter(prefix="/api", tags=["Circuits & User Profile"])

# ==================== Saved Circuits ====================

@router.get("/circuits/saved", response_model=List[SavedCircuitResponse])
def get_user_circuits(user_id: int = 1, db: Session = Depends(get_db)):
    """Retrieves all saved circuits for the learner."""
    circuits = db.query(models.SavedCircuit).filter_by(user_id=user_id).order_by(models.SavedCircuit.updated_at.desc()).all()
    return circuits

@router.post("/circuits/saved", response_model=SavedCircuitResponse)
def save_circuit(circuit_in: SavedCircuitCreate, user_id: int = 1, db: Session = Depends(get_db)):
    """Saves a quantum circuit to the database."""
    circuit = models.SavedCircuit(
        user_id=user_id,
        name=circuit_in.name,
        description=circuit_in.description or "",
        num_qubits=circuit_in.num_qubits,
        circuit_json=circuit_in.circuit_json,
        is_public=circuit_in.is_public or False
    )
    db.add(circuit)
    db.commit()
    db.refresh(circuit)
    return circuit

@router.get("/circuits/saved/{circuit_id}", response_model=SavedCircuitResponse)
def get_circuit_by_id(circuit_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific saved circuit."""
    circuit = db.query(models.SavedCircuit).filter_by(id=circuit_id).first()
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return circuit

@router.delete("/circuits/saved/{circuit_id}")
def delete_circuit(circuit_id: int, user_id: int = 1, db: Session = Depends(get_db)):
    """Deletes a saved circuit."""
    circuit = db.query(models.SavedCircuit).filter_by(id=circuit_id, user_id=user_id).first()
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    db.delete(circuit)
    db.commit()
    return {"message": "Circuit deleted successfully", "id": circuit_id}

# ==================== User Profile & Progress ====================

@router.get("/user/profile")
def get_user_profile(user_id: int = 1, db: Session = Depends(get_db)):
    """Returns the user profile, level, earned badges, and statistics."""
    user = db.query(models.User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    saved_count = db.query(models.SavedCircuit).filter_by(user_id=user_id).count()
    completed_lessons = db.query(models.LearningProgress).filter_by(user_id=user_id, completed=True).count()
    passed_challenges = db.query(models.ChallengeSubmission).filter_by(user_id=user_id, passed=True).count()

    badge_list = [b.strip() for b in user.badges.split(",") if b.strip()]

    return {
        "id": user.id,
        "username": user.username,
        "display_name": user.display_name,
        "email": user.email,
        "level": user.level,
        "xp": user.xp,
        "badges": badge_list,
        "stats": {
            "saved_circuits": saved_count,
            "completed_lessons": completed_lessons,
            "passed_challenges": passed_challenges
        }
    }

@router.post("/user/progress")
def update_lesson_progress(progress_in: ProgressUpdate, db: Session = Depends(get_db)):
    """Marks a curriculum lesson as completed with quiz score."""
    record = db.query(models.LearningProgress).filter_by(
        user_id=progress_in.user_id,
        module_id=progress_in.module_id,
        lesson_id=progress_in.lesson_id
    ).first()

    if not record:
        record = models.LearningProgress(
            user_id=progress_in.user_id,
            module_id=progress_in.module_id,
            lesson_id=progress_in.lesson_id,
            completed=progress_in.completed,
            quiz_score=progress_in.quiz_score or 100.0
        )
        db.add(record)
    else:
        record.completed = progress_in.completed
        record.quiz_score = progress_in.quiz_score or 100.0

    # Award XP for lesson completion
    if progress_in.completed:
        user = db.query(models.User).filter_by(id=progress_in.user_id).first()
        if user:
            user.xp += 30

    db.commit()
    return {"message": "Progress recorded", "lesson_id": progress_in.lesson_id}
