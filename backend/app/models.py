from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

def utc_now():
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(64), unique=True, index=True, nullable=False)
    display_name = Column(String(128), default="Learner")
    email = Column(String(128), unique=True, nullable=True)
    password_hash = Column(String(256), nullable=True)
    level = Column(String(32), default="Beginner")  # Beginner, Intermediate, Advanced, Master
    xp = Column(Integer, default=0)
    badges = Column(Text, default="")  # Comma-separated badges
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    circuits = relationship("SavedCircuit", back_populates="user", cascade="all, delete-orphan")
    progress = relationship("LearningProgress", back_populates="user", cascade="all, delete-orphan")
    submissions = relationship("ChallengeSubmission", back_populates="user", cascade="all, delete-orphan")
    tutor_logs = relationship("TutorInteraction", back_populates="user", cascade="all, delete-orphan")

class SavedCircuit(Base):
    __tablename__ = "saved_circuits"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(Text, default="")
    num_qubits = Column(Integer, default=2)
    circuit_json = Column(Text, nullable=False)  # Serialized JSON of qubits and gate timeline
    is_public = Column(Boolean, default=False)
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

    user = relationship("User", back_populates="circuits")

class LearningProgress(Base):
    __tablename__ = "learning_progress"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    module_id = Column(String(64), nullable=False, index=True)
    lesson_id = Column(String(64), nullable=False, index=True)
    completed = Column(Boolean, default=False)
    quiz_score = Column(Float, default=0.0)
    completed_at = Column(DateTime, default=utc_now)

    user = relationship("User", back_populates="progress")

class ChallengeSubmission(Base):
    __tablename__ = "challenge_submissions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    challenge_id = Column(String(64), nullable=False, index=True)
    circuit_json = Column(Text, nullable=False)
    passed = Column(Boolean, default=False)
    fidelity = Column(Float, default=0.0)
    score = Column(Integer, default=0)
    feedback = Column(Text, default="")
    submitted_at = Column(DateTime, default=utc_now)

    user = relationship("User", back_populates="submissions")

class TutorInteraction(Base):
    __tablename__ = "tutor_interactions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    circuit_id = Column(Integer, nullable=True)
    query_type = Column(String(32), default="chat")  # explain, debug, hint, chat
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    created_at = Column(DateTime, default=utc_now)

    user = relationship("User", back_populates="tutor_logs")
