from datetime import datetime, timezone
from typing import Optional, Any, Dict

def utc_now():
    return datetime.now(timezone.utc)

class DocumentModel:
    """Base document model with dual attribute and dict-like access for MongoDB documents."""
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.to_dict()})"

class User(DocumentModel):
    id: int
    username: str
    display_name: str = "Learner"
    email: Optional[str] = None
    password_hash: Optional[str] = None
    level: str = "Beginner"
    xp: int = 0
    badges: str = ""
    created_at: Any = None
    updated_at: Any = None

class SavedCircuit(DocumentModel):
    id: int
    user_id: int
    name: str
    description: str = ""
    num_qubits: int = 2
    circuit_json: str = "{}"
    is_public: bool = False
    created_at: Any = None
    updated_at: Any = None

class LearningProgress(DocumentModel):
    id: Optional[int] = None
    user_id: int
    module_id: str
    lesson_id: str
    completed: bool = False
    quiz_score: float = 0.0
    completed_at: Any = None

class ChallengeSubmission(DocumentModel):
    id: Optional[int] = None
    user_id: int
    challenge_id: str
    circuit_json: str
    passed: bool = False
    fidelity: float = 0.0
    score: int = 0
    feedback: str = ""
    submitted_at: Any = None

class TutorInteraction(DocumentModel):
    id: Optional[int] = None
    user_id: Optional[int] = 1
    circuit_id: Optional[int] = None
    query_type: str = "chat"
    prompt: str = ""
    response: str = ""
    created_at: Any = None

