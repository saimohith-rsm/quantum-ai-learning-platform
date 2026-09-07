from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException
from pymongo.database import Database
from app.database import get_db, get_next_sequence
from app.schemas import ChallengeSubmissionRequest, ChallengeSubmissionResponse, CircuitSchema
from app.challenges.challenge_defs import get_all_challenges, get_challenge_by_id
from app.challenges.evaluator import evaluate_challenge_submission

router = APIRouter(prefix="/api/challenges", tags=["Interactive Challenges"])

@router.get("")
def list_challenges():
    """Lists all available quantum algorithm challenges."""
    return get_all_challenges()

@router.get("/{challenge_id}")
def get_challenge(challenge_id: str):
    """Retrieves specific challenge requirements, instructions, and test targets."""
    challenge = get_challenge_by_id(challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail=f"Challenge '{challenge_id}' not found")
    return challenge

@router.post("/{challenge_id}/submit", response_model=ChallengeSubmissionResponse)
def submit_challenge(
    challenge_id: str,
    req: ChallengeSubmissionRequest,
    db: Database = Depends(get_db)
):
    """
    Submits a circuit for automated quantum verification.
    Computes fidelity, verifies gate count, awards XP, and persists result to MongoDB.
    """
    try:
        eval_result = evaluate_challenge_submission(challenge_id, req.circuit)
        user_id = req.user_id or 1
        now = datetime.now(timezone.utc)
        sub_id = get_next_sequence("submission_id", db)

        # Record submission in DB
        submission = {
            "id": sub_id,
            "user_id": user_id,
            "challenge_id": challenge_id,
            "circuit_json": req.circuit.model_dump_json(),
            "passed": eval_result.passed,
            "fidelity": float(eval_result.fidelity),
            "score": int(eval_result.score),
            "feedback": eval_result.feedback,
            "submitted_at": now
        }
        db.challenge_submissions.insert_one(submission)

        # If passed, update user XP and badges
        if eval_result.passed:
            user = db.users.find_one({"id": user_id})
            if user:
                new_xp = user.get("xp", 0) + eval_result.score
                badge_earned = eval_result.details.get("badge_earned")
                badges_str = user.get("badges") or ""
                current_badges = [b.strip() for b in badges_str.split(",") if b.strip()]
                if badge_earned and badge_earned not in current_badges:
                    current_badges.append(badge_earned)
                
                # Dynamic level upgrade based on XP
                new_level = user.get("level", "Beginner")
                if new_xp > 500:
                    new_level = "Master"
                elif new_xp > 300:
                    new_level = "Advanced"
                elif new_xp > 150:
                    new_level = "Intermediate"

                db.users.update_one(
                    {"id": user_id},
                    {"$set": {
                        "xp": new_xp,
                        "badges": ", ".join(current_badges),
                        "level": new_level,
                        "updated_at": now
                    }}
                )

        return eval_result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

