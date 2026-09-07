import os
import json
import httpx
from typing import List, Dict, Any, Optional
from app.config import GEMINI_API_KEY, OPENAI_API_KEY, DEFAULT_AI_PROVIDER
from app.schemas import CircuitSchema, TutorResponse
from app.tutor.quantum_kb import QUANTUM_CONCEPTS_KB, COMMON_BUGS_KB
from app.quantum.simulator import QuantumSimulator

class AITutorEngine:
    """
    Intelligent AI Quantum Tutor for the QuantumAI learning platform.
    Combines rule-based verified quantum physics heuristics with multi-provider LLMs (Gemini, OpenAI ChatGPT)
    and pedagogical Socratic guidance.
    """

    def __init__(self):
        self.gemini_key = GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
        self.openai_key = OPENAI_API_KEY or os.getenv("OPENAI_API_KEY", "")
        self.default_provider = DEFAULT_AI_PROVIDER or "gemini"

    def _call_gemini_api(self, prompt: str, system_prompt: str) -> Optional[str]:
        """Calls Google Gemini API if configured."""
        if not self.gemini_key:
            return None

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_key}"
        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": f"{system_prompt}\n\nUser Question/Circuit:\n{prompt}"}]}
            ],
            "generationConfig": {
                "temperature": 0.4,
                "maxOutputTokens": 800
            }
        }

        try:
            with httpx.Client(timeout=12.0) as client:
                resp = client.post(url, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    candidates = data.get("candidates", [])
                    if candidates:
                        parts = candidates[0].get("content", {}).get("parts", [])
                        if parts:
                            return parts[0].get("text", "").strip()
        except Exception as e:
            print(f"Gemini API call failed, falling back: {e}")
        return None

    def _call_openai_api(self, prompt: str, system_prompt: str) -> Optional[str]:
        """Calls OpenAI ChatGPT API if configured."""
        if not self.openai_key:
            return None

        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openai_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.4,
            "max_tokens": 800
        }

        try:
            with httpx.Client(timeout=12.0) as client:
                resp = client.post(url, json=payload, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    choices = data.get("choices", [])
                    if choices:
                        return choices[0].get("message", {}).get("content", "").strip()
        except Exception as e:
            print(f"OpenAI API call failed, falling back: {e}")
        return None

    def explain_circuit(self, circuit: CircuitSchema, user_level: str = "Beginner") -> TutorResponse:
        """Analyzes and explains the quantum mechanics of the given circuit."""
        gates = circuit.gates
        num_qubits = circuit.qubits

        if not gates:
            return TutorResponse(
                title="Empty Circuit",
                explanation="Your circuit currently has no quantum gates. All qubits begin in the ground state |0...0⟩. Try placing a Hadamard (H) gate on Qubit 0 to enter superposition!",
                key_insights=["Qubits are initialized to |0⟩ by default", "Without gates, no quantum operations occur"],
                suggested_actions=["Drag an 'H' gate onto Qubit 0", "Run simulation to observe the state change"],
                source="quantum_engine"
            )

        # Detect famous algorithms
        gate_names = [g.name.upper() for g in sorted(gates, key=lambda x: x.step)]
        has_h = "H" in gate_names
        has_cnot = "CNOT" in gate_names or "CX" in gate_names
        has_cz = "CZ" in gate_names
        has_x = "X" in gate_names

        # Run simulator to check probabilities
        sim = QuantumSimulator(num_qubits)
        sim_res = sim.simulate_circuit(circuit, shots=512, record_steps=False)
        probs = sim_res.probabilities

        # Case 1: Bell State
        if num_qubits == 2 and len(gates) == 2 and has_h and has_cnot:
            g0, g1 = sorted(gates, key=lambda x: x.step)
            if g0.name.upper() == "H" and g0.target == 0 and g1.name.upper() in ("CNOT", "CX") and g1.control == 0 and g1.target == 1:
                return TutorResponse(
                    title="Maximally Entangled Bell State |Φ+⟩",
                    explanation="Brilliant! You have constructed the canonical Bell state (|00⟩ + |11⟩)/√2. Step 1 (Hadamard on Qubit 0) places q0 into equal superposition (|0⟩ + |1⟩)/√2. Step 2 (CNOT) entangles Qubit 1 conditionally: if q0 is |1⟩, q1 is flipped from |0⟩ to |1⟩, creating perfect correlation.",
                    key_insights=[
                        "Neither qubit has a definite independent state anymore",
                        "Measuring q0 as 0 guarantees q1 is 0; measuring q0 as 1 guarantees q1 is 1",
                        "Measurement distribution is exactly 50% |00⟩ and 50% |11⟩"
                    ],
                    suggested_actions=[
                        "Inspect the 3D Bloch Sphere: notice both qubits have zero pure polarization in isolation",
                        "Try adding a Pauli-Z or Pauli-X gate before CNOT to create other Bell states (|Φ-⟩ or |Ψ+⟩)"
                    ],
                    quantum_math="|00⟩ \\xrightarrow{H_0} \\frac{|00⟩ + |10⟩}{\\sqrt{2}} \\xrightarrow{CNOT_{0\\to 1}} \\frac{|00⟩ + |11⟩}{\\sqrt{2}} = |\\Phi^+⟩",
                    source="quantum_engine"
                )

        # Case 2: Grover's Search
        if num_qubits >= 2 and has_cz and has_h and (has_x or len(gates) >= 6):
            return TutorResponse(
                title="Grover's Amplitude Amplification",
                explanation="This circuit exhibits the core structure of Grover's Search Algorithm. It prepares equal superposition, marks the target item with a phase inversion (Oracle), and uses the diffusion operator (inversion about the mean) to constructively interfere the target amplitude.",
                key_insights=[
                    "Oracle flips the phase (-1) of the searched solution",
                    "Diffusion operator flips amplitudes around the average, boosting the target probability",
                    "Provides O(√N) quadratic quantum speedup over classical brute-force"
                ],
                suggested_actions=[
                    "Look at the Statevector Amplitude chart to see the target state peak above others",
                    "Check the measurement histogram for near-100% convergence"
                ],
                quantum_math="G = (2|s⟩⟨s| - I) O_{oracle}",
                source="quantum_engine"
            )

        # Generic breakdown
        step_explanations = []
        for g in sorted(gates, key=lambda x: x.step):
            name = g.name.upper()
            if name == "H":
                step_explanations.append(f"• Hadamard on Q{g.target}: Creates equal superposition (|0⟩ + |1⟩)/√2.")
            elif name == "X":
                step_explanations.append(f"• Pauli-X on Q{g.target}: Bit-flip gate, maps |0⟩ ↔ |1⟩.")
            elif name == "Z":
                step_explanations.append(f"• Pauli-Z on Q{g.target}: Phase-flip gate, maps |1⟩ → -|1⟩.")
            elif name in ("CNOT", "CX"):
                step_explanations.append(f"• CNOT (Control Q{g.control} → Target Q{g.target}): Flips Q{g.target} whenever Q{g.control} is |1⟩.")
            elif name == "CZ":
                step_explanations.append(f"• Controlled-Z between Q{g.control} and Q{g.target}: Inverts phase only when both qubits are |1⟩.")
            elif name == "SWAP":
                step_explanations.append(f"• SWAP between Q{g.control} and Q{g.target}: Exchanges the quantum states of both qubits.")
            else:
                step_explanations.append(f"• {name} on Q{g.target}: Applies unitary transformation.")

        top_states = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:3]
        state_summary = ", ".join([f"|{k}⟩ ({v*100:.1f}%)" for k, v in top_states if v > 0.01])

        return TutorResponse(
            title=f"{num_qubits}-Qubit Quantum Circuit Walkthrough",
            explanation=f"This circuit contains {len(gates)} gate operations across {num_qubits} qubits. The final quantum state predominantly collapses to: {state_summary}.\n\nStep breakdown:\n" + "\n".join(step_explanations[:6]),
            key_insights=[
                f"Circuit Depth: {max(g.step for g in gates) + 1} time steps",
                f"Active Qubits: {num_qubits}",
                "State amplitudes and relative phases determine measurement probabilities"
            ],
            suggested_actions=[
                "Use the Step Scrubber to observe how each gate evolves the statevector",
                "Examine the Bloch Sphere to see individual qubit rotations"
            ],
            source="quantum_engine"
        )

    def debug_circuit(self, circuit: CircuitSchema, goal: str, user_level: str = "Beginner") -> TutorResponse:
        """Diagnoses why the learner's circuit might not meet their intended goal."""
        gates = circuit.gates
        num_qubits = circuit.qubits
        goal_lower = goal.lower()

        # Goal: Bell State
        if "bell" in goal_lower or "entangle" in goal_lower:
            has_h = any(g.name.upper() == "H" for g in gates)
            has_cnot = any(g.name.upper() in ("CNOT", "CX") for g in gates)

            if not has_h:
                return TutorResponse(
                    title="Missing Superposition for Entanglement",
                    explanation="To create a Bell state, one qubit must first be in a superposition before entangling it. Currently, your circuit lacks a Hadamard (H) gate.",
                    key_insights=["Entanglement requires correlating a superposition with a second qubit"],
                    suggested_actions=["Place a Hadamard (H) gate on Qubit 0 at Step 0", "Follow it with a CNOT gate from Qubit 0 to Qubit 1"],
                    quantum_math="|00⟩ \\xrightarrow{H_0} \\frac{|00⟩ + |10⟩}{\\sqrt{2}}",
                    source="debugger"
                )
            elif not has_cnot:
                return TutorResponse(
                    title="Missing 2-Qubit Entangler",
                    explanation="You have created a superposition with your Hadamard gate, but the qubits remain completely independent product states because there is no 2-qubit gate.",
                    key_insights=["Single-qubit gates cannot generate entanglement alone", "CNOT is necessary to link the state of Q0 with Q1"],
                    suggested_actions=["Add a CNOT gate with Control on Qubit 0 and Target on Qubit 1"],
                    quantum_math="CNOT \\left(\\frac{|0⟩+|1⟩}{\\sqrt{2}}\\otimes |0⟩\\right) = \\frac{|00⟩ + |11⟩}{\\sqrt{2}}",
                    source="debugger"
                )
            else:
                return TutorResponse(
                    title="Circuit Structure Looks Good!",
                    explanation="Your circuit has both Hadamard and CNOT gates. Check the gate order: Hadamard MUST come before CNOT.",
                    key_insights=["Order matters in quantum mechanics: H then CNOT produces entanglement; CNOT then H does not"],
                    suggested_actions=["Verify that H is on Step 0 and CNOT is on Step 1"],
                    source="debugger"
                )

        # Goal: Grover Search
        if "grover" in goal_lower or "search" in goal_lower:
            has_cz = any(g.name.upper() == "CZ" for g in gates)
            h_count = sum(1 for g in gates if g.name.upper() == "H")

            if h_count < 2:
                return TutorResponse(
                    title="Grover: Missing Initialization Superposition",
                    explanation="Grover's search begins by putting ALL qubits into an equal superposition using Hadamard gates on each qubit.",
                    key_insights=["Equal superposition gives every database entry equal starting amplitude 1/√N"],
                    suggested_actions=["Apply Hadamard (H) to both Qubit 0 and Qubit 1 at Step 0"],
                    source="debugger"
                )
            elif not has_cz:
                return TutorResponse(
                    title="Grover: Missing Oracle",
                    explanation="To find a marked state like |11⟩, the oracle must invert the phase of the target state. A Controlled-Z (CZ) gate acts as the phase oracle for |11⟩.",
                    key_insights=["The oracle tags the target answer by multiplying its amplitude by -1"],
                    suggested_actions=["Add a CZ gate between Qubit 0 and Qubit 1 after the initial Hadamards"],
                    source="debugger"
                )
            else:
                return TutorResponse(
                    title="Grover: Check Diffusion Operator",
                    explanation="Ensure you include the full diffusion operator (Inversion about the mean): H on all qubits -> X on all qubits -> CZ -> X on all qubits -> H on all qubits.",
                    key_insights=["Without the diffusion operator, the phase marked by the oracle cannot be converted into high probability"],
                    suggested_actions=["Complete the diffusion sequence: H -> X -> CZ -> X -> H"],
                    source="debugger"
                )

        # General bug check
        for bug in COMMON_BUGS_KB:
            if bug["check"](gates, num_qubits):
                return TutorResponse(
                    title="Circuit Diagnostic Alert",
                    explanation=bug["issue"],
                    key_insights=["Circuit topology requires adjustment to achieve intended computation"],
                    suggested_actions=[bug["hint"]],
                    source="debugger"
                )

        return TutorResponse(
            title="Circuit Structure Verified",
            explanation="No common circuit anomalies detected. Run the simulation to view the state amplitudes and measurement statistics.",
            key_insights=["All gates have valid controls and targets", "Unitary evolution preserved"],
            suggested_actions=["Run Simulation to inspect statevector probabilities"],
            source="debugger"
        )

    def generate_hint(self, challenge_id: str, circuit: CircuitSchema, tier: int = 1) -> TutorResponse:
        """Provides tiered hints for challenge problems (Tier 1: Nudge, Tier 2: Math, Tier 3: Direct)."""
        from app.challenges.challenge_defs import CHALLENGES

        challenge = next((c for c in CHALLENGES if c["id"] == challenge_id), None)
        if not challenge:
            return TutorResponse(
                title="Hint Not Available",
                explanation=f"Challenge '{challenge_id}' not found.",
                source="hint_engine"
            )

        hints = challenge.get("hints", [])
        tier_index = min(tier - 1, len(hints) - 1)
        hint_text = hints[tier_index] if hints else "Keep experimenting with basic gates!"

        tier_names = {1: "Conceptual Nudge (Tier 1)", 2: "Mathematical Clue (Tier 2)", 3: "Circuit Solution Guide (Tier 3)"}

        return TutorResponse(
            title=tier_names.get(tier, "Hint"),
            explanation=hint_text,
            key_insights=[f"Challenge: {challenge['title']}", f"Difficulty: {challenge['difficulty']}"],
            suggested_actions=["Apply the clue to your circuit in the builder", "Click 'Simulate' to test your answer"],
            source="hint_engine"
        )

    def _build_circuit_context(self, circuit: Optional[CircuitSchema]) -> str:
        """Constructs concise mathematical summary of the learner's active circuit."""
        if not circuit or not circuit.gates:
            return "Active Circuit: None (Empty workspace)."
        gates_desc = ", ".join(f"{g.name}(q{g.target}{f', c={g.control}' if g.control is not None else ''})" for g in circuit.gates[:10])
        return f"Active Circuit: {circuit.qubits} qubits, {len(circuit.gates)} gates [{gates_desc}]."

    def answer_chat(
        self,
        message: str,
        circuit: Optional[CircuitSchema] = None,
        user_level: str = "Beginner",
        provider: str = "auto",
        socratic_mode: bool = False
    ) -> TutorResponse:
        """Handles conversational questions using multi-provider LLMs (Gemini/OpenAI) or verified offline KB."""
        circuit_ctx = self._build_circuit_context(circuit)

        # Build pedagogical system prompt
        if socratic_mode:
            system_prompt = (
                f"You are a Socratic Quantum Computing AI Tutor for the SIH 2026 platform. "
                f"The learner's level is {user_level}. {circuit_ctx}\n"
                f"PEDAGOGICAL INSTRUCTION: Do NOT give away full direct solutions immediately. "
                f"Provide an intuitive conceptual hint or physical analogy, and pose 1-2 thought-provoking guiding questions "
                f"to lead the student to derive the answer themselves. Keep your tone supportive, concise, and intellectually engaging."
            )
        else:
            system_prompt = (
                f"You are an expert Quantum Computing AI Tutor for the SIH 2026 platform. "
                f"The learner's level is {user_level}. {circuit_ctx}\n"
                f"Provide concise, mathematically rigorous yet intuitive explanations using Dirac notation (|ψ⟩), "
                f"clear physical analogies, and practical guidance for quantum circuit design."
            )

        llm_response = None
        source_name = "quantum_kb"

        # Determine target provider
        target_provider = provider.lower() if provider else "auto"
        if target_provider == "auto":
            if self.openai_key and self.default_provider == "openai":
                target_provider = "openai"
            elif self.gemini_key:
                target_provider = "gemini"
            elif self.openai_key:
                target_provider = "openai"

        # 1. Execute requested LLM provider
        if target_provider == "openai" and self.openai_key:
            llm_response = self._call_openai_api(message, system_prompt)
            if llm_response:
                source_name = "chatgpt_llm"
        elif target_provider == "gemini" and self.gemini_key:
            llm_response = self._call_gemini_api(message, system_prompt)
            if llm_response:
                source_name = "gemini_llm"

        if llm_response:
            return TutorResponse(
                title="Socratic Quantum Guide" if socratic_mode else "AI Quantum Tutor",
                explanation=llm_response,
                source=source_name
            )

        # 2. Fallback to rich internal verified quantum knowledge base
        msg_lower = message.lower()

        # Direct concept KB lookup
        for key, item in QUANTUM_CONCEPTS_KB.items():
            if key in msg_lower or item["title"].lower() in msg_lower:
                return TutorResponse(
                    title=item["title"],
                    explanation=f"{item['summary']}\n\nAnalogy: {item['analogy']}",
                    quantum_math=item["math"],
                    key_insights=[f"Key concept in {item['title']}", "Explore this in the Circuit Builder or Challenge Arena!"],
                    suggested_actions=["Experiment with relevant gates in the visual circuit timeline"],
                    source="quantum_kb"
                )

        # Keyword mapping for specific topics
        topic_mappings = [
            (("hadamard", " h gate", "superposition"), "hadamard"),
            (("entangle", "bell state", "epr"), "entanglement"),
            (("grover", "search algorithm", "amplitude amplification"), "grover"),
            (("bloch", "sphere", "qubit rotation"), "bloch_sphere"),
            (("teleport", "teleportation"), "teleportation"),
            (("bb84", "qkd", "cryptography", "quantum key"), "bb84"),
            (("clone", "no-cloning", "copy quantum"), "no_cloning"),
            (("decoherence", "noise", "t1", "t2"), "decoherence"),
            (("volume", "quantum volume"), "quantum_volume"),
            (("ghz", "greenberger"), "ghz"),
            (("fourier", "qft"), "qft"),
            (("deutsch", "jozsa"), "deutsch_jozsa")
        ]

        for keywords, concept_key in topic_mappings:
            if any(k in msg_lower for k in keywords) and concept_key in QUANTUM_CONCEPTS_KB:
                item = QUANTUM_CONCEPTS_KB[concept_key]
                return TutorResponse(
                    title=item["title"],
                    explanation=f"{item['summary']}\n\n{item['analogy']}",
                    quantum_math=item["math"],
                    source="quantum_kb"
                )

        # Default Socratic or direct guidance greeting
        if socratic_mode:
            return TutorResponse(
                title="Socratic Quantum Guide",
                explanation="Welcome! In Socratic Mode, I will help you reason through quantum mechanics step-by-step. What quantum state, algorithm, or gate are you curious about? Try asking: 'Why does Hadamard create superposition?' or 'How does entanglement work?'",
                key_insights=["Socratic Mode focuses on deep conceptual understanding through inquiry", "Try challenging me with questions on BB84, Grover's search, or decoherence!"],
                suggested_actions=["Ask a fundamental question about quantum physics", "Construct a circuit and ask: 'What does this circuit do?'"],
                source="socratic_engine"
            )

        return TutorResponse(
            title="AI Quantum Tutor",
            explanation="Hello! I am your AI Quantum Tutor. I can explain quantum concepts (superposition, entanglement, phase kickback, Grover's search, BB84 QKD, quantum teleportation), optimize your circuits, simulate real hardware noise (T1/T2 decoherence), or diagnose bugs. What would you like to explore today?",
            key_insights=[
                "Ask: 'What does the Hadamard gate do?'",
                "Ask: 'How does the BB84 QKD protocol detect eavesdroppers?'",
                "Ask: 'What causes quantum decoherence and T1 decay?'",
                "Click 'Explain Circuit' or 'Debug Circuit' to analyze your current workspace!"
            ],
            suggested_actions=[
                "Load an algorithm preset from the library",
                "Build a 2-qubit circuit and test the NISQ Hardware Noise simulator"
            ],
            source="quantum_kb"
        )
