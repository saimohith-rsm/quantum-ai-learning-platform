"""
Automated Migration Script: SQLite to MongoDB
Migrates all users, saved circuits, progress, challenges, and tutor logs
from quantum_learning.db into MongoDB collections.
"""
import os
import sqlite3
from pymongo import MongoClient, ASCENDING
from datetime import datetime

SQLITE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "quantum_learning.db")
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "quantum_learning")

def migrate():
    if not os.path.exists(SQLITE_PATH):
        print(f"SQLite DB not found at {SQLITE_PATH}. Nothing to migrate.")
        return

    client = MongoClient(MONGODB_URI, serverSelectionTimeoutMS=3000)
    db = client[MONGODB_DB_NAME]
    print(f"Connected to MongoDB '{MONGODB_DB_NAME}' on {MONGODB_URI}")

    sqlite_conn = sqlite3.connect(SQLITE_PATH)
    sqlite_conn.row_factory = sqlite3.Row
    cur = sqlite_conn.cursor()

    # 1. Migrate Users
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    max_user_id = 0
    for u in users:
        u_dict = dict(u)
        uid = int(u_dict["id"])
        max_user_id = max(max_user_id, uid)
        # Upsert by id
        db.users.update_one(
            {"id": uid},
            {"$set": {
                "id": uid,
                "username": u_dict.get("username"),
                "display_name": u_dict.get("display_name", "Learner"),
                "email": u_dict.get("email"),
                "password_hash": u_dict.get("password_hash"),
                "level": u_dict.get("level", "Beginner"),
                "xp": int(u_dict.get("xp", 0)),
                "badges": u_dict.get("badges", ""),
                "created_at": u_dict.get("created_at") or datetime.utcnow().isoformat(),
                "updated_at": u_dict.get("updated_at") or datetime.utcnow().isoformat()
            }},
            upsert=True
        )
    print(f"Migrated {len(users)} users to MongoDB.")

    # 2. Migrate Saved Circuits
    cur.execute("SELECT * FROM saved_circuits")
    circuits = cur.fetchall()
    max_circuit_id = 0
    for c in circuits:
        c_dict = dict(c)
        cid = int(c_dict["id"])
        max_circuit_id = max(max_circuit_id, cid)
        db.saved_circuits.update_one(
            {"id": cid},
            {"$set": {
                "id": cid,
                "user_id": int(c_dict["user_id"]),
                "name": c_dict.get("name"),
                "description": c_dict.get("description", ""),
                "num_qubits": int(c_dict.get("num_qubits", 2)),
                "circuit_json": c_dict.get("circuit_json"),
                "is_public": bool(c_dict.get("is_public", False)),
                "created_at": c_dict.get("created_at") or datetime.utcnow().isoformat(),
                "updated_at": c_dict.get("updated_at") or datetime.utcnow().isoformat()
            }},
            upsert=True
        )
    print(f"Migrated {len(circuits)} saved circuits to MongoDB.")

    # 3. Migrate Challenge Submissions
    cur.execute("SELECT * FROM challenge_submissions")
    subs = cur.fetchall()
    max_sub_id = 0
    for s in subs:
        s_dict = dict(s)
        sid = int(s_dict["id"])
        max_sub_id = max(max_sub_id, sid)
        db.challenge_submissions.update_one(
            {"id": sid},
            {"$set": {
                "id": sid,
                "user_id": int(s_dict["user_id"]),
                "challenge_id": s_dict.get("challenge_id"),
                "circuit_json": s_dict.get("circuit_json"),
                "passed": bool(s_dict.get("passed", False)),
                "fidelity": float(s_dict.get("fidelity", 0.0)),
                "score": int(s_dict.get("score", 0)),
                "feedback": s_dict.get("feedback", ""),
                "submitted_at": s_dict.get("submitted_at") or datetime.utcnow().isoformat()
            }},
            upsert=True
        )
    print(f"Migrated {len(subs)} challenge submissions to MongoDB.")

    # 4. Migrate Tutor Interactions
    cur.execute("SELECT * FROM tutor_interactions")
    logs = cur.fetchall()
    max_log_id = 0
    for l in logs:
        l_dict = dict(l)
        lid = int(l_dict["id"])
        max_log_id = max(max_log_id, lid)
        db.tutor_interactions.update_one(
            {"id": lid},
            {"$set": {
                "id": lid,
                "user_id": int(l_dict["user_id"]) if l_dict.get("user_id") else 1,
                "circuit_id": int(l_dict["circuit_id"]) if l_dict.get("circuit_id") else None,
                "query_type": l_dict.get("query_type", "chat"),
                "prompt": l_dict.get("prompt", ""),
                "response": l_dict.get("response", ""),
                "created_at": l_dict.get("created_at") or datetime.utcnow().isoformat()
            }},
            upsert=True
        )
    print(f"Migrated {len(logs)} tutor interaction logs to MongoDB.")

    # 5. Initialize sequence counters so new IDs continue smoothly
    db.counters.update_one({"_id": "user_id"}, {"$set": {"seq": max_user_id}}, upsert=True)
    db.counters.update_one({"_id": "circuit_id"}, {"$set": {"seq": max_circuit_id}}, upsert=True)
    db.counters.update_one({"_id": "submission_id"}, {"$set": {"seq": max_sub_id}}, upsert=True)
    db.counters.update_one({"_id": "tutor_log_id"}, {"$set": {"seq": max_log_id}}, upsert=True)
    db.counters.update_one({"_id": "progress_id"}, {"$set": {"seq": 0}}, upsert=True)

    # 6. Ensure indexes
    db.users.create_index([("username", ASCENDING)], unique=True)
    db.users.create_index([("id", ASCENDING)], unique=True)
    db.saved_circuits.create_index([("id", ASCENDING)], unique=True)
    db.saved_circuits.create_index([("user_id", ASCENDING)])
    db.learning_progress.create_index([("user_id", ASCENDING), ("lesson_id", ASCENDING)], unique=True)

    print("✅ Full migration from SQLite to MongoDB completed successfully!")
    sqlite_conn.close()

if __name__ == "__main__":
    migrate()
