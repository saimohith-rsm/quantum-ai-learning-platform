import numpy as np
from typing import List, Dict, Any

PRESET_ALGORITHMS: List[Dict[str, Any]] = [
    {
        "id": "bell_phi_plus",
        "name": "Bell State |Φ+⟩ (Entanglement)",
        "category": "Entanglement",
        "difficulty": "Beginner",
        "description": "The quintessential maximally entangled 2-qubit EPR pair. Measuring one qubit instantaneously determines the state of the second qubit.",
        "qubits": 2,
        "gates": [
            {"name": "H", "target": 0, "step": 0},
            {"name": "CNOT", "control": 0, "target": 1, "step": 1}
        ],
        "expected_state": "|Φ+⟩ = (|00⟩ + |11⟩) / √2",
        "key_concept": "Hadamard creates superposition on q0, then CNOT entangles q1 conditionally on q0 being |1⟩."
    },
    {
        "id": "bell_psi_minus",
        "name": "Bell State |Ψ-⟩ (Singlet State)",
        "category": "Entanglement",
        "difficulty": "Beginner",
        "description": "Antisymmetric entangled singlet state |Ψ-⟩ = (|01⟩ - |10⟩) / √2, fundamental in spin physics and quantum cryptography.",
        "qubits": 2,
        "gates": [
            {"name": "X", "target": 0, "step": 0},
            {"name": "X", "target": 1, "step": 0},
            {"name": "H", "target": 0, "step": 1},
            {"name": "CNOT", "control": 0, "target": 1, "step": 2}
        ],
        "expected_state": "|Ψ-⟩ = (|01⟩ - |10⟩) / √2",
        "key_concept": "Starts from |11⟩, applies Hadamard and CNOT to yield the negative parity Bell state."
    },
    {
        "id": "grover_2qubit",
        "name": "Grover's Search (2-Qubit Target |11⟩)",
        "category": "Search",
        "difficulty": "Intermediate",
        "description": "Finds a marked item in an unsorted database of 4 items in a single query (vs classical 2.25 average queries), achieving quadratic quantum speedup.",
        "qubits": 2,
        "gates": [
            # 1. State Preparation (Equal Superposition)
            {"name": "H", "target": 0, "step": 0},
            {"name": "H", "target": 1, "step": 0},
            # 2. Oracle (flips phase of |11⟩)
            {"name": "CZ", "control": 0, "target": 1, "step": 1},
            # 3. Diffusion Operator (Inversion about the mean: H -> X -> CZ -> X -> H)
            {"name": "H", "target": 0, "step": 2},
            {"name": "H", "target": 1, "step": 2},
            {"name": "X", "target": 0, "step": 3},
            {"name": "X", "target": 1, "step": 3},
            {"name": "CZ", "control": 0, "target": 1, "step": 4},
            {"name": "X", "target": 0, "step": 5},
            {"name": "X", "target": 1, "step": 5},
            {"name": "H", "target": 0, "step": 6},
            {"name": "H", "target": 1, "step": 6}
        ],
        "expected_state": "100% Probability of |11⟩",
        "key_concept": "Oracle marks the target with a negative phase (-1), and the diffusion operator amplifies its amplitude while suppressing unwanted states."
    },
    {
        "id": "deutsch_jozsa",
        "name": "Deutsch-Jozsa (Balanced Oracle)",
        "category": "Oracles",
        "difficulty": "Intermediate",
        "description": "Determines whether an unknown black-box function f(x) is constant (all 0s or all 1s) or balanced (half 0s, half 1s) in exactly 1 quantum evaluation.",
        "qubits": 2,
        "gates": [
            # Prepare ancilla qubit q1 in |1⟩
            {"name": "X", "target": 1, "step": 0},
            # Put both qubits into superposition (q1 becomes |−⟩ for phase kickback)
            {"name": "H", "target": 0, "step": 1},
            {"name": "H", "target": 1, "step": 1},
            # Balanced Oracle: f(x) = x implemented via CNOT
            {"name": "CNOT", "control": 0, "target": 1, "step": 2},
            # Interference on input register
            {"name": "H", "target": 0, "step": 3}
        ],
        "expected_state": "Measuring q0 yields |1⟩ (Balanced) with 100% certainty",
        "key_concept": "Phase kickback from the ancilla |−⟩ state flips the phase of input states where f(x)=1, leading to destructive interference on |0⟩."
    },
    {
        "id": "quantum_teleportation",
        "name": "Quantum Teleportation Protocol",
        "category": "Protocols",
        "difficulty": "Advanced",
        "description": "Transfers an arbitrary unknown quantum state |ψ⟩ from Alice (q0) to Bob (q2) using shared entanglement (q1, q2) and 2 classical bits of information.",
        "qubits": 3,
        "gates": [
            # Prepare state to teleport on q0: rotate by pi/3
            {"name": "RY", "target": 0, "step": 0, "params": {"theta": 1.0472}},
            # Create Bell pair between q1 and q2
            {"name": "H", "target": 1, "step": 1},
            {"name": "CNOT", "control": 1, "target": 2, "step": 2},
            # Alice performs Bell measurement on q0 and q1
            {"name": "CNOT", "control": 0, "target": 1, "step": 3},
            {"name": "H", "target": 0, "step": 4},
            # Bob applies conditional correction based on Alice's qubits
            {"name": "CNOT", "control": 1, "target": 2, "step": 5},
            {"name": "CZ", "control": 0, "target": 2, "step": 6}
        ],
        "expected_state": "Bob's qubit (q2) reconstructs Alice's original state |ψ⟩ with unit fidelity.",
        "key_concept": "Entanglement enables non-local quantum state reconstruction without violating the no-cloning theorem."
    },
    {
        "id": "superdense_coding",
        "name": "Superdense Coding (Transmitting '11')",
        "category": "Protocols",
        "difficulty": "Intermediate",
        "description": "Allows Alice to send 2 classical bits of information to Bob by transmitting only 1 entangled qubit.",
        "qubits": 2,
        "gates": [
            # Shared EPR pair
            {"name": "H", "target": 0, "step": 0},
            {"name": "CNOT", "control": 0, "target": 1, "step": 1},
            # Alice encodes classical '11' using Z and X gates on q0
            {"name": "Z", "target": 0, "step": 2},
            {"name": "X", "target": 0, "step": 3},
            # Bob receives q0 and decodes with CNOT and H
            {"name": "CNOT", "control": 0, "target": 1, "step": 4},
            {"name": "H", "target": 0, "step": 5}
        ],
        "expected_state": "Measuring both qubits yields '11' with 100% probability",
        "key_concept": "Prior entanglement doubles the classical channel capacity of a single transmitted qubit."
    },
    {
        "id": "qft_3qubit",
        "name": "3-Qubit Quantum Fourier Transform (QFT)",
        "category": "Transformations",
        "difficulty": "Advanced",
        "description": "Quantum version of the discrete Fourier transform. Crucial core subroutine in Shor's factoring algorithm and Quantum Phase Estimation (QPE).",
        "qubits": 3,
        "gates": [
            # Qubit 0
            {"name": "H", "target": 0, "step": 0},
            {"name": "CPHASE", "control": 1, "target": 0, "step": 1, "params": {"phi": 1.5708}},   # pi/2
            {"name": "CPHASE", "control": 2, "target": 0, "step": 2, "params": {"phi": 0.7854}},   # pi/4
            # Qubit 1
            {"name": "H", "target": 1, "step": 3},
            {"name": "CPHASE", "control": 2, "target": 1, "step": 4, "params": {"phi": 1.5708}},   # pi/2
            # Qubit 2
            {"name": "H", "target": 2, "step": 5},
            # Final Bit-Reversal SWAP
            {"name": "SWAP", "control": 0, "target": 2, "step": 6}
        ],
        "expected_state": "Maps computational basis states to Fourier basis phase states",
        "key_concept": "Executes discrete Fourier transform in O(n^2) quantum operations instead of classical O(n 2^n) FFT."
    },
    {
        "id": "qrng_3qubit",
        "name": "Quantum Random Number Generator (QRNG)",
        "category": "Foundations",
        "difficulty": "Beginner",
        "description": "Generates truly non-deterministic random integers from 0 to 7 based on fundamental quantum indeterminacy.",
        "qubits": 3,
        "gates": [
            {"name": "H", "target": 0, "step": 0},
            {"name": "H", "target": 1, "step": 0},
            {"name": "H", "target": 2, "step": 0}
        ],
        "expected_state": "Equal 12.5% (1/8) probability across all 8 basis states |000⟩ through |111⟩",
        "key_concept": "Unlike pseudo-random classical algorithms, quantum measurement yields intrinsic physical randomness."
    }
]

def get_preset_by_id(preset_id: str) -> Dict[str, Any]:
    for p in PRESET_ALGORITHMS:
        if p["id"] == preset_id:
            return p
    return None
