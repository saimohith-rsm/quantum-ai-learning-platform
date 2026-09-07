import time
import numpy as np
from typing import List, Dict, Any, Tuple
from app.quantum.gates import (
    get_single_qubit_matrix,
    apply_single_qubit_gate,
    apply_cnot_gate,
    apply_cz_gate,
    apply_swap_gate,
    apply_toffoli_gate,
    apply_controlled_phase
)
from app.schemas import (
    CircuitSchema,
    GateSchema,
    StatevectorEntry,
    BlochVector,
    SimulationStep,
    SimulationResponse
)
from app.quantum.qiskit_export import circuit_to_qiskit, circuit_to_qasm

class QuantumSimulator:
    """
    High-performance, mathematically exact statevector quantum circuit simulator.
    Supports step-by-step statevector inspection, single-qubit reduced density matrix
    calculation for 3D Bloch sphere visualization, and Monte-Carlo measurement shots.
    """

    def __init__(self, num_qubits: int):
        if num_qubits < 1 or num_qubits > 8:
            raise ValueError("Qubit count must be between 1 and 8")
        self.num_qubits = num_qubits
        self.reset()

    def reset(self):
        """Initializes register to |0...0>"""
        self.state_tensor = np.zeros((2,) * self.num_qubits, dtype=complex)
        # First element [0, 0, ..., 0] is amplitude 1.0
        self.state_tensor[(0,) * self.num_qubits] = 1.0 + 0.0j

    def get_statevector_flat(self) -> np.ndarray:
        """Returns 1D statevector of length 2^n in standard computational basis."""
        return self.state_tensor.flatten()

    def calculate_single_qubit_bloch(self, qubit_idx: int) -> BlochVector:
        """
        Computes the reduced density matrix rho_k by taking partial trace over all other qubits.
        Extracts Bloch coordinates (x, y, z), purity, and spherical angles (theta, phi).
        """
        n = self.num_qubits
        # Reshape or trace out other qubits
        # Reorder axes so that target qubit is first (axis 0), rest are flattened
        axes = [qubit_idx] + [i for i in range(n) if i != qubit_idx]
        permuted = np.transpose(self.state_tensor, axes)
        matrix_psi = permuted.reshape(2, 2 ** (n - 1))
        
        # Reduced density matrix rho = psi @ psi.conj().T
        rho = matrix_psi @ matrix_psi.conj().T
        
        # Normalization guard
        tr = np.trace(rho)
        if tr > 1e-12:
            rho = rho / tr
        
        # Pauli expectation values
        # rho = 0.5 * (I + x*sigma_x + y*sigma_y + z*sigma_z)
        # x = 2 * Re(rho[0, 1])
        # y = -2 * Im(rho[0, 1])
        # z = Re(rho[0, 0] - rho[1, 1])
        x = float(2.0 * np.real(rho[0, 1]))
        y = float(-2.0 * np.imag(rho[0, 1]))
        z = float(np.real(rho[0, 0] - rho[1, 1]))

        # Clean tiny floating point noise
        x = 0.0 if abs(x) < 1e-7 else x
        y = 0.0 if abs(y) < 1e-7 else y
        z = 0.0 if abs(z) < 1e-7 else z

        # Purity = Tr(rho^2) = 0.5 * (1 + r^2)
        r = np.sqrt(x * x + y * y + z * z)
        purity = float(np.clip(0.5 * (1.0 + r * r), 0.0, 1.0))

        # Spherical coordinates
        theta = float(np.arccos(np.clip(z / (r if r > 1e-7 else 1.0), -1.0, 1.0)))
        phi = float(np.arctan2(y, x))
        if phi < 0:
            phi += 2.0 * np.pi

        return BlochVector(
            qubit=qubit_idx,
            x=round(x, 5),
            y=round(y, 5),
            z=round(z, 5),
            purity=round(purity, 5),
            theta_rad=round(theta, 5),
            phi_rad=round(phi, 5)
        )

    def get_all_bloch_vectors(self) -> List[BlochVector]:
        return [self.calculate_single_qubit_bloch(q) for q in range(self.num_qubits)]

    def get_formatted_statevector(self) -> List[StatevectorEntry]:
        flat = self.get_statevector_flat()
        entries = []
        n = self.num_qubits
        for idx, amp in enumerate(flat):
            prob = float(np.abs(amp) ** 2)
            phase = float(np.angle(amp))
            if phase < 0:
                phase += 2.0 * np.pi
            
            # Binary label e.g. "01"
            label = format(idx, f"0{n}b")
            entries.append(StatevectorEntry(
                index=idx,
                label=label,
                real=round(float(np.real(amp)), 6),
                imag=round(float(np.imag(amp)), 6),
                magnitude=round(float(np.abs(amp)), 6),
                probability=round(prob, 6),
                phase_rad=round(phase, 4),
                phase_deg=round(np.degrees(phase), 2)
            ))
        return entries

    def get_probabilities(self) -> Dict[str, float]:
        flat = self.get_statevector_flat()
        n = self.num_qubits
        probs = {}
        for idx, amp in enumerate(flat):
            p = float(np.abs(amp) ** 2)
            label = format(idx, f"0{n}b")
            probs[label] = round(p, 6)
        return probs

    def sample_shots(self, shots: int = 1024) -> Dict[str, int]:
        """Performs Monte-Carlo measurement sampling over basis states."""
        flat = self.get_statevector_flat()
        probs = np.abs(flat) ** 2
        total_p = np.sum(probs)
        if total_p > 1e-12:
            probs = probs / total_p
        else:
            probs = np.ones_like(probs) / len(probs)
        
        indices = np.arange(len(probs))
        samples = np.random.choice(indices, size=shots, p=probs)
        unique, counts = np.unique(samples, return_counts=True)
        
        n = self.num_qubits
        counts_dict = {format(i, f"0{n}b"): 0 for i in range(2 ** n)}
        for u, c in zip(unique, counts):
            label = format(int(u), f"0{n}b")
            counts_dict[label] = int(c)
        return counts_dict

    def apply_gate(self, gate: GateSchema):
        """Applies a single gate to the current state tensor."""
        name = gate.name.upper()
        target = gate.target

        if target >= self.num_qubits:
            raise ValueError(f"Target qubit {target} exceeds total qubits ({self.num_qubits})")

        if name in ("H", "X", "Y", "Z", "S", "SDG", "S_DAG", "T", "TDG", "T_DAG", "RX", "RY", "RZ", "P", "PHASE", "I"):
            mat = get_single_qubit_matrix(name, gate.params)
            self.state_tensor = apply_single_qubit_gate(self.state_tensor, mat, target)
        elif name in ("CNOT", "CX"):
            if gate.control is None or gate.control >= self.num_qubits or gate.control == target:
                raise ValueError(f"Invalid CNOT control {gate.control} for target {target}")
            self.state_tensor = apply_cnot_gate(self.state_tensor, gate.control, target)
        elif name == "CZ":
            if gate.control is None or gate.control >= self.num_qubits or gate.control == target:
                raise ValueError(f"Invalid CZ control {gate.control} for target {target}")
            self.state_tensor = apply_cz_gate(self.state_tensor, gate.control, target)
        elif name == "SWAP":
            if gate.control is None or gate.control >= self.num_qubits or gate.control == target:
                raise ValueError(f"Invalid SWAP qubit {gate.control} with target {target}")
            self.state_tensor = apply_swap_gate(self.state_tensor, gate.control, target)
        elif name in ("CCX", "TOFFOLI"):
            c1 = gate.control
            c2 = gate.control2
            if c1 is None or c2 is None or len({c1, c2, target}) < 3:
                raise ValueError("Toffoli requires 2 distinct control qubits and 1 target qubit")
            self.state_tensor = apply_toffoli_gate(self.state_tensor, c1, c2, target)
        elif name in ("CPHASE", "CRZ"):
            phi = float(gate.params.get("phi", np.pi / 2.0)) if gate.params else np.pi / 2.0
            self.state_tensor = apply_controlled_phase(self.state_tensor, gate.control, target, phi)
        elif name in ("MEASURE", "BARRIER"):
            # Informational / non-unitary in pure simulator mode
            pass
        else:
            raise ValueError(f"Unsupported gate type: {name}")

    def simulate_circuit(self, circuit: CircuitSchema, shots: int = 1024, record_steps: bool = True) -> SimulationResponse:
        start_time = time.perf_counter()
        self.reset()

        steps_log: List[SimulationStep] = []

        # Initial state before gates (Step 0)
        if record_steps:
            steps_log.append(SimulationStep(
                step_index=0,
                gate_applied="INIT",
                target_qubit=None,
                control_qubit=None,
                probabilities=self.get_probabilities(),
                bloch_vectors=self.get_all_bloch_vectors(),
                statevector=self.get_formatted_statevector()
            ))

        # Sort gates by time step, then target
        sorted_gates = sorted(circuit.gates, key=lambda g: (g.step, g.target))

        for idx, gate in enumerate(sorted_gates, start=1):
            self.apply_gate(gate)
            if record_steps:
                steps_log.append(SimulationStep(
                    step_index=idx,
                    gate_applied=gate.name,
                    target_qubit=gate.target,
                    control_qubit=gate.control,
                    probabilities=self.get_probabilities(),
                    bloch_vectors=self.get_all_bloch_vectors(),
                    statevector=self.get_formatted_statevector()
                ))

        final_sv = self.get_formatted_statevector()
        probs = self.get_probabilities()
        shot_counts = self.sample_shots(shots)
        bloch_vecs = self.get_all_bloch_vectors()

        qiskit_code = circuit_to_qiskit(circuit)
        qasm_code = circuit_to_qasm(circuit)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return SimulationResponse(
            num_qubits=self.num_qubits,
            statevector=final_sv,
            probabilities=probs,
            shot_counts=shot_counts,
            bloch_vectors=bloch_vecs,
            steps=steps_log,
            qiskit_code=qiskit_code,
            qasm_code=qasm_code,
            execution_time_ms=round(elapsed_ms, 3)
        )
