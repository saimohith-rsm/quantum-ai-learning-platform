from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from app.config import DATABASE_URL
from app.auth import hash_password

connect_args = {"check_same_thread": False} if "sqlite" in DATABASE_URL else {}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """FastAPI dependency to yield a database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initializes tables and seeds initial learner data if empty."""
    import app.models as models  # noqa: F401
    Base.metadata.create_all(bind=engine)

    # Lightweight migration for password_hash column if upgrading existing SQLite DB
    try:
        with engine.connect() as conn:
            res = conn.execute(text("PRAGMA table_info(users)")).fetchall()
            cols = [r[1] for r in res]
            if "password_hash" not in cols:
                conn.execute(text("ALTER TABLE users ADD COLUMN password_hash VARCHAR(256)"))
                conn.commit()
    except Exception as ex:
        print(f"Schema check note: {ex}")
    
    # Check if default user exists, else seed
    db = SessionLocal()
    try:
        default_user = db.query(models.User).filter_by(username="quantum_explorer").first()
        user_to_seed = None
        if not default_user:
            default_user = models.User(
                username="quantum_explorer",
                display_name="Quantum Explorer",
                email="explorer@quantum.learn",
                password_hash=hash_password("quantum123"),
                level="Beginner",
                xp=150,
                badges="Superposition Novice, Entanglement Spark"
            )
            db.add(default_user)
            db.commit()
            db.refresh(default_user)
            user_to_seed = default_user
        elif not default_user.password_hash:
            default_user.password_hash = hash_password("quantum123")
            db.commit()
            user_to_seed = default_user

        # Seed starter circuits if user has none
        if user_to_seed:
            existing_circuit = db.query(models.SavedCircuit).filter_by(user_id=user_to_seed.id).first()
            if not existing_circuit:
                bell_circuit = models.SavedCircuit(
                    user_id=user_to_seed.id,
                    name="Bell State |Φ+⟩",
                    description="Creates an entangled EPR pair using Hadamard and CNOT gates",
                    num_qubits=2,
                    circuit_json='{"qubits":2,"gates":[{"name":"H","target":0,"step":0},{"name":"CNOT","control":0,"target":1,"step":1}]}'
                )
                grover_circuit = models.SavedCircuit(
                    user_id=user_to_seed.id,
                    name="2-Qubit Grover Search (|11⟩)",
                    description="Searches for target state |11⟩ using an oracle and diffusion operator",
                    num_qubits=2,
                    circuit_json='{"qubits":2,"gates":[{"name":"H","target":0,"step":0},{"name":"H","target":1,"step":0},{"name":"CZ","control":0,"target":1,"step":1},{"name":"H","target":0,"step":2},{"name":"H","target":1,"step":2},{"name":"X","target":0,"step":3},{"name":"X","target":1,"step":3},{"name":"CZ","control":0,"target":1,"step":4},{"name":"X","target":0,"step":5},{"name":"X","target":1,"step":5},{"name":"H","target":0,"step":6},{"name":"H","target":1,"step":6}]}'
                )
                db.add(bell_circuit)
                db.add(grover_circuit)
                db.commit()
    except Exception as e:
        db.rollback()
        print(f"Warning during seed: {e}")
    finally:
        db.close()
