from fastapi import APIRouter, Depends, HTTPException, Header
from typing import Optional
from datetime import datetime, timezone
from pymongo.database import Database
from app.database import get_db, get_next_sequence
import app.models as models
from app.schemas import UserRegister, UserLogin, AuthResponse, UserResponse
from app.auth import hash_password, verify_password, create_access_token, verify_access_token

router = APIRouter(prefix="/api/auth", tags=["Authentication & Accounts"])

def get_current_user_from_token(
    authorization: Optional[str] = Header(None),
    db: Database = Depends(get_db)
) -> Optional[dict]:
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
    return db.users.find_one({"id": user_id})

@router.post("/register", response_model=AuthResponse)
def register_user(req: UserRegister, db: Database = Depends(get_db)):
    """Registers a new learner account."""
    clean_username = req.username.strip().lower()
    if not clean_username or len(clean_username) < 3:
        raise HTTPException(status_code=400, detail="Username must be at least 3 characters long")

    if len(req.password) < 4:
        raise HTTPException(status_code=400, detail="Password must be at least 4 characters long")

    # Check existing username
    existing_user = db.users.find_one({"username": clean_username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username is already taken")

    # Check existing email if provided
    clean_email = None
    if req.email and req.email.strip():
        clean_email = req.email.strip().lower()
        existing_email = db.users.find_one({"email": clean_email})
        if existing_email:
            raise HTTPException(status_code=400, detail="Email is already registered")

    new_id = get_next_sequence("user_id", db)
    now = datetime.now(timezone.utc)
    new_user = {
        "id": new_id,
        "username": clean_username,
        "display_name": req.display_name.strip() if req.display_name else clean_username.title(),
        "email": clean_email,
        "password_hash": hash_password(req.password),
        "level": "Beginner",
        "xp": 0,
        "badges": "Quantum Initiate",
        "created_at": now,
        "updated_at": now
    }
    db.users.insert_one(new_user)

    token = create_access_token(new_id, clean_username)
    return AuthResponse(token=token, user=UserResponse.model_validate(new_user))

@router.post("/login", response_model=AuthResponse)
def login_user(req: UserLogin, db: Database = Depends(get_db)):
    """Authenticates a user by username or email and password."""
    identifier = req.username.strip().lower()
    
    # Try username or email match
    user = db.users.find_one({
        "$or": [
            {"username": identifier},
            {"email": identifier}
        ]
    })

    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    password_hash = user.get("password_hash")
    if not password_hash or not verify_password(req.password, password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(user["id"], user["username"])
    return AuthResponse(token=token, user=UserResponse.model_validate(user))

@router.post("/demo-login", response_model=AuthResponse)
def demo_login(db: Database = Depends(get_db)):
    """One-click instant login as default demo learner (Quantum Explorer)."""
    user = db.users.find_one({"username": "quantum_explorer"})
    if not user:
        new_id = get_next_sequence("user_id", db)
        now = datetime.now(timezone.utc)
        user = {
            "id": new_id,
            "username": "quantum_explorer",
            "display_name": "Quantum Explorer",
            "email": "explorer@quantum.learn",
            "password_hash": hash_password("quantum123"),
            "level": "Beginner",
            "xp": 150,
            "badges": "Superposition Novice, Entanglement Spark",
            "created_at": now,
            "updated_at": now
        }
        db.users.insert_one(user)

    token = create_access_token(user["id"], user["username"])
    return AuthResponse(token=token, user=UserResponse.model_validate(user))

@router.get("/me")
def get_current_user_profile(
    authorization: Optional[str] = Header(None),
    token: Optional[str] = None,
    db: Database = Depends(get_db)
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
    user = db.users.find_one({"id": user_id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    saved_count = db.saved_circuits.count_documents({"user_id": user["id"]})
    completed_lessons = db.learning_progress.count_documents({"user_id": user["id"], "completed": True})
    passed_challenges = db.challenge_submissions.count_documents({"user_id": user["id"], "passed": True})
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

