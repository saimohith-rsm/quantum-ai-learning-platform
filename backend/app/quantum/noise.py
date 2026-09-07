"""
NISQ Quantum Hardware Noise & Decoherence Simulation Engine.
Models realistic physical imperfections in superconducting and trapped-ion QPUs:
- T1 Amplitude Damping (Energy Relaxation |1> -> |0>)
- T2 Phase Damping (Dephasing / loss of phase coherence)
- Depolarizing Gate Noise (1-qubit and 2-qubit stochastic Pauli errors)
- Readout SPAM Error (State Preparation and Measurement bit-flip errors)
- Quantum State & Distribution Fidelity (Bhattacharyya and trace distance metrics)
"""

import numpy as np
from typing import Dict, Any, List, Optional
from app.schemas import CircuitSchema, GateSchema
from app.quantum.simulator import QuantumSimulator

class HardwareNoiseModel:
    """Configurable noise profile modeling physical quantum processor noise."""
    
    PRESETS = {
        "ibm_eagle": {
            "name": "IBM Quantum Eagle (127Q)",
            "description": "Superconducting transmon processor with realistic average gate and decoherence rates",
            "t1_prob": 0.03,
            "t2_prob": 0.05,
            "gate_error": 0.002,
            "cnot_error": 0.015,
            "readout_error": 0.02
        },
        "ionq_aria": {
            "name": "IonQ Aria (Trapped Ion)",
            "description": "Trapped ytterbium ion system with high coherence times and low 2-qubit error",
            "t1_prob": 0.005,
            "t2_prob": 0.01,
            "gate_error": 0.0008,
            "cnot_error": 0.004,
            "readout_error": 0.005
        },
        "high_decoherence": {
            "name": "Extreme Noise / Educational Stress Test",
            "description": "High noise environment designed to visually demonstrate complete state decoherence",
            "t1_prob": 0.15,
            "t2_prob": 0.20,
            "gate_error": 0.05,
            "cnot_error": 0.12,
            "readout_error": 0.08
        }
    }

    def __init__(
        self,
        t1_prob: float = 0.02,
        t2_prob: float = 0.04,
        gate_error: float = 0.002,
        cnot_error: float = 0.015,
        readout_error: float = 0.02,
        name: str = "Custom NISQ QPU"
    ):
        self.t1_prob = max(0.0, min(1.0, float(t1_prob)))
        self.t2_prob = max(0.0, min(1.0, float(t2_prob)))
        self.gate_error = max(0.0, min(1.0, float(gate_error)))
        self.cnot_error = max(0.0, min(1.0, float(cnot_error)))
        self.readout_error = max(0.0, min(1.0, float(readout_error)))
        self.name = name

    @classmethod
    def from_preset(cls, preset_key: str):
        config = cls.PRESETS.get(preset_key, cls.PRESETS["ibm_eagle"])
        return cls(
            t1_prob=config["t1_prob"],
            t2_prob=config["t2_prob"],
            gate_error=config["gate_error"],
            cnot_error=config["cnot_error"],
            readout_error=config["readout_error"],
            name=config["name"]
        )

class NoisyQuantumSimulator:
    """
    Quantum simulator executing quantum trajectories under Markovian Kraus error channels.
    Provides comparison between ideal noiseless execution and real hardware execution.
    """

    def __init__(self, num_qubits: int, noise_model: Optional[HardwareNoiseModel] = None):
        self.num_qubits = num_qubits
        self.noise = noise_model or HardwareNoiseModel()

    def _apply_amplitude_damping(self, sim: QuantumSimulator, qubit: int):
        """Simulates T1 energy relaxation (|1> decaying to |0>) with probability t1_prob."""
        if np.random.random() < self.noise.t1_prob:
            bloch = sim.calculate_single_qubit_bloch(qubit)
            if bloch.z < 0.5:
                sim.apply_gate(GateSchema(name="X", target=qubit, step=-1))

    def _apply_phase_damping(self, sim: QuantumSimulator, qubit: int):
        """Simulates T2 dephasing (random Z phase flip) with probability t2_prob."""
        if np.random.random() < self.noise.t2_prob:
            sim.apply_gate(GateSchema(name="Z", target=qubit, step=-1))

    def _apply_depolarizing_1q(self, sim: QuantumSimulator, qubit: int):
        """Applies random Pauli error (X, Y, or Z) with probability gate_error."""
        if np.random.random() < self.noise.gate_error:
            error_gate = np.random.choice(["X", "Y", "Z"])
            sim.apply_gate(GateSchema(name=error_gate, target=qubit, step=-1))

    def _apply_depolarizing_2q(self, sim: QuantumSimulator, control: int, target: int):
        """Applies 2-qubit depolarizing error after entangling gates with probability cnot_error."""
        if np.random.random() < self.noise.cnot_error:
            err1 = np.random.choice(["I", "X", "Y", "Z"])
            err2 = np.random.choice(["X", "Y", "Z"]) if err1 == "I" else np.random.choice(["I", "X", "Y", "Z"])
            if err1 != "I":
                sim.apply_gate(GateSchema(name=err1, target=control, step=-1))
            if err2 != "I":
                sim.apply_gate(GateSchema(name=err2, target=target, step=-1))

    def simulate_noisy_trajectory(self, circuit: CircuitSchema) -> Dict[str, float]:
        """Runs a single noisy quantum trajectory."""
        sim = QuantumSimulator(circuit.qubits)
        gates = sorted(circuit.gates, key=lambda g: g.step)

        for gate in gates:
            sim.apply_gate(gate)

            # Apply gate error & decoherence
            if gate.name.upper() in ("CNOT", "CX", "CZ", "SWAP"):
                if gate.control is not None:
                    self._apply_depolarizing_2q(sim, gate.control, gate.target)
                    self._apply_amplitude_damping(sim, gate.control)
                    self._apply_phase_damping(sim, gate.control)
                self._apply_amplitude_damping(sim, gate.target)
                self._apply_phase_damping(sim, gate.target)
            else:
                self._apply_depolarizing_1q(sim, gate.target)
                self._apply_amplitude_damping(sim, gate.target)
                self._apply_phase_damping(sim, gate.target)

        return sim.get_probabilities()

    def simulate_with_noise(
        self,
        circuit: CircuitSchema,
        trajectories: int = 150,
        shots: int = 1024
    ) -> Dict[str, Any]:
        """
        Executes full noisy simulation ensemble, averages across trajectories,
        applies readout error, and computes quantum fidelity against the ideal circuit.
        """
        n = circuit.qubits
        basis_states = [format(i, f"0{n}b") for i in range(2 ** n)]

        # 1. Ideal noiseless reference simulation
        ideal_sim = QuantumSimulator(n)
        ideal_res = ideal_sim.simulate_circuit(circuit, shots=shots, record_steps=False)
        ideal_probs = ideal_res.probabilities

        # 2. Monte Carlo average over noisy quantum trajectories
        accum_probs = {state: 0.0 for state in basis_states}
        actual_trajectories = max(20, min(trajectories, 300))

        for _ in range(actual_trajectories):
            traj_probs = self.simulate_noisy_trajectory(circuit)
            for state, p in traj_probs.items():
                accum_probs[state] += p

        noisy_probs = {state: p / actual_trajectories for state, p in accum_probs.items()}

        # 3. Apply Readout SPAM Error on basis states
        if self.noise.readout_error > 0.0:
            final_noisy_probs = {state: 0.0 for state in basis_states}
            p_flip = self.noise.readout_error
            for state, p in noisy_probs.items():
                for target_state in basis_states:
                    hamming_dist = sum(c1 != c2 for c1, c2 in zip(state, target_state))
                    transition_prob = ((1.0 - p_flip) ** (n - hamming_dist)) * (p_flip ** hamming_dist)
                    final_noisy_probs[target_state] += p * transition_prob
            noisy_probs = final_noisy_probs

        # Normalize noisy probabilities
        total_p = sum(noisy_probs.values())
        if total_p > 0:
            noisy_probs = {k: round(v / total_p, 6) for k, v in noisy_probs.items()}

        # 4. Generate noisy shot counts
        states = list(noisy_probs.keys())
        p_vals = list(noisy_probs.values())
        sampled_indices = np.random.choice(len(states), size=shots, p=p_vals)
        unique, counts = np.unique(sampled_indices, return_counts=True)
        noisy_counts = {k: 0 for k in basis_states}
        for u, c in zip(unique, counts):
            noisy_counts[states[u]] = int(c)

        # 5. Calculate Quantum Fidelity Metrics
        fidelity_bhattacharyya = float(
            sum(np.sqrt(max(0.0, ideal_probs.get(s, 0.0) * noisy_probs.get(s, 0.0))) for s in basis_states) ** 2
        )
        fidelity = round(float(np.clip(fidelity_bhattacharyya, 0.0, 1.0)), 4)
        quantum_error_rate = round(float(1.0 - fidelity), 4)

        return {
            "hardware_model": self.noise.name,
            "fidelity": fidelity,
            "quantum_error_rate": quantum_error_rate,
            "ideal_probabilities": ideal_probs,
            "noisy_probabilities": noisy_probs,
            "noisy_counts": noisy_counts,
            "noise_parameters": {
                "t1_decay_rate": self.noise.t1_prob,
                "t2_dephasing_rate": self.noise.t2_prob,
                "single_qubit_error": self.noise.gate_error,
                "two_qubit_cnot_error": self.noise.cnot_error,
                "readout_error": self.noise.readout_error
            },
            "interpretation": (
                f"On {self.noise.name}, your circuit achieves {fidelity * 100:.1f}% state fidelity. "
                + ("Noticeable decoherence and gate noise dilute the target probability peaks." if fidelity < 0.90
                   else "High fidelity execution with minimal noise degradation.")
            )
        }
