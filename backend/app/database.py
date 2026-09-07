import os
from datetime import datetime, timezone
from typing import Optional, Generator
from pymongo import MongoClient, ASCENDING, ReturnDocument
from pymongo.database import Database
from app.config import MONGODB_URI, MONGODB_DB_NAME
from app.auth import hash_password

_client: Optional[MongoClient] = None

def get_client() -> MongoClient:
    """Returns a singleton MongoClient with connection pooling."""
    global _client
    if _client is None:
        _client = MongoClient(
            MONGODB_URI,
            maxPoolSize=50,
            minPoolSize=5,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=5000
        )
    return _client

def get_database(db_name: Optional[str] = None) -> Database:
    """Returns the MongoDB database instance."""
    client = get_client()
    return client[db_name or MONGODB_DB_NAME]

def get_db() -> Generator[Database, None, None]:
    """
    FastAPI dependency yielding the MongoDB database per request.
    Maintains clean dependency injection signature across all routers.
    """
    db = get_database()
    try:
        yield db
    finally:
        pass

def SessionLocal() -> Database:
    """Compatibility helper for direct database access."""
    return get_database()

def get_next_sequence(sequence_name: str, db: Optional[Database] = None) -> int:
    """
    Atomically increments and returns the next integer sequence ID.
    Maintains 100% backward-compatible integer IDs (e.g. user.id: 1, circuit.id: 2)
    for existing React frontend components.
    """
    if db is None:
        db = get_database()
    counter = db.counters.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER
    )
    return int(counter["seq"])

def init_db():
    """Initializes MongoDB indexes and seeds default learner and circuits if empty."""
    db = get_database()

    # 1. Ensure Indexes
    try:
        db.users.create_index([("username", ASCENDING)], unique=True)
        db.users.create_index([("id", ASCENDING)], unique=True)
        db.users.create_index([("email", ASCENDING)], unique=True, sparse=True)
        db.saved_circuits.create_index([("id", ASCENDING)], unique=True)
        db.saved_circuits.create_index([("user_id", ASCENDING)])
        db.learning_progress.create_index([("user_id", ASCENDING), ("lesson_id", ASCENDING)], unique=True)
        db.challenge_submissions.create_index([("user_id", ASCENDING), ("challenge_id", ASCENDING)])
        db.tutor_interactions.create_index([("user_id", ASCENDING)])
    except Exception as ex:
        print(f"Index creation notice: {ex}")

    # 2. Check or Seed Default Demo User (Quantum Explorer)
    default_user = db.users.find_one({"username": "quantum_explorer"})
    user_to_seed = None
    if not default_user:
        uid = get_next_sequence("user_id", db)
        now = datetime.now(timezone.utc)
        default_user = {
            "id": uid,
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
        db.users.insert_one(default_user)
        user_to_seed = default_user
        print(f"🌱 Seeded default user '{default_user['username']}' with id={uid}")
    elif not default_user.get("password_hash"):
        db.users.update_one(
            {"_id": default_user["_id"]},
            {"$set": {"password_hash": hash_password("quantum123")}}
        )
        user_to_seed = default_user
    else:
        user_to_seed = default_user

    # 3. Check or Seed Starter Circuits
    if user_to_seed:
        uid = user_to_seed["id"]
        circuit_count = db.saved_circuits.count_documents({"user_id": uid})
        if circuit_count == 0:
            now = datetime.now(timezone.utc)
            bell_id = get_next_sequence("circuit_id", db)
            grover_id = get_next_sequence("circuit_id", db)
            bell_circuit = {
                "id": bell_id,
                "user_id": uid,
                "name": "Bell State |Φ+⟩",
                "description": "Creates an entangled EPR pair using Hadamard and CNOT gates",
                "num_qubits": 2,
                "circuit_json": '{"qubits":2,"gates":[{"name":"H","target":0,"step":0},{"name":"CNOT","control":0,"target":1,"step":1}]}',
                "is_public": False,
                "created_at": now,
                "updated_at": now
            }
            grover_circuit = {
                "id": grover_id,
                "user_id": uid,
                "name": "2-Qubit Grover Search (|11⟩)",
                "description": "Searches for target state |11⟩ using an oracle and diffusion operator",
                "num_qubits": 2,
                "circuit_json": '{"qubits":2,"gates":[{"name":"H","target":0,"step":0},{"name":"H","target":1,"step":0},{"name":"CZ","control":0,"target":1,"step":1},{"name":"H","target":0,"step":2},{"name":"H","target":1,"step":2},{"name":"X","target":0,"step":3},{"name":"X","target":1,"step":3},{"name":"CZ","control":0,"target":1,"step":4},{"name":"X","target":0,"step":5},{"name":"X","target":1,"step":5},{"name":"H","target":0,"step":6},{"name":"H","target":1,"step":6}]}',
                "is_public": False,
                "created_at": now,
                "updated_at": now
            }
            db.saved_circuits.insert_many([bell_circuit, grover_circuit])
            print(f"🌱 Seeded starter circuits (Bell State & Grover Search) for user id={uid}")

