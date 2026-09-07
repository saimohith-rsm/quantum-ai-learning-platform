import os
import hashlib
import secrets
import base64
import json
import time
from typing import Optional, Dict, Any

SECRET_SALT = os.getenv("JWT_SECRET", "quantum-ai-sih-2026-human-x-secret")

def hash_password(password: str) -> str:
    """Hashes a password using PBKDF2-HMAC-SHA256 with a unique salt."""
    salt = secrets.token_hex(16)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt), 100000)
    return f"{salt}${key.hex()}"

def verify_password(password: str, stored_hash: str) -> bool:
    """Verifies a plaintext password against a stored PBKDF2 hash."""
    if not stored_hash or "$" not in stored_hash:
        return False
    try:
        salt, key_hex = stored_hash.split("$", 1)
        new_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt), 100000)
        return secrets.compare_digest(new_key.hex(), key_hex)
    except Exception:
        return False

def create_access_token(user_id: int, username: str, expires_in_seconds: int = 86400 * 7) -> str:
    """Generates a signed, self-contained bearer token for session authentication."""
    payload = {
        "uid": user_id,
        "usr": username,
        "exp": int(time.time()) + expires_in_seconds
    }
    payload_bytes = json.dumps(payload).encode('utf-8')
    payload_b64 = base64.urlsafe_b64encode(payload_bytes).decode('utf-8').rstrip('=')
    
    # Sign payload
    sig = hashlib.sha256((payload_b64 + SECRET_SALT).encode('utf-8')).hexdigest()
    return f"{payload_b64}.{sig}"

def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Validates token signature and expiration, returning the user payload if valid."""
    if not token or "." not in token:
        return None
    try:
        payload_b64, sig = token.split(".", 1)
        expected_sig = hashlib.sha256((payload_b64 + SECRET_SALT).encode('utf-8')).hexdigest()
        if not secrets.compare_digest(sig, expected_sig):
            return None
        
        # Add padding back if necessary
        padded = payload_b64 + '=' * (-len(payload_b64) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded).decode('utf-8'))
        
        if payload.get("exp", 0) < time.time():
            return None  # Expired
            
        return payload
    except Exception:
        return None
