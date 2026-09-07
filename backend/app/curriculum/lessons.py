from typing import List, Dict, Any

CURRICULUM_MODULES: List[Dict[str, Any]] = [
    {
        "id": "module_1",
        "title": "Module 1: Foundations of Quantum Information",
        "description": "Master qubits, quantum superposition, the 3D Bloch Sphere, and essential single-qubit gates.",
        "difficulty": "Beginner",
        "lessons": [
            {
                "id": "lesson_1_1",
                "title": "1.1 Classical Bits vs Quantum Qubits",
                "estimated_minutes": 10,
                "summary": "Understand the fundamental difference between classical binary states {0, 1} and quantum linear superpositions.",
                "content": """
# Classical Bits vs Quantum Qubits

In classical computing, the fundamental unit of information is a **bit**, which exists strictly as either a `0` or a `1`. 

A **qubit** (quantum bit), however, exploits the quantum mechanical property of **superposition**. A qubit can exist in a linear combination of basis states:

$$|\\psi\\rangle = \\alpha|0\\rangle + \\beta|1\\rangle$$

where $\\alpha, \\beta \\in \\mathbb{C}$ are complex probability amplitudes satisfying:

$$|\\alpha|^2 + |\\beta|^2 = 1$$

When measured, the qubit probabilistically collapses to:
- State $|0\\rangle$ with probability $P(0) = |\\alpha|^2$
- State $|1\\rangle$ with probability $P(1) = |\\beta|^2$
                """,
                "starter_circuit": {
                    "qubits": 1,
                    "gates": []
                },
                "quiz": {
                    "question": "If a qubit is in state |ψ⟩ = (1/√2)|0⟩ + (1/√2)|1⟩, what is the probability of measuring |1⟩?",
                    "options": ["25%", "50%", "75%", "100%"],
                    "correct_index": 1,
                    "explanation": "P(1) = |β|² = (1/√2)² = 1/2 = 50%."
                }
            },
            {
                "id": "lesson_1_2",
                "title": "1.2 The Hadamard Gate & The Bloch Sphere",
                "estimated_minutes": 15,
                "summary": "Visualize single-qubit rotations in 3D on the Bloch sphere and discover how Hadamard creates equal superposition.",
                "content": """
# The Hadamard Gate & The Bloch Sphere

The **Bloch Sphere** is a 3D unit sphere representation of a two-level quantum state:

$$|\\psi\\rangle = \\cos\\left(\\frac{\\theta}{2}\\right)|0\\rangle + e^{i\\phi}\\sin\\left(\\frac{\\theta}{2}\\right)|1\\rangle$$

- The **North Pole** ($\theta = 0$) corresponds to $|0\\rangle$.
- The **South Pole** ($\theta = \\pi$) corresponds to $|1\\rangle$.
- Points on the equator correspond to equal superpositions ($|\\alpha| = |\\beta| = 1/\\sqrt{2}$) with varying relative phases $\\phi$.

### The Hadamard Gate (H)
The Hadamard gate transforms the computational basis into the diagonal superposition basis:

$$H|0\\rangle = \\frac{|0\\rangle + |1\\rangle}{\\sqrt{2}} = |+\\rangle$$
$$H|1\\rangle = \\frac{|0\\rangle - |1\\rangle}{\\sqrt{2}} = |-\\rangle$$
                """,
                "starter_circuit": {
                    "qubits": 1,
                    "gates": [{"name": "H", "target": 0, "step": 0}]
                },
                "quiz": {
                    "question": "Where does state |+⟩ lie on the Bloch sphere?",
                    "options": ["At the North Pole (z=+1)", "At the South Pole (z=-1)", "On the Equator along the positive X-axis (x=+1)", "At the center of the sphere"],
                    "correct_index": 2,
                    "explanation": "|+⟩ has θ=π/2 and φ=0, placing the Bloch vector at (1, 0, 0) on the positive X-axis."
                }
            }
        ]
    },
    {
        "id": "module_2",
        "title": "Module 2: Multi-Qubit Systems & Entanglement",
        "description": "Explore tensor products, 2-qubit gates, Bell states, quantum teleportation, and superdense coding.",
        "difficulty": "Intermediate",
        "lessons": [
            {
                "id": "lesson_2_1",
                "title": "2.1 The CNOT Gate & Bell States",
                "estimated_minutes": 15,
                "summary": "Build the four maximally entangled Bell states using Hadamard and Controlled-NOT gates.",
                "content": """
# The CNOT Gate & Bell States

When multiple qubits are combined, their composite state space is given by the tensor product $\\mathcal{H}_1 \\otimes \\mathcal{H}_2$.

The **CNOT (Controlled-NOT)** gate performs a conditional bit-flip on the target qubit if and only if the control qubit is $|1\\rangle$:

$$\\text{CNOT}|00\\rangle = |00\\rangle, \\quad \\text{CNOT}|01\\rangle = |01\\rangle$$
$$\\text{CNOT}|10\\rangle = |11\\rangle, \\quad \\text{CNOT}|11\\rangle = |10\\rangle$$

### Creating Bell State $|\\Phi^+\\rangle$
By applying a Hadamard to Qubit 0 followed by a CNOT from Qubit 0 to Qubit 1:

$$|00\\rangle \\xrightarrow{H_0} \\frac{|00\\rangle + |10\\rangle}{\\sqrt{2}} \\xrightarrow{\\text{CNOT}_{0\\to 1}} \\frac{|00\\rangle + |11\\rangle}{\\sqrt{2}} = |\\Phi^+\\rangle$$

This state is **maximally entangled**; it cannot be written as $|\\psi_A\\rangle \\otimes |\\psi_B\\rangle$.
                """,
                "starter_circuit": {
                    "qubits": 2,
                    "gates": [
                        {"name": "H", "target": 0, "step": 0},
                        {"name": "CNOT", "control": 0, "target": 1, "step": 1}
                    ]
                },
                "quiz": {
                    "question": "If Alice measures her qubit in state |Φ+⟩ and observes |0⟩, what state will Bob measure on his qubit?",
                    "options": ["Always |0⟩ with 100% certainty", "Always |1⟩ with 100% certainty", "50% chance of |0⟩, 50% chance of |1⟩", "A completely random state"],
                    "correct_index": 0,
                    "explanation": "Because |Φ+⟩ = (|00⟩ + |11⟩)/√2 has only |00⟩ and |11⟩ terms, observing 0 on one qubit instantly projects the pair into |00⟩."
                }
            }
        ]
    },
    {
        "id": "module_3",
        "title": "Module 3: Landmark Quantum Algorithms",
        "description": "Understand how quantum interference and phase kickback unlock exponential and quadratic speedups.",
        "difficulty": "Advanced",
        "lessons": [
            {
                "id": "lesson_3_1",
                "title": "3.1 Deutsch-Jozsa Algorithm",
                "estimated_minutes": 20,
                "summary": "Discover how quantum parallelism and interference evaluate global function properties in a single evaluation.",
                "content": """
# Deutsch-Jozsa Algorithm

Given a black-box oracle function $f: \\{0,1\\}^n \\to \\{0,1\\}$ that is guaranteed to be either **constant** (same output for all inputs) or **balanced** (output 0 for half of inputs, 1 for the other half):

- **Classical computers** require $2^{n-1} + 1$ evaluations in the worst case to be certain.
- **Quantum computers** solve this in **exactly 1 evaluation**!

### Key Mechanism: Phase Kickback
By setting the ancilla qubit in the state $|-\\rangle = \\frac{|0\\rangle - |1\\rangle}{\\sqrt{2}}$, the oracle evaluates:

$$U_f |x\\rangle |-\\rangle = (-1)^{f(x)} |x\\rangle |-\\rangle$$

When we apply Hadamard gates before measuring the input register, constructive interference directs the amplitude to $|0\\dots0\\rangle$ if and only if $f$ is constant. If $f$ is balanced, it destructively interferes to zero on $|0\\dots0\\rangle$!
                """,
                "starter_circuit": {
                    "qubits": 2,
                    "gates": [
                        {"name": "X", "target": 1, "step": 0},
                        {"name": "H", "target": 0, "step": 1},
                        {"name": "H", "target": 1, "step": 1},
                        {"name": "CNOT", "control": 0, "target": 1, "step": 2},
                        {"name": "H", "target": 0, "step": 3}
                    ]
                },
                "quiz": {
                    "question": "What does a measurement result of |0⟩ on the input register indicate in Deutsch-Jozsa?",
                    "options": ["The function is balanced", "The function is constant", "The oracle failed", "The result is inconclusive"],
                    "correct_index": 1,
                    "explanation": "If all input qubits measure |0⟩, the function f is constant. Any other measurement proves f is balanced."
                }
            },
            {
                "id": "lesson_3_2",
                "title": "3.2 Grover's Search Algorithm",
                "estimated_minutes": 25,
                "summary": "Master unstructured database search with quadratic speedup using amplitude amplification.",
                "content": r"""
# Grover's Search Algorithm

Searching for a specific item in an unsorted database of $N = 2^n$ items classically requires $O(N)$ operations on average. Grover's algorithm finds the target in $O(\sqrt{N})$ queries.

### The Two Operators:
1. **Oracle ($O$)**: Inverts the phase of the marked target state $|\omega\rangle$:
   $$O|x\rangle = \begin{cases} -|x\rangle & \text{if } x = \omega \\ |x\rangle & \text{if } x \neq \omega \end{cases}$$

2. **Diffusion Operator ($D$)**: Inversion about the mean amplitude:
   $$D = 2|s\rangle\langle s| - I$$
   where $|s\rangle = H^{\otimes n}|0\rangle$ is the equal superposition state.

Applying the Grover iteration $G = D \cdot O$ boosts the target amplitude while suppressing all other states through destructive interference.
                """,
                "starter_circuit": {
                    "qubits": 2,
                    "gates": [
                        {"name": "H", "target": 0, "step": 0},
                        {"name": "H", "target": 1, "step": 0},
                        {"name": "CZ", "control": 0, "target": 1, "step": 1},
                        {"name": "H", "target": 0, "step": 2},
                        {"name": "H", "target": 1, "step": 2},
                        {"name": "X", "target": 0, "step": 3},
                        {"name": "X", "target": 1, "step": 3},
                        {"name": "CZ", "control": 0, "target": 1, "step": 4},
                        {"name": "X", "target": 0, "step": 5},
                        {"name": "X", "target": 1, "step": 5},
                        {"name": "H", "target": 0, "step": 6},
                        {"name": "H", "target": 1, "step": 6}
                    ]
                },
                "quiz": {
                    "question": "How many queries does 2-qubit Grover's search require to find the target item out of 4 possibilities?",
                    "options": ["1 query", "2 queries", "3 queries", "4 queries"],
                    "correct_index": 0,
                    "explanation": "For N=4 (2 qubits), Grover's search finds the marked item with 100% theoretical probability in exactly 1 iteration!"
                }
            }
        ]
    }
]

def get_all_modules() -> List[Dict[str, Any]]:
    return CURRICULUM_MODULES

def get_lesson_by_id(lesson_id: str) -> Dict[str, Any]:
    for mod in CURRICULUM_MODULES:
        for l in mod["lessons"]:
            if l["id"] == lesson_id:
                return l
    return None
