import sys
import os
import unittest
from fastapi.testclient import TestClient

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app
from app.database import init_db

class TestAPIEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()
        cls.client = TestClient(app)

    def test_root_and_health(self):
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "online")
        self.assertEqual(data["problem_statement_id"], "26140")
        self.assertEqual(data["team_name"], "Human X")

        health = self.client.get("/api/health")
        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.json()["status"], "healthy")

    def test_simulation_endpoint(self):
        payload = {
            "circuit": {
                "qubits": 2,
                "gates": [
                    {"name": "H", "target": 0, "step": 0},
                    {"name": "CNOT", "control": 0, "target": 1, "step": 1}
                ]
            },
            "shots": 500,
            "calculate_steps": True
        }
        resp = self.client.post("/api/quantum/simulate", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["num_qubits"], 2)
        self.assertIn("00", data["probabilities"])
        self.assertIn("11", data["probabilities"])
        self.assertAlmostEqual(data["probabilities"]["00"], 0.5, delta=0.01)
        self.assertAlmostEqual(data["probabilities"]["11"], 0.5, delta=0.01)
        self.assertEqual(len(data["bloch_vectors"]), 2)
        self.assertIn("qc.h(0)", data["qiskit_code"])

    def test_export_endpoints(self):
        payload = {
            "qubits": 2,
            "gates": [
                {"name": "H", "target": 0, "step": 0},
                {"name": "CNOT", "control": 0, "target": 1, "step": 1}
            ]
        }
        qiskit_resp = self.client.post("/api/quantum/export/qiskit", json=payload)
        self.assertEqual(qiskit_resp.status_code, 200)
        self.assertIn("from qiskit import QuantumCircuit", qiskit_resp.json()["code"])

        qasm_resp = self.client.post("/api/quantum/export/qasm", json=payload)
        self.assertEqual(qasm_resp.status_code, 200)
        self.assertIn("OPENQASM 2.0;", qasm_resp.json()["qasm"])

    def test_presets_endpoints(self):
        resp = self.client.get("/api/quantum/presets")
        self.assertEqual(resp.status_code, 200)
        presets = resp.json()
        self.assertGreaterEqual(len(presets), 6)

        single = self.client.get("/api/quantum/presets/grover_2qubit")
        self.assertEqual(single.status_code, 200)
        self.assertEqual(single.json()["id"], "grover_2qubit")

    def test_tutor_explain_endpoint(self):
        payload = {
            "circuit": {
                "qubits": 2,
                "gates": [
                    {"name": "H", "target": 0, "step": 0},
                    {"name": "CNOT", "control": 0, "target": 1, "step": 1}
                ]
            },
            "user_level": "Beginner"
        }
        resp = self.client.post("/api/tutor/explain", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("Bell State", data["title"])

    def test_curriculum_endpoints(self):
        resp = self.client.get("/api/curriculum/modules")
        self.assertEqual(resp.status_code, 200)
        modules = resp.json()
        self.assertGreaterEqual(len(modules), 3)

        lesson_resp = self.client.get("/api/curriculum/lessons/lesson_1_1")
        self.assertEqual(lesson_resp.status_code, 200)
        self.assertIn("Classical Bits vs Quantum Qubits", lesson_resp.json()["title"])

    def test_challenges_and_submit_endpoint(self):
        list_resp = self.client.get("/api/challenges")
        self.assertEqual(list_resp.status_code, 200)
        self.assertGreaterEqual(len(list_resp.json()), 4)

        submit_payload = {
            "challenge_id": "bell_plus",
            "circuit": {
                "qubits": 2,
                "gates": [
                    {"name": "H", "target": 0, "step": 0},
                    {"name": "CNOT", "control": 0, "target": 1, "step": 1}
                ]
            },
            "user_id": 1
        }
        sub_resp = self.client.post("/api/challenges/bell_plus/submit", json=submit_payload)
        self.assertEqual(sub_resp.status_code, 200)
        data = sub_resp.json()
        self.assertTrue(data["passed"])
        self.assertGreaterEqual(data["fidelity"], 0.99)

    def test_database_crud_saved_circuits(self):
        save_payload = {
            "name": "Custom Test Circuit",
            "description": "Created during integration test",
            "num_qubits": 2,
            "circuit_json": '{"qubits": 2, "gates": [{"name": "X", "target": 0, "step": 0}]}',
            "is_public": True
        }
        create_resp = self.client.post("/api/circuits/saved?user_id=1", json=save_payload)
        self.assertEqual(create_resp.status_code, 200)
        created_id = create_resp.json()["id"]

        get_resp = self.client.get(f"/api/circuits/saved/{created_id}")
        self.assertEqual(get_resp.status_code, 200)
        self.assertEqual(get_resp.json()["name"], "Custom Test Circuit")

        del_resp = self.client.delete(f"/api/circuits/saved/{created_id}?user_id=1")
        self.assertEqual(del_resp.status_code, 200)

    def test_auth_endpoints(self):
        # 1. Demo login
        demo_resp = self.client.post("/api/auth/demo-login")
        self.assertEqual(demo_resp.status_code, 200)
        data = demo_resp.json()
        self.assertIn("token", data)
        self.assertEqual(data["user"]["username"], "quantum_explorer")

        import uuid
        test_user = f"ada_{uuid.uuid4().hex[:8]}"
        reg_payload = {
            "username": test_user,
            "password": "analytical_engine",
            "email": f"{test_user}@quantum.test",
            "display_name": "Ada Lovelace"
        }
        reg_resp = self.client.post("/api/auth/register", json=reg_payload)
        self.assertEqual(reg_resp.status_code, 200)
        reg_data = reg_resp.json()
        token = reg_data["token"]
        self.assertEqual(reg_data["user"]["username"], test_user)

        # 3. Login with correct credentials
        login_payload = {
            "username": test_user,
            "password": "analytical_engine"
        }
        login_resp = self.client.post("/api/auth/login", json=login_payload)
        self.assertEqual(login_resp.status_code, 200)

        # 4. Login with wrong password
        bad_login = self.client.post("/api/auth/login", json={"username": test_user, "password": "wrong"})
        self.assertEqual(bad_login.status_code, 401)

        # 5. Get profile with Bearer token
        me_resp = self.client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(me_resp.status_code, 200)
        self.assertEqual(me_resp.json()["username"], test_user)

    def test_security_headers(self):
        resp = self.client.get("/api/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers.get("x-content-type-options"), "nosniff")
        self.assertEqual(resp.headers.get("x-frame-options"), "DENY")
        self.assertEqual(resp.headers.get("referrer-policy"), "strict-origin-when-cross-origin")

    def test_unauthorized_access(self):
        # Missing token
        resp = self.client.get("/api/auth/me")
        self.assertEqual(resp.status_code, 401)

        # Invalid token
        resp2 = self.client.get("/api/auth/me", headers={"Authorization": "Bearer invalid.token.signature"})
        self.assertEqual(resp2.status_code, 401)

    def test_invalid_circuit_handling(self):
        # Invalid qubits range (> 8 or < 1)
        bad_payload = {
            "circuit": {
                "qubits": 99,
                "gates": []
            },
            "shots": 100
        }
        resp = self.client.post("/api/quantum/simulate", json=bad_payload)
        self.assertEqual(resp.status_code, 422)

if __name__ == "__main__":
    unittest.main()
