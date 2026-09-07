from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
import app.models as models
from app.schemas import UserRegister, UserLogin, AuthResponse, UserResponse
from app.auth import hash_password, verify_password, create_access_token, verify_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication & Accounts"])

def get_current_user_from_token(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> Optional[models.User]:
    """Helper to extract and authenticate current user from Bearer header."""
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    token = parts[1]
    payload = verify_access_token(token)
    if not payload:
        return None
    user_id = payload.get("uid")
    return db.query(models.User).filter_by(id=user_id).first()

@router.post("/register", response_model=AuthResponse)
def register_user(req: UserRegister, db: Session = Depends(get_db)):
    """Registers a new learner account."""
    clean_username = req.username.strip().lower()
    if not clean_username or len(clean_username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters long")

    if len(req.password) < 4:
        raise HTTPException(status_code=400, detail="Password must be at least 4 characters long")

    # Check existing username
    existing_user = db.query(models.User).filter_by(username=clean_username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username is already taken")

    # Check existing email if provided
    if req.email and req.email.strip():
        existing_email = db.query(models.User).filter_by(email=req.email.strip().lower()).first()
        if existing_email:
            raise HTTPException(status_code=400, detail="Email is already registered")

    new_user = models.User(
        username=clean_username,
        display_name=req.display_name.strip() if req.display_name else clean_username.title(),
        email=req.email.strip().lower() if req.email else None,
        password_hash=hash_password(req.password),
        level="Beginner",
        xp=0,
        badges="Quantum Initiate"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    token = create_access_token(new_user.id, new_user.username)
    return AuthResponse(token=token, user=UserResponse.model_validate(new_user))

@router.post("/login", response_model=AuthResponse)
def login_user(req: UserLogin, db: Session = Depends(get_db)):
    """Authenticates a user by username or email and password."""
    identifier = req.username.strip().lower()
    
    # Try username or email match
    user = db.query(models.User).filter(
        (models.User.username == identifier) | (models.User.email == identifier)
    ).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not user.password_hash or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(user.id, user.username)
    return AuthResponse(token=token, user=UserResponse.model_validate(user))

@router.post("/demo-login", response_model=AuthResponse)
def demo_login(db: Session = Depends(get_db)):
    """One-click instant login as default demo learner (Quantum Explorer)."""
    user = db.query(models.User).filter_by(username="quantum_explorer").first()
    if not user:
        user = models.User(
            username="quantum_explorer",
            display_name="Quantum Explorer",
            email="explorer@quantum.learn",
            password_hash=hash_password("quantum123"),
            level="Beginner",
            xp=150,
            badges="Superposition Novice, Entanglement Spark"
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    token = create_access_token(user.id, user.username)
    return AuthResponse(token=token, user=UserResponse.model_validate(user))

@router.get("/me")
def get_current_user_profile(
    authorization: Optional[str] = Header(None),
    token: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Retrieves current user profile and statistics based on session token."""
    raw_token = token
    if not raw_token and authorization:
        parts = authorization.split()
        if len(parts) == 2 and parts[0].lower() == "bearer":
            raw_token = parts[1]

    if not raw_token:
        raise HTTPException(status_code=401, detail="Authentication token required")

    payload = verify_access_token(raw_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("uid")
    user = db.query(models.User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    saved_count = db.query(models.SavedCircuit).filter_by(user_id=user.id).count()
    completed_lessons = db.query(models.LearningProgress).filter_by(user_id=user.id, completed=True).count()
    passed_challenges = db.query(models.ChallengeSubmission).filter_by(user_id=user.id, passed=True).count()
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
