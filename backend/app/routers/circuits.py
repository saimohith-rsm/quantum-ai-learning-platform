from datetime import datetime, timezone
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database
from app.database import get_db, get_next_sequence
from app.schemas import (
    SavedCircuitCreate,
    SavedCircuitResponse,
    UserResponse,
    ProgressUpdate
)

router = APIRouter(prefix="/api", tags=["Circuits & User Profile"])

# ==================== Saved Circuits ====================

@router.get("/circuits/saved", response_model=List[SavedCircuitResponse])
def get_user_circuits(user_id: int = 1, db: Database = Depends(get_db)):
    """Retrieves all saved circuits for the learner."""
    circuits = list(db.saved_circuits.find({"user_id": user_id}).sort("updated_at", -1))
    return [SavedCircuitResponse.model_validate(c) for c in circuits]

@router.post("/circuits/saved", response_model=SavedCircuitResponse)
def save_circuit(circuit_in: SavedCircuitCreate, user_id: int = 1, db: Database = Depends(get_db)):
    """Saves a quantum circuit to the database."""
    cid = get_next_sequence("circuit_id", db)
    now = datetime.now(timezone.utc)
    doc = {
        "id": cid,
        "user_id": user_id,
        "name": circuit_in.name,
        "description": circuit_in.description or "",
        "num_qubits": circuit_in.num_qubits,
        "circuit_json": circuit_in.circuit_json,
        "is_public": bool(circuit_in.is_public),
        "created_at": now,
        "updated_at": now
    }
    db.saved_circuits.insert_one(doc)
    return SavedCircuitResponse.model_validate(doc)

@router.get("/circuits/saved/{circuit_id}", response_model=SavedCircuitResponse)
def get_circuit_by_id(circuit_id: int, db: Database = Depends(get_db)):
    """Retrieves a specific saved circuit."""
    circuit = db.saved_circuits.find_one({"id": circuit_id})
    if not circuit:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return SavedCircuitResponse.model_validate(circuit)

@router.delete("/circuits/saved/{circuit_id}")
def delete_circuit(circuit_id: int, user_id: int = 1, db: Database = Depends(get_db)):
    """Deletes a saved circuit."""
    res = db.saved_circuits.delete_one({"id": circuit_id, "user_id": user_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Circuit not found")
    return {"message": "Circuit deleted successfully", "id": circuit_id}

# ==================== User Profile & Progress ====================

@router.get("/user/profile")
def get_user_profile(user_id: int = 1, db: Database = Depends(get_db)):
    """Returns the user profile, level, earned badges, and statistics."""
    user = db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    saved_count = db.saved_circuits.count_documents({"user_id": user_id})
    completed_lessons = db.learning_progress.count_documents({"user_id": user_id, "completed": True})
    passed_challenges = db.challenge_submissions.count_documents({"user_id": user_id, "passed": True})

    badges_str = user.get("badges") or ""
    badge_list = [b.strip() for b in badges_str.split(",") if b.strip()]

    return {
        "id": user["id"],
        "username": user["username"],
        "display_name": user.get("display_name", user["username"]),
        "email": user.get("email"),
        "level": user.get("level", "Beginner"),
        "xp": user.get("xp", 0),
        "badges": badge_list,
        "stats": {
            "saved_circuits": saved_count,
            "completed_lessons": completed_lessons,
            "passed_challenges": passed_challenges
        }
    }

@router.post("/user/progress")
def update_lesson_progress(progress_in: ProgressUpdate, db: Database = Depends(get_db)):
    """Marks a curriculum lesson as completed with quiz score."""
    now = datetime.now(timezone.utc)
    db.learning_progress.update_one(
        {"user_id": progress_in.user_id, "lesson_id": progress_in.lesson_id},
        {"$set": {
            "module_id": progress_in.module_id,
            "completed": progress_in.completed,
            "quiz_score": progress_in.quiz_score or 100.0,
            "completed_at": now
        }},
        upsert=True
    )

    # Award XP for lesson completion
    if progress_in.completed:
        db.users.update_one(
            {"id": progress_in.user_id},
            {"$inc": {"xp": 30}}
        )

    return {"message": "Progress recorded", "lesson_id": progress_in.lesson_id}

