from typing import List, Dict, Any

CHALLENGES: List[Dict[str, Any]] = [
    {
        "id": "bell_plus",
        "title": "Challenge 1: Create Bell State |Φ+⟩",
        "category": "Entanglement",
        "difficulty": "Beginner",
        "xp": 100,
        "badge": "Entanglement Pioneer",
        "num_qubits": 2,
        "max_gates": 4,
        "description": "Construct a 2-qubit circuit that produces the maximally entangled EPR Bell state |Φ+⟩ = (|00⟩ + |11⟩)/√2.",
        "instructions": [
            "Use Qubit 0 and Qubit 1.",
            "Apply a Hadamard gate to Qubit 0 to create equal superposition.",
            "Apply a CNOT gate with Control on Qubit 0 and Target on Qubit 1.",
            "Target distribution: 50% |00⟩ and 50% |11⟩."
        ],
        "hints": [
            "You need one single-qubit gate and one two-qubit gate.",
            "Remember: Hadamard creates superposition; CNOT entangles.",
            "Place H on Qubit 0 at Step 0, then CNOT(0 -> 1) at Step 1."
        ],
        "verification": {
            "type": "probabilities",
            "target": {"00": 0.5, "11": 0.5},
            "tolerance": 0.05
        }
    },
    {
        "id": "superposition_pair",
        "title": "Challenge 2: 2-Qubit Uniform Superposition",
        "category": "Foundations",
        "difficulty": "Beginner",
        "xp": 80,
        "badge": "Superposition Adept",
        "num_qubits": 2,
        "max_gates": 4,
        "description": "Prepare both qubits in uniform superposition |++⟩, resulting in equal 25% probability across all four basis states.",
        "instructions": [
            "Apply Hadamard gates to both Qubit 0 and Qubit 1.",
            "Ensure no entangling gates are used.",
            "Target distribution: 25% for |00⟩, |01⟩, |10⟩, and |11⟩."
        ],
        "hints": [
            "Think about how single-qubit Hadamards act in parallel.",
            "H|0⟩ gives (|0⟩+|1⟩)/√2. What happens if you apply H to both wires?",
            "Add an H gate on Qubit 0 and another H gate on Qubit 1."
        ],
        "verification": {
            "type": "probabilities",
            "target": {"00": 0.25, "01": 0.25, "10": 0.25, "11": 0.25},
            "tolerance": 0.05
        }
    },
    {
        "id": "ghz_state",
        "title": "Challenge 3: 3-Qubit GHZ State",
        "category": "Entanglement",
        "difficulty": "Intermediate",
        "xp": 150,
        "badge": "GHZ Architect",
        "num_qubits": 3,
        "max_gates": 5,
        "description": "Construct the famous 3-qubit Greenberger–Horne–Zeilinger (GHZ) state: |GHZ⟩ = (|000⟩ + |111⟩)/√2.",
        "instructions": [
            "Initialize on 3 qubits.",
            "Create superposition on Qubit 0.",
            "Cascade CNOT gates to entangle Qubit 1 and Qubit 2.",
            "Target distribution: 50% |000⟩ and 50% |111⟩."
        ],
        "hints": [
            "Extend the 2-qubit Bell state idea to 3 qubits.",
            "First do H on Q0, then CNOT(0->1). Now how do you bring Q2 in?",
            "Add CNOT(1->2) or CNOT(0->2) to complete the entanglement chain."
        ],
        "verification": {
            "type": "probabilities",
            "target": {"000": 0.5, "111": 0.5},
            "tolerance": 0.05
        }
    },
    {
        "id": "grover_search",
        "title": "Challenge 4: 2-Qubit Grover Search for |11⟩",
        "category": "Algorithms",
        "difficulty": "Advanced",
        "xp": 200,
        "badge": "Quantum Speedup Master",
        "num_qubits": 2,
        "max_gates": 14,
        "description": "Build a complete Grover search algorithm that amplifies target state |11⟩ to 100% probability using an oracle and diffusion operator.",
        "instructions": [
            "1. Initialize both qubits with Hadamard gates.",
            "2. Apply the phase oracle for |11⟩ (a CZ gate).",
            "3. Apply the diffusion operator: H on both -> X on both -> CZ -> X on both -> H on both.",
            "Target distribution: 100% |11⟩."
        ],
        "hints": [
            "Follow the 3 distinct phases: Superposition, Oracle, Diffusion.",
            "The diffusion operator formula in 2 qubits is H -> X -> CZ -> X -> H on both qubits.",
            "Verify that both qubits have H, then CZ(0->1), then H on both, X on both, CZ(0->1), X on both, H on both."
        ],
        "verification": {
            "type": "probabilities",
            "target": {"11": 1.0},
            "tolerance": 0.05
        }
    }
]

def get_all_challenges() -> List[Dict[str, Any]]:
    return CHALLENGES

def get_challenge_by_id(challenge_id: str) -> Dict[str, Any]:
    for c in CHALLENGES:
        if c["id"] == challenge_id:
            return c
    return None
