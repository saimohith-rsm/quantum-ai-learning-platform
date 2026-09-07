import sys
import os
import unittest
import numpy as np

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.schemas import CircuitSchema, GateSchema, SimulationRequest
from app.quantum.simulator import QuantumSimulator
from app.quantum.qiskit_export import circuit_to_qiskit, circuit_to_qasm
from app.tutor.ai_tutor import AITutorEngine
from app.challenges.evaluator import evaluate_challenge_submission
from app.database import init_db, SessionLocal
import app.models as models

class TestQuantumBackend(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()

    def test_database_initialization(self):
        """Verify MongoDB database collections and seed data."""
        db = SessionLocal()
        user = db.users.find_one({"username": "quantum_explorer"})
        self.assertIsNotNone(user, "Default user should exist in DB")
        self.assertIn(user.get("level"), ["Beginner", "Intermediate", "Advanced", "Master"])

        circuits = list(db.saved_circuits.find({"user_id": user["id"]}))
        self.assertGreaterEqual(len(circuits), 2, "Default seed circuits should be present")


    def test_hadamard_simulation(self):
        """Verify H gate creates equal superposition and correct Bloch coordinates."""
        circuit = CircuitSchema(
            qubits=1,
            gates=[GateSchema(name="H", target=0, step=0)]
        )
        sim = QuantumSimulator(1)
        res = sim.simulate_circuit(circuit, shots=1000)
        
        # Probabilities
        self.assertAlmostEqual(res.probabilities["0"], 0.5, delta=0.01)
        self.assertAlmostEqual(res.probabilities["1"], 0.5, delta=0.01)

        # Bloch vector for |+> state should be (1, 0, 0)
        bv = res.bloch_vectors[0]
        self.assertAlmostEqual(bv.x, 1.0, delta=0.01)
        self.assertAlmostEqual(bv.y, 0.0, delta=0.01)
        self.assertAlmostEqual(bv.z, 0.0, delta=0.01)

    def test_pauli_x_simulation(self):
        """Verify X gate bit flips |0> to |1> with Bloch vector (0, 0, -1)."""
        circuit = CircuitSchema(
            qubits=1,
            gates=[GateSchema(name="X", target=0, step=0)]
        )
        sim = QuantumSimulator(1)
        res = sim.simulate_circuit(circuit, shots=1000)

        self.assertAlmostEqual(res.probabilities["0"], 0.0, delta=0.01)
        self.assertAlmostEqual(res.probabilities["1"], 1.0, delta=0.01)

        bv = res.bloch_vectors[0]
        self.assertAlmostEqual(bv.z, -1.0, delta=0.01)

    def test_bell_state_entanglement(self):
        """Verify Bell state |Φ+⟩ has 50% |00> and 50% |11>."""
        circuit = CircuitSchema(
            qubits=2,
            gates=[
                GateSchema(name="H", target=0, step=0),
                GateSchema(name="CNOT", control=0, target=1, step=1)
            ]
        )
        sim = QuantumSimulator(2)
        res = sim.simulate_circuit(circuit, shots=1000)

        self.assertAlmostEqual(res.probabilities["00"], 0.5, delta=0.01)
        self.assertAlmostEqual(res.probabilities["11"], 0.5, delta=0.01)
        self.assertAlmostEqual(res.probabilities["01"], 0.0, delta=0.01)
        self.assertAlmostEqual(res.probabilities["10"], 0.0, delta=0.01)

    def test_grover_2qubit_search(self):
        """Verify 2-qubit Grover search yields 100% probability for |11>."""
        circuit = CircuitSchema(
            qubits=2,
            gates=[
                GateSchema(name="H", target=0, step=0),
                GateSchema(name="H", target=1, step=0),
                GateSchema(name="CZ", control=0, target=1, step=1),
                GateSchema(name="H", target=0, step=2),
                GateSchema(name="H", target=1, step=2),
                GateSchema(name="X", target=0, step=3),
                GateSchema(name="X", target=1, step=3),
                GateSchema(name="CZ", control=0, target=1, step=4),
                GateSchema(name="X", target=0, step=5),
                GateSchema(name="X", target=1, step=5),
                GateSchema(name="H", target=0, step=6),
                GateSchema(name="H", target=1, step=6)
            ]
        )
        sim = QuantumSimulator(2)
        res = sim.simulate_circuit(circuit, shots=1000)

        self.assertAlmostEqual(res.probabilities["11"], 1.0, delta=0.01)
        self.assertAlmostEqual(res.probabilities["00"], 0.0, delta=0.01)

    def test_qiskit_and_qasm_export(self):
        """Verify export functions generate non-empty code with proper syntax."""
        circuit = CircuitSchema(
            qubits=2,
            gates=[
                GateSchema(name="H", target=0, step=0),
                GateSchema(name="CNOT", control=0, target=1, step=1)
            ]
        )
        qiskit_code = circuit_to_qiskit(circuit)
        qasm_code = circuit_to_qasm(circuit)

        self.assertIn("qc.h(0)", qiskit_code)
        self.assertIn("qc.cx(0, 1)", qiskit_code)
        self.assertIn("OPENQASM 2.0;", qasm_code)
        self.assertIn("h q[0];", qasm_code)
        self.assertIn("cx q[0],q[1];", qasm_code)

    def test_ai_tutor_bell_explanation(self):
        """Verify AI tutor recognizes the Bell state."""
        circuit = CircuitSchema(
            qubits=2,
            gates=[
                GateSchema(name="H", target=0, step=0),
                GateSchema(name="CNOT", control=0, target=1, step=1)
            ]
        )
        tutor = AITutorEngine()
        resp = tutor.explain_circuit(circuit)

        self.assertIn("Bell State", resp.title)
        self.assertIn("|Φ+⟩", resp.title)
        self.assertGreater(len(resp.key_insights), 0)

    def test_challenge_evaluator_pass_and_fail(self):
        """Verify automated grader correctly scores passing and failing circuits."""
        # Passing Bell State
        pass_circuit = CircuitSchema(
            qubits=2,
            gates=[
                GateSchema(name="H", target=0, step=0),
                GateSchema(name="CNOT", control=0, target=1, step=1)
            ]
        )
        eval_pass = evaluate_challenge_submission("bell_plus", pass_circuit)
        self.assertTrue(eval_pass.passed)
        self.assertGreaterEqual(eval_pass.fidelity, 0.99)
        self.assertEqual(eval_pass.score, 100)

        # Failing Circuit (only Hadamard)
        fail_circuit = CircuitSchema(
            qubits=2,
            gates=[
                GateSchema(name="H", target=0, step=0)
            ]
        )
        eval_fail = evaluate_challenge_submission("bell_plus", fail_circuit)
        self.assertFalse(eval_fail.passed)

if __name__ == "__main__":
    unittest.main()
