import numpy as np
from typing import Dict, Any
from app.schemas import CircuitSchema, ChallengeSubmissionResponse
from app.challenges.challenge_defs import get_challenge_by_id
from app.quantum.simulator import QuantumSimulator

def evaluate_challenge_submission(challenge_id: str, circuit: CircuitSchema) -> ChallengeSubmissionResponse:
    challenge = get_challenge_by_id(challenge_id)
    if not challenge:
        return ChallengeSubmissionResponse(
            challenge_id=challenge_id,
            passed=False,
            fidelity=0.0,
            score=0,
            feedback=f"Unknown challenge ID: {challenge_id}",
            details={}
        )

    # 1. Qubit Count Check
    required_qubits = challenge["num_qubits"]
    if circuit.qubits != required_qubits:
        return ChallengeSubmissionResponse(
            challenge_id=challenge_id,
            passed=False,
            fidelity=0.0,
            score=0,
            feedback=f"Circuit must have exactly {required_qubits} qubits. Your circuit has {circuit.qubits} qubits.",
            details={"required_qubits": required_qubits, "circuit_qubits": circuit.qubits}
        )

    # 2. Gate Count Check
    max_gates = challenge.get("max_gates", 50)
    actual_gate_count = len(circuit.gates)
    if actual_gate_count > max_gates:
        return ChallengeSubmissionResponse(
            challenge_id=challenge_id,
            passed=False,
            fidelity=0.0,
            score=0,
            feedback=f"Gate count exceeded! Allowed maximum: {max_gates} gates. Your circuit used {actual_gate_count} gates.",
            details={"max_gates": max_gates, "actual_gates": actual_gate_count}
        )

    # 3. Simulate Circuit
    sim = QuantumSimulator(circuit.qubits)
    sim_res = sim.simulate_circuit(circuit, shots=1024, record_steps=False)
    actual_probs = sim_res.probabilities

    # 4. Verify Criteria
    verif = challenge["verification"]
    target_probs = verif["target"]
    tolerance = verif.get("tolerance", 0.05)

    # Compute classical fidelity / Bhattacharyya coefficient overlap: sum(sqrt(p_target * p_actual))
    # Or total variation distance: 1 - 0.5 * sum(|p_target - p_actual|)
    all_keys = set(actual_probs.keys()).union(set(target_probs.keys()))
    tvd = 0.0
    for k in all_keys:
        p_act = actual_probs.get(k, 0.0)
        p_tgt = target_probs.get(k, 0.0)
        tvd += abs(p_act - p_tgt)
    tvd *= 0.5

    fidelity = max(0.0, 1.0 - tvd)

    # Criteria check
    passed = True
    details_diff = {}
    for tgt_state, expected_p in target_probs.items():
        actual_p = actual_probs.get(tgt_state, 0.0)
        diff = abs(actual_p - expected_p)
        details_diff[tgt_state] = {"expected": expected_p, "actual": round(actual_p, 4), "diff": round(diff, 4)}
        if diff > tolerance:
            passed = False

    # Check that non-target states with zero expected don't have large amplitude
    for k, actual_p in actual_probs.items():
        if k not in target_probs and actual_p > tolerance:
            passed = False
            details_diff[k] = {"expected": 0.0, "actual": round(actual_p, 4), "diff": round(actual_p, 4)}

    if passed:
        score = challenge["xp"]
        feedback = f"🎉 Outstanding! Challenge Passed with {round(fidelity * 100, 1)}% fidelity. You have unlocked the '{challenge.get('badge', 'Quantum Achiever')}' badge!"
    else:
        score = int(challenge["xp"] * max(0.0, fidelity - 0.2))
        feedback = f"Circuit did not achieve the required target state. Fidelity: {round(fidelity * 100, 1)}%. Check the feedback details and try adjusting your gates."

    return ChallengeSubmissionResponse(
        challenge_id=challenge_id,
        passed=passed,
        fidelity=round(fidelity, 4),
        score=score,
        feedback=feedback,
        details={
            "probabilities": actual_probs,
            "target_comparison": details_diff,
            "total_variation_distance": round(tvd, 4),
            "gate_count": actual_gate_count,
            "badge_earned": challenge.get("badge") if passed else None
        }
    )
