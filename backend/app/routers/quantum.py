from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.schemas import (
    SimulationRequest,
    SimulationResponse,
    CircuitSchema,
    CircuitOptimizeRequest,
    CircuitOptimizeResponse,
    NoisySimulationRequest,
    NoisySimulationResponse,
    MultiSdkExportRequest,
    MultiSdkExportResponse,
    BB84Request
)
from app.quantum.simulator import QuantumSimulator
from app.quantum.noise import HardwareNoiseModel, NoisyQuantumSimulator
from app.quantum.optimizer import CircuitOptimizer
from app.quantum.protocols import BB84Simulator
from app.quantum.qiskit_export import (
    circuit_to_qiskit,
    circuit_to_qasm,
    circuit_to_cirq,
    circuit_to_pennylane,
    circuit_to_braket,
    export_all_sdks
)
from app.quantum.presets import PRESET_ALGORITHMS, get_preset_by_id

router = APIRouter(prefix="/api/quantum", tags=["Quantum Engine"])

@router.post("/simulate", response_model=SimulationResponse)
def simulate_quantum_circuit(req: SimulationRequest):
    """
    Executes mathematically exact statevector simulation of the provided quantum circuit.
    """
    try:
        sim = QuantumSimulator(req.circuit.qubits)
        result = sim.simulate_circuit(
            circuit=req.circuit,
            shots=req.shots,
            record_steps=req.calculate_steps
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/optimize", response_model=CircuitOptimizeResponse)
def optimize_circuit(req: CircuitOptimizeRequest):
    """
    Applies algebraic gate cancellation, rotation merging, and timeline compaction
    to minimize quantum circuit depth and gate count.
    """
    try:
        optimizer = CircuitOptimizer(req.circuit)
        result = optimizer.optimize()
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/simulate-noisy", response_model=NoisySimulationResponse)
def simulate_noisy_circuit(req: NoisySimulationRequest):
    """
    Simulates real-world NISQ hardware noise:
    - T1 Energy Relaxation (|1> -> |0> decay)
    - T2 Phase Dephasing
    - 1-qubit & 2-qubit stochastic Pauli depolarizing gate errors
    - Readout SPAM measurement errors
    - State Fidelity against ideal noiseless circuit
    """
    try:
        if req.t1_prob is not None or req.t2_prob is not None:
            noise_model = HardwareNoiseModel(
                t1_prob=req.t1_prob if req.t1_prob is not None else 0.02,
                t2_prob=req.t2_prob if req.t2_prob is not None else 0.04,
                gate_error=req.gate_error if req.gate_error is not None else 0.002,
                cnot_error=req.cnot_error if req.cnot_error is not None else 0.015,
                readout_error=req.readout_error if req.readout_error is not None else 0.02,
                name="Custom User Hardware Profile"
            )
        else:
            preset = req.hardware_preset or "ibm_eagle"
            noise_model = HardwareNoiseModel.from_preset(preset)

        noisy_sim = NoisyQuantumSimulator(req.circuit.qubits, noise_model)
        result = noisy_sim.simulate_with_noise(
            circuit=req.circuit,
            trajectories=req.trajectories,
            shots=req.shots
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/export-multisdk", response_model=MultiSdkExportResponse)
def export_multisdk(req: MultiSdkExportRequest):
    """
    Universal Transpiler: exports visual quantum circuits to:
    - IBM Qiskit 1.0+
    - Google Cirq
    - PennyLane (QML)
    - Amazon Braket SDK
    - OpenQASM 2.0 / 3.0
    """
    try:
        codes = export_all_sdks(req.circuit)
        return MultiSdkExportResponse(**codes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/export/qiskit")
def export_to_qiskit(circuit: CircuitSchema):
    """Generates runnable IBM Qiskit 1.0+ Python code for the circuit."""
    try:
        code = circuit_to_qiskit(circuit)
        return {"language": "python", "framework": "qiskit", "code": code}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/export/qasm")
def export_to_qasm(circuit: CircuitSchema):
    """Generates standard OpenQASM 2.0 code for the circuit."""
    try:
        qasm = circuit_to_qasm(circuit)
        return {"format": "openqasm", "version": "2.0", "qasm": qasm}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/protocol/bb84")
def run_bb84_qkd_simulation(req: BB84Request):
    """
    Runs an interactive BB84 Quantum Key Distribution (QKD) protocol simulation.
    Demonstrates Alice bit generation, photon polarization bases, optional Eve interception,
    Bob measurement, public sifting, and Quantum Bit Error Rate (QBER) detection.
    """
    try:
        sim = BB84Simulator(
            num_bits=req.num_bits,
            eve_present=req.eve_present,
            eve_intercept_rate=req.eve_intercept_rate
        )
        return sim.run_protocol()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/presets")
def list_preset_algorithms():
    """Lists pre-built quantum algorithm presets (Bell State, Grover, Deutsch-Jozsa, QFT, Teleportation, etc.)."""
    return PRESET_ALGORITHMS

@router.get("/presets/{preset_id}")
def get_preset_algorithm(preset_id: str):
    """Returns a specific pre-built quantum algorithm circuit definition."""
    preset = get_preset_by_id(preset_id)
    if not preset:
        raise HTTPException(status_code=404, detail=f"Preset '{preset_id}' not found")
    return preset
