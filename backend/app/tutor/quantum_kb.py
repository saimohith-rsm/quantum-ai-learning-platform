from typing import Dict, Any, List

QUANTUM_CONCEPTS_KB = {
    "qubit": {
        "title": "What is a Qubit?",
        "summary": "A qubit (quantum bit) is the basic unit of quantum information. Unlike a classical bit that is strictly 0 or 1, a qubit exists in a linear superposition |ψ⟩ = α|0⟩ + β|1⟩, where α and β are complex probability amplitudes with |α|² + |β|² = 1.",
        "math": "|ψ⟩ = cos(θ/2)|0⟩ + e^{iφ}sin(θ/2)|1⟩",
        "analogy": "A classical bit is like a coin lying flat showing either Heads or Tails. A qubit is like a coin spinning in mid-air—it contains probabilities of both until it lands (measurement)."
    },
    "bloch_sphere": {
        "title": "The Bloch Sphere",
        "summary": "A geometrical representation of a single qubit state as a point on the surface of a unit sphere. The North pole corresponds to |0⟩, the South pole to |1⟩, and the equator represents equal superpositions with varying relative phases.",
        "math": "r⃗ = (sin θ cos φ, sin θ sin φ, cos θ)",
        "analogy": "Think of Earth: the North Pole is |0⟩, South Pole is |1⟩. The Equator holds states like |+⟩ and |−⟩. Any single-qubit gate is simply a 3D rotation of this globe."
    },
    "hadamard": {
        "title": "Hadamard Gate (H)",
        "summary": "The fundamental gateway to quantum mechanics. It converts definite computational basis states into balanced superpositions: H|0⟩ = (|0⟩ + |1⟩)/√2 = |+⟩, and H|1⟩ = (|0⟩ − |1⟩)/√2 = |−⟩.",
        "math": "H = \\frac{1}{\\sqrt{2}} \\begin{pmatrix} 1 & 1 \\\\ 1 & -1 \\end{pmatrix}",
        "analogy": "The Hadamard gate sets a stationary coin spinning with exactly a 50-50 chance of landing on Heads or Tails."
    },
    "entanglement": {
        "title": "Quantum Entanglement",
        "summary": "A phenomenon where two or more qubits become inextricably correlated such that the quantum state of one cannot be described independently of the state of the other, even when separated by light-years.",
        "math": "|Φ+⟩ = \\frac{|00⟩ + |11⟩}{\\sqrt{2}} \\neq |ψ_A⟩ \\otimes |ψ_B⟩",
        "analogy": "Imagine two magic dice rolled in different cities: each die is individually random, but whenever you check, both dice always land on the exact same number."
    },
    "grover": {
        "title": "Grover's Search Algorithm",
        "summary": "Searches an unstructured database of N items in O(√N) evaluations, offering a quadratic speedup over classical O(N) search. It works by repeatedly flipping the phase of the target state (Oracle) and inverting amplitudes about the average (Diffusion Operator).",
        "math": "G = (2|s⟩⟨s| - I) O_x",
        "analogy": "Like using constructive wave interference: we make the target answer's wave peak higher and higher while destructive interference cancels out all the wrong answers."
    },
    "phase_kickback": {
        "title": "Phase Kickback",
        "summary": "A profound quantum effect where an operation on a target qubit in an eigenstate (like |−⟩) kicks back a phase shift onto the controlling qubit, allowing oracles to imprint global information without measuring.",
        "math": "CNOT |x⟩|−⟩ = (-1)^{f(x)} |x⟩|−⟩",
        "analogy": "Like kicking a heavy wall while standing on roller skates: instead of moving the wall, the force kicks you backward."
    },
    "teleportation": {
        "title": "Quantum Teleportation",
        "summary": "Transmits an unknown quantum state |ψ⟩ from Alice to Bob without physical movement of the particle. Uses 1 shared entangled Bell pair and 2 classical bits. The sender's original state is destroyed upon Bell measurement, strictly preserving the No-Cloning theorem.",
        "math": "|ψ⟩_A \\otimes |\\Phi^+⟩_{AB} \\xrightarrow{Bell\\ Meas} (c_0, c_1) \\xrightarrow{Z^{c_0} X^{c_1}} |ψ⟩_B",
        "analogy": "Like transmitting the exact blueprint of a sculpture over the phone: assembling the duplicate at the receiver's end requires completely melting down the original sculpture."
    },
    "bb84": {
        "title": "BB84 Quantum Key Distribution (QKD)",
        "summary": "The first quantum cryptography protocol (1984). Encodes cryptographic key bits in photon polarization bases (+ or ×). Any eavesdropper (Eve) attempting to measure photons irreversibly disturbs the quantum states, generating detectable Quantum Bit Error Rate (QBER > 11%).",
        "math": "QBER = \\frac{\\text{Errors}}{\\text{Sifted Bits}} \\le 11\\% \\implies \\text{Secure}",
        "analogy": "Like writing a secret in invisible ink on delicate soap bubbles: if anyone tries to touch or read the bubbles en route, they burst and leave obvious evidence."
    },
    "no_cloning": {
        "title": "The No-Cloning Theorem",
        "summary": "A fundamental theorem of quantum mechanics proving it is mathematically impossible to create an identical copy of an arbitrary unknown quantum state. Stems from the linearity of unitary quantum operators.",
        "math": "U(|ψ⟩|0⟩) = |ψ⟩|ψ⟩ \\quad \\text{is impossible for general } |ψ⟩",
        "analogy": "You cannot photocopy a spinning coin in mid-air without stopping its spin and forcing it to land on one side."
    },
    "decoherence": {
        "title": "Decoherence & Hardware Noise (T1 / T2)",
        "summary": "The loss of quantum coherence caused by environmental coupling in real QPUs. Characterized by T1 (thermal energy relaxation from |1⟩ to |0⟩) and T2 (dephasing on the Bloch sphere equator). Error mitigation and fault tolerance are required to overcome decoherence.",
        "math": "T_2 \\le 2 T_1, \\quad \\rho_{01}(t) = \\rho_{01}(0) e^{-t/T_2}",
        "analogy": "A spinning top slows down and falls over due to floor friction (T1), and wobbles out of sync due to air currents (T2)."
    },
    "quantum_volume": {
        "title": "Quantum Volume (QV)",
        "summary": "A hardware-agnostic benchmark metric quantifying the capability of a quantum processor. Measures the largest random square circuit (depth = number of qubits) that can be executed successfully with fidelity above 2/3.",
        "math": "V_Q = 2^{\\min(N, d)}",
        "analogy": "Like testing an engine not just by horsepower, but by running it through rigorous endurance courses with maximum gear complexity."
    },
    "ghz": {
        "title": "GHZ State (Greenberger-Horne-Zeilinger)",
        "summary": "A maximally entangled quantum state of 3 or more qubits: (|000⟩ + |111⟩)/√2. Crucial for demonstrating quantum non-locality and multi-party quantum communication protocols.",
        "math": "|GHZ⟩ = \\frac{|000⟩ + |111⟩}{\\sqrt{2}}",
        "analogy": "Three synchronized lights across the galaxy: if any one turns blue, all three are guaranteed to be blue."
    },
    "qft": {
        "title": "Quantum Fourier Transform (QFT)",
        "summary": "The quantum analogue of the discrete Fourier transform. Maps computational basis states to phase states in O(n²) quantum gates, providing exponential speedup over classical FFT O(n 2ⁿ). The core subroutine in Shor's factoring algorithm and Quantum Phase Estimation.",
        "math": "|j⟩ \\mapsto \\frac{1}{\\sqrt{2^n}} \\sum_{k=0}^{2^n-1} e^{2\\pi i j k / 2^n} |k⟩",
        "analogy": "Like listening to an orchestra chord and instantly knowing every individual musical note and harmonic overtone present in the sound."
    },
    "deutsch_jozsa": {
        "title": "Deutsch-Jozsa Algorithm",
        "summary": "One of the first examples of exponential quantum advantage. Determines whether a boolean function f(x) is constant (all 0s or all 1s) or balanced (equal 0s and 1s) using exactly 1 quantum oracle evaluation, whereas classical computers require 2^(n-1) + 1 queries.",
        "math": "|0⟩^{\\otimes n} \\xrightarrow{H^{\\otimes n}} \\frac{1}{\\sqrt{2^n}}\\sum |x⟩ \\xrightarrow{U_f} \\text{Interference} \\xrightarrow{H^{\\otimes n}} |00\\dots0⟩ \\text{ iff constant}",
        "analogy": "Checking if a coin is double-sided or fair with a single look, without having to flip it repeatedly."
    }
}

COMMON_BUGS_KB = [
    {
        "id": "missing_superposition",
        "check": lambda gates, q_count: not any(g.name.upper() == "H" for g in gates),
        "issue": "No superposition detected in circuit",
        "hint": "Quantum algorithms gain speed through superposition. Consider adding a Hadamard (H) gate to initialize your qubits."
    },
    {
        "id": "bell_missing_cnot",
        "check": lambda gates, q_count: q_count >= 2 and any(g.name.upper() == "H" for g in gates) and not any(g.name.upper() in ("CNOT", "CX") for g in gates),
        "issue": "Superposition created, but no 2-qubit entangling gate found",
        "hint": "To create an entangled Bell state, you need a two-qubit gate like CNOT to correlate your qubits."
    },
    {
        "id": "early_measurement",
        "check": lambda gates, q_count: any(g.name.upper() == "MEASURE" and g.step < max(other.step for other in gates) for g in gates),
        "issue": "Measurement placed before unitary computation finishes",
        "hint": "Measurement collapses quantum superposition into classical states. Ensure measurements are placed at the end of the circuit."
    }
]
