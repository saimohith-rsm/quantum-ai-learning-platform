from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

# ==================== Circuit & Simulation Schemas ====================

class GateSchema(BaseModel):
    name: str = Field(..., description="Gate name: H, X, Y, Z, S, T, Rx, Ry, Rz, CNOT, CZ, SWAP, Toffoli, Measure")
    target: int = Field(..., description="Target qubit index (0-indexed)")
    control: Optional[int] = Field(None, description="Primary control qubit index for 2/3-qubit gates")
    control2: Optional[int] = Field(None, description="Secondary control qubit index for 3-qubit gates (Toffoli)")
    step: int = Field(0, description="Time step column in circuit timeline")
    params: Optional[Dict[str, float]] = Field(default_factory=dict, description="Parameters like theta for rotation gates")

class CircuitSchema(BaseModel):
    qubits: int = Field(2, ge=1, le=8, description="Number of qubits (1 to 8)")
    gates: List[GateSchema] = Field(default_factory=list, description="List of gates in the circuit")

class SimulationRequest(BaseModel):
    circuit: CircuitSchema
    shots: int = Field(1024, ge=1, le=100000, description="Number of measurement shots")
    calculate_steps: bool = Field(True, description="Whether to return step-by-step state evolution")

class StatevectorEntry(BaseModel):
    index: int
    label: str
    real: float
    imag: float
    magnitude: float
    probability: float
    phase_rad: float
    phase_deg: float

class BlochVector(BaseModel):
    qubit: int
    x: float
    y: float
    z: float
    purity: float
    theta_rad: float
    phi_rad: float

class SimulationStep(BaseModel):
    step_index: int
    gate_applied: Optional[str]
    target_qubit: Optional[int]
    control_qubit: Optional[int]
    probabilities: Dict[str, float]
    bloch_vectors: List[BlochVector]
    statevector: List[StatevectorEntry]

class SimulationResponse(BaseModel):
    num_qubits: int
    statevector: List[StatevectorEntry]
    probabilities: Dict[str, float]
    shot_counts: Dict[str, int]
    bloch_vectors: List[BlochVector]
    steps: List[SimulationStep]
    qiskit_code: str
    qasm_code: str
    execution_time_ms: float

# ==================== AI Tutor Schemas ====================

class TutorExplainRequest(BaseModel):
    circuit: CircuitSchema
    user_level: str = "Beginner"  # Beginner, Intermediate, Advanced

class TutorDebugRequest(BaseModel):
    circuit: CircuitSchema
    goal: str = Field(..., description="Target algorithm or expected outcome")
    user_level: str = "Beginner"

class TutorHintRequest(BaseModel):
    challenge_id: str
    circuit: CircuitSchema
    tier: int = Field(1, ge=1, le=3, description="1=Intuition Nudge, 2=Mathematical Hint, 3=Direct Circuit Suggestion")

class TutorChatRequest(BaseModel):
    message: str
    circuit: Optional[CircuitSchema] = None
    user_level: str = "Beginner"
    provider: Optional[str] = Field("auto", description="LLM provider: gemini, openai, or auto")
    socratic_mode: bool = Field(False, description="Whether to guide the user with Socratic questions rather than direct answers")

class TutorResponse(BaseModel):
    title: str
    explanation: str
    key_insights: List[str] = Field(default_factory=list)
    suggested_actions: List[str] = Field(default_factory=list)
    quantum_math: Optional[str] = None
    source: str = "ai_engine"

# ==================== Challenge Schemas ====================

class ChallengeSubmissionRequest(BaseModel):
    challenge_id: str
    circuit: CircuitSchema
    user_id: Optional[int] = 1

class ChallengeSubmissionResponse(BaseModel):
    challenge_id: str
    passed: bool
    fidelity: float
    score: int
    feedback: str
    details: Dict[str, Any]

# ==================== Auth Schemas ====================

class UserRegister(BaseModel):
    username: str
    password: str
    email: Optional[str] = None
    display_name: Optional[str] = None

class UserLogin(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    token: str
    user: "UserResponse"

# ==================== Database CRUD Schemas ====================

class UserCreate(BaseModel):
    username: str
    display_name: Optional[str] = "Learner"
    email: Optional[str] = None
    level: Optional[str] = "Beginner"

class UserResponse(BaseModel):
    id: int
    username: str
    display_name: str
    email: Optional[str]
    level: str
    xp: int
    badges: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class SavedCircuitCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    num_qubits: int
    circuit_json: str
    is_public: Optional[bool] = False

class SavedCircuitResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: str
    num_qubits: int
    circuit_json: str
    is_public: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProgressUpdate(BaseModel):
    user_id: int
    module_id: str
    lesson_id: str
    completed: bool
    quiz_score: Optional[float] = 100.0

# ==================== Advanced SIH 2026 Schemas ====================

class CircuitOptimizeRequest(BaseModel):
    circuit: CircuitSchema

class CircuitOptimizeResponse(BaseModel):
    original_circuit: Dict[str, Any]
    optimized_circuit: Dict[str, Any]
    metrics: Dict[str, Any]
    optimizations_applied: List[str]

class NoisySimulationRequest(BaseModel):
    circuit: CircuitSchema
    hardware_preset: Optional[str] = Field("ibm_eagle", description="ibm_eagle, ionq_aria, high_decoherence, or custom")
    t1_prob: Optional[float] = None
    t2_prob: Optional[float] = None
    gate_error: Optional[float] = None
    cnot_error: Optional[float] = None
    readout_error: Optional[float] = None
    shots: int = Field(1024, ge=100, le=10000)
    trajectories: int = Field(120, ge=20, le=300)

class NoisySimulationResponse(BaseModel):
    hardware_model: str
    fidelity: float
    quantum_error_rate: float
    ideal_probabilities: Dict[str, float]
    noisy_probabilities: Dict[str, float]
    noisy_counts: Dict[str, int]
    noise_parameters: Dict[str, float]
    interpretation: str

class MultiSdkExportRequest(BaseModel):
    circuit: CircuitSchema

class MultiSdkExportResponse(BaseModel):
    qiskit: str
    cirq: str
    pennylane: str
    braket: str
    qasm: str

class BB84Request(BaseModel):
    num_bits: int = Field(24, ge=8, le=64, description="Number of photons transmitted")
    eve_present: bool = Field(False, description="Whether eavesdropper intercepts photons")
    eve_intercept_rate: float = Field(1.0, ge=0.0, le=1.0, description="Percentage of photons intercepted by Eve")

