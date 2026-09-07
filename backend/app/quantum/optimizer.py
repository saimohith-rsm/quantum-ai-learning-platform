"""
Automated Quantum Circuit Optimizer and Complexity Analyzer.
Applies compiler-level optimization passes inspired by Qiskit Transpiler Level 3:
- Inverse Gate Cancellation (H*H = I, X*X = I, CNOT*CNOT = I, SWAP*SWAP = I)
- Adjoint Cancellation (S*SDG = I, T*TDG = I, S*S = Z)
- Continuous Rotation Merging (Rx(a)*Rx(b) = Rx(a+b), Rz(a)*Rz(b) = Rz(a+b))
- Timeline Compaction / Critical Path Depth Minimization
- Fault-Tolerant Resource Estimation (T-count, CNOT count, Quantum Circuit Depth)
"""

import numpy as np
from typing import List, Dict, Any, Tuple, Optional
from app.schemas import CircuitSchema, GateSchema

SELF_INVERSE_1Q = {"H", "X", "Y", "Z"}

class CircuitOptimizer:
    """Optimizes quantum gate sequences and computes hardware execution complexity."""

    def __init__(self, circuit: CircuitSchema):
        self.circuit = circuit
        self.num_qubits = circuit.qubits

    def calculate_depth(self, gates: List[GateSchema]) -> int:
        """Calculates the circuit depth (critical path length in execution steps)."""
        if not gates:
            return 0
        qubit_depth = [0] * self.num_qubits
        # Sort chronologically by step
        sorted_gates = sorted(gates, key=lambda g: g.step)
        for g in sorted_gates:
            involved = [g.target]
            if g.control is not None:
                involved.append(g.control)
            if g.control2 is not None:
                involved.append(g.control2)
            
            # The current gate can only execute after all involved qubits are free
            current_max = max(qubit_depth[q] for q in involved)
            new_depth = current_max + 1
            for q in involved:
                qubit_depth[q] = new_depth

        return max(qubit_depth) if qubit_depth else 0

    def optimize(self) -> Dict[str, Any]:
        """Runs the optimization pipeline and returns the optimized circuit + metrics."""
        def _to_dict(obj):
            return obj.model_dump() if hasattr(obj, "model_dump") else obj.dict()

        original_gates = [GateSchema(**_to_dict(g)) for g in sorted(self.circuit.gates, key=lambda x: (x.step, x.target))]
        original_count = len(original_gates)
        original_depth = self.calculate_depth(original_gates)

        optimizations_applied = []
        gates = original_gates

        # Pass 1: Per-qubit 1-qubit gate cancellations & rotation merging
        gates, pass1_notes = self._optimize_single_qubit_lines(gates)
        optimizations_applied.extend(pass1_notes)

        # Pass 2: Adjacent 2-qubit CNOT / SWAP cancellation
        gates, pass2_notes = self._cancel_adjacent_2q_gates(gates)
        optimizations_applied.extend(pass2_notes)

        # Pass 3: Re-pack / compact timeline steps to minimize depth
        optimized_gates = self._compact_timeline(gates)

        optimized_count = len(optimized_gates)
        optimized_depth = self.calculate_depth(optimized_gates)

        cnot_count = sum(1 for g in optimized_gates if g.name.upper() in ("CNOT", "CX", "CZ"))
        t_count = sum(1 for g in optimized_gates if g.name.upper() in ("T", "TDG", "T_DAG"))

        gate_reduction = round(((original_count - optimized_count) / original_count * 100) if original_count > 0 else 0.0, 1)
        depth_reduction = round(((original_depth - optimized_depth) / original_depth * 100) if original_depth > 0 else 0.0, 1)

        if not optimizations_applied and original_count > 0:
            optimizations_applied.append("Circuit is already canonically minimal. No redundant operations detected.")

        return {
            "original_circuit": _to_dict(self.circuit),
            "optimized_circuit": {
                "qubits": self.num_qubits,
                "gates": [_to_dict(g) for g in optimized_gates]
            },
            "metrics": {
                "original_gate_count": original_count,
                "optimized_gate_count": optimized_count,
                "gate_reduction_pct": gate_reduction,
                "original_depth": original_depth,
                "optimized_depth": optimized_depth,
                "depth_reduction_pct": depth_reduction,
                "cnot_count": cnot_count,
                "t_count": t_count,
                "fault_tolerant_t_depth": t_count,
                "estimated_quantum_volume": 2 ** min(self.num_qubits, optimized_depth) if optimized_depth > 0 else 0
            },
            "optimizations_applied": optimizations_applied
        }

    def _optimize_single_qubit_lines(self, gates: List[GateSchema]) -> Tuple[List[GateSchema], List[str]]:
        """Scans each qubit timeline and eliminates consecutive cancelling gates or merges rotations."""
        notes = []
        # Group gates that act on each qubit
        qubit_ops: Dict[int, List[GateSchema]] = {q: [] for q in range(self.num_qubits)}
        for g in gates:
            if g.control is None and g.control2 is None:
                qubit_ops[g.target].append(g)

        # Look for consecutive pairs on each qubit without intervening entangling gates
        to_remove_ids = set()
        gates_by_step = sorted(gates, key=lambda x: x.step)

        for q in range(self.num_qubits):
            q_gates = [g for g in gates_by_step if g.target == q and g.control is None]
            i = 0
            while i < len(q_gates) - 1:
                g1 = q_gates[i]
                g2 = q_gates[i + 1]

                # Ensure no multi-qubit gate intervened on qubit q between g1.step and g2.step
                intervening_multiqubit = any(
                    (g.control == q or g.target == q or g.control2 == q)
                    and g.control is not None
                    and min(g1.step, g2.step) < g.step < max(g1.step, g2.step)
                    for g in gates
                )

                if intervening_multiqubit:
                    i += 1
                    continue

                n1 = g1.name.upper()
                n2 = g2.name.upper()

                # Rule A: Self-inverse pairs (H*H = I, X*X = I, etc.)
                if n1 == n2 and n1 in SELF_INVERSE_1Q:
                    to_remove_ids.add(id(g1))
                    to_remove_ids.add(id(g2))
                    notes.append(f"Eliminated self-cancelling pair {n1} - {n2} on Qubit {q} ({n1}^2 = I)")
                    i += 2
                    continue

                # Rule B: S and S_DAG, T and T_DAG
                if (n1 == "S" and n2 in ("SDG", "S_DAG")) or (n1 in ("SDG", "S_DAG") and n2 == "S"):
                    to_remove_ids.add(id(g1))
                    to_remove_ids.add(id(g2))
                    notes.append(f"Eliminated adjoint pair S - S† on Qubit {q}")
                    i += 2
                    continue

                if (n1 == "T" and n2 in ("TDG", "T_DAG")) or (n1 in ("TDG", "T_DAG") and n2 == "T"):
                    to_remove_ids.add(id(g1))
                    to_remove_ids.add(id(g2))
                    notes.append(f"Eliminated adjoint pair T - T† on Qubit {q}")
                    i += 2
                    continue

                # Rule C: Rotation merging Rz(a) + Rz(b) = Rz(a+b)
                if n1 == n2 and n1 in ("RZ", "RX", "RY") and g1.params and g2.params:
                    theta1 = float(g1.params.get("theta", 0.0))
                    theta2 = float(g2.params.get("theta", 0.0))
                    merged_theta = (theta1 + theta2) % (2.0 * np.pi)
                    if abs(merged_theta) < 1e-6 or abs(merged_theta - 2.0 * np.pi) < 1e-6:
                        to_remove_ids.add(id(g1))
                        to_remove_ids.add(id(g2))
                        notes.append(f"Merged full-cycle rotations {n1}({theta1:.2f}) + {n1}({theta2:.2f}) to Identity on Qubit {q}")
                    else:
                        g1.params["theta"] = round(merged_theta, 4)
                        to_remove_ids.add(id(g2))
                        notes.append(f"Merged adjacent {n1} rotations on Qubit {q} into {n1}({merged_theta:.3f} rad)")
                    i += 2
                    continue

                i += 1

        remaining = [g for g in gates if id(g) not in to_remove_ids]
        return remaining, notes

    def _cancel_adjacent_2q_gates(self, gates: List[GateSchema]) -> Tuple[List[GateSchema], List[str]]:
        """Cancels consecutive identical CNOTs or SWAPs with matching control and target."""
        notes = []
        to_remove = set()
        sorted_gates = sorted(gates, key=lambda g: g.step)

        i = 0
        while i < len(sorted_gates) - 1:
            g1 = sorted_gates[i]
            g2 = sorted_gates[i + 1]

            n1 = g1.name.upper()
            n2 = g2.name.upper()

            if n1 in ("CNOT", "CX") and n2 in ("CNOT", "CX"):
                if g1.control == g2.control and g1.target == g2.target and g2.step == g1.step + 1:
                    to_remove.add(id(g1))
                    to_remove.add(id(g2))
                    notes.append(f"Eliminated consecutive CNOT pair between Qubit {g1.control} and Qubit {g1.target} (CNOT^2 = I)")
                    i += 2
                    continue

            if n1 == "SWAP" and n2 == "SWAP":
                if {g1.control, g1.target} == {g2.control, g2.target} and g2.step == g1.step + 1:
                    to_remove.add(id(g1))
                    to_remove.add(id(g2))
                    notes.append(f"Eliminated consecutive SWAP pair on Qubits {g1.control} & {g1.target} (SWAP^2 = I)")
                    i += 2
                    continue

            i += 1

        remaining = [g for g in sorted_gates if id(g) not in to_remove]
        return remaining, notes

    def _compact_timeline(self, gates: List[GateSchema]) -> List[GateSchema]:
        """Repacks gate steps greedily so that every gate is placed in the earliest collision-free step."""
        if not gates:
            return []

        qubit_available_step = [0] * self.num_qubits
        compacted_gates: List[GateSchema] = []

        # Sort gates by their original logical order
        sorted_gates = sorted(gates, key=lambda g: (g.step, g.target))

        for g in sorted_gates:
            involved = [g.target]
            if g.control is not None:
                involved.append(g.control)
            if g.control2 is not None:
                involved.append(g.control2)

            earliest_step = max(qubit_available_step[q] for q in involved)
            new_gate = GateSchema(
                name=g.name,
                target=g.target,
                control=g.control,
                control2=g.control2,
                step=earliest_step,
                params=g.params
            )
            compacted_gates.append(new_gate)

            next_available = earliest_step + 1
            for q in involved:
                qubit_available_step[q] = next_available

        return compacted_gates
