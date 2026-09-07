import unittest
import sys
import os

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.schemas import CircuitSchema, GateSchema, TutorChatRequest
from app.quantum.noise import HardwareNoiseModel, NoisyQuantumSimulator
from app.quantum.optimizer import CircuitOptimizer
from app.quantum.protocols import BB84Simulator
from app.quantum.qiskit_export import (
    circuit_to_qiskit,
    circuit_to_cirq,
    circuit_to_pennylane,
    circuit_to_braket,
    circuit_to_qasm,
    export_all_sdks
)
from app.tutor.ai_tutor import AITutorEngine

class TestAdvancedFeatures(unittest.TestCase):

    def setUp(self):
        # Sample Bell circuit: H(0), CNOT(0, 1)
        self.bell_circuit = CircuitSchema(
            qubits=2,
            gates=[
                GateSchema(name="H", target=0, step=0),
                GateSchema(name="CNOT", control=0, target=1, step=1)
            ]
        )

    def test_noise_model_simulation(self):
        """Tests NISQ Hardware Noise Simulation produces valid fidelity and noisy probabilities."""
        noise_model = HardwareNoiseModel.from_preset("ibm_eagle")
        self.assertEqual(noise_model.name, "IBM Quantum Eagle (127Q)")

        noisy_sim = NoisyQuantumSimulator(2, noise_model)
        result = noisy_sim.simulate_with_noise(self.bell_circuit, trajectories=50, shots=500)

        self.assertIn("fidelity", result)
        self.assertIn("quantum_error_rate", result)
        self.assertIn("ideal_probabilities", result)
        self.assertIn("noisy_probabilities", result)
        self.assertIn("noisy_counts", result)

        # Fidelity between 0.0 and 1.0
        self.assertGreaterEqual(result["fidelity"], 0.0)
        self.assertLessEqual(result["fidelity"], 1.0)

        # Ideal Bell probabilities should have |00> and |11> around 0.5
        ideal = result["ideal_probabilities"]
        self.assertAlmostEqual(ideal["00"], 0.5, places=3)
        self.assertAlmostEqual(ideal["11"], 0.5, places=3)

    def test_circuit_optimizer_cancellation(self):
        """Tests that self-cancelling gates (H*H, X*X, adjacent CNOTs) are correctly eliminated."""
        redundant_circuit = CircuitSchema(
            qubits=2,
            gates=[
                GateSchema(name="H", target=0, step=0),
                GateSchema(name="H", target=0, step=1),  # H*H = I
                GateSchema(name="X", target=1, step=0),
                GateSchema(name="X", target=1, step=1),  # X*X = I
                GateSchema(name="CNOT", control=0, target=1, step=2),
                GateSchema(name="CNOT", control=0, target=1, step=3),  # CNOT*CNOT = I
                GateSchema(name="Z", target=0, step=4)   # Kept
            ]
        )

        optimizer = CircuitOptimizer(redundant_circuit)
        opt_res = optimizer.optimize()

        self.assertEqual(opt_res["metrics"]["original_gate_count"], 7)
        self.assertEqual(opt_res["metrics"]["optimized_gate_count"], 1)
        self.assertEqual(opt_res["optimized_circuit"]["gates"][0]["name"], "Z")
        self.assertGreater(opt_res["metrics"]["gate_reduction_pct"], 80.0)

    def test_bb84_qkd_protocol(self):
        """Tests BB84 QKD execution both without Eve and with Eve interception."""
        # 1. No Eve: QBER should be 0%
        bb84_clean = BB84Simulator(num_bits=32, eve_present=False)
        clean_res = bb84_clean.run_protocol()
        self.assertEqual(clean_res["errors_in_sifted_key"], 0)
        self.assertEqual(clean_res["qber_percentage"], 0.0)
        self.assertIn("SECURE", clean_res["channel_status"])
        self.assertEqual(clean_res["alice_sifted_key"], clean_res["bob_sifted_key"])

        # 2. With Eve: Eve disturbs quantum states, QBER should be elevated
        bb84_eve = BB84Simulator(num_bits=48, eve_present=True, eve_intercept_rate=1.0)
        eve_res = bb84_eve.run_protocol()
        self.assertIn("qber_percentage", eve_res)
        self.assertIn("transmission_steps", eve_res)

    def test_multi_sdk_transpilers(self):
        """Tests universal transpiler output for Qiskit, Cirq, PennyLane, Braket, and QASM."""
        sdks = export_all_sdks(self.bell_circuit)

        self.assertIn("QuantumCircuit(2)", sdks["qiskit"])
        self.assertIn("qc.h(0)", sdks["qiskit"])
        self.assertIn("qc.cx(0, 1)", sdks["qiskit"])

        self.assertIn("cirq.H(qubits[0])", sdks["cirq"])
        self.assertIn("cirq.CNOT", sdks["cirq"])

        self.assertIn("qml.Hadamard(wires=0)", sdks["pennylane"])
        self.assertIn("qml.CNOT(wires=[0, 1])", sdks["pennylane"])

        self.assertIn("circuit.h(0)", sdks["braket"])
        self.assertIn("circuit.cnot(0, 1)", sdks["braket"])

        self.assertIn("OPENQASM 2.0;", sdks["qasm"])

    def test_ai_tutor_socratic_and_advanced_topics(self):
        """Tests AI tutor Socratic mode and expanded quantum topics."""
        tutor = AITutorEngine()

        # Teleportation query
        resp_teleport = tutor.answer_chat("How does quantum teleportation work?")
        self.assertIn("Teleportation", resp_teleport.title)

        # BB84 query
        resp_bb84 = tutor.answer_chat("Explain the BB84 QKD protocol.")
        self.assertIn("BB84", resp_bb84.title)

        # Decoherence query
        resp_decoh = tutor.answer_chat("What is T1 and T2 decoherence?")
        self.assertIn("Decoherence", resp_decoh.title)

        # Socratic mode greeting
        resp_socratic = tutor.answer_chat("Help me learn", socratic_mode=True)
        self.assertIn("Socratic", resp_socratic.title)

if __name__ == "__main__":
    unittest.main()
