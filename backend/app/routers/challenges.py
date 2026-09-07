import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import ChallengeSubmissionRequest, ChallengeSubmissionResponse, CircuitSchema
from app.challenges.challenge_defs import get_all_challenges, get_challenge_by_id
from app.challenges.evaluator import evaluate_challenge_submission
import app.models as models

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
    db: Session = Depends(get_db)
):
    """
    Submits a circuit for automated quantum verification.
    Computes fidelity, verifies gate count, awards XP, and persists result to the database.
    """
    try:
        eval_result = evaluate_challenge_submission(challenge_id, req.circuit)
        user_id = req.user_id or 1

        # Record submission in DB
        submission = models.ChallengeSubmission(
            user_id=user_id,
            challenge_id=challenge_id,
            circuit_json=req.circuit.model_dump_json(),
            passed=eval_result.passed,
            fidelity=eval_result.fidelity,
            score=eval_result.score,
            feedback=eval_result.feedback
        )
        db.add(submission)

        # If passed, update user XP and badges
        if eval_result.passed:
            user = db.query(models.User).filter_by(id=user_id).first()
            if user:
                user.xp += eval_result.score
                badge_earned = eval_result.details.get("badge_earned")
                if badge_earned:
                    current_badges = [b.strip() for b in user.badges.split(",") if b.strip()]
                    if badge_earned not in current_badges:
                        current_badges.append(badge_earned)
                        user.badges = ", ".join(current_badges)
                
                # Dynamic level upgrade based on XP
                if user.xp > 500:
                    user.level = "Master"
                elif user.xp > 300:
                    user.level = "Advanced"
                elif user.xp > 150:
                    user.level = "Intermediate"

        db.commit()
        return eval_result
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
