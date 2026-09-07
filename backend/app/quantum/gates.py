import numpy as np

# Single-Qubit Standard Matrices
I2 = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=complex)
X_GATE = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
Y_GATE = np.array([[0.0, -1.0j], [1.0j, 0.0]], dtype=complex)
Z_GATE = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)
H_GATE = (1.0 / np.sqrt(2.0)) * np.array([[1.0, 1.0], [1.0, -1.0]], dtype=complex)
S_GATE = np.array([[1.0, 0.0], [0.0, 1.0j]], dtype=complex)
SDG_GATE = np.array([[1.0, 0.0], [0.0, -1.0j]], dtype=complex)
T_GATE = np.array([[1.0, 0.0], [0.0, np.exp(1.0j * np.pi / 4.0)]], dtype=complex)
TDG_GATE = np.array([[1.0, 0.0], [0.0, np.exp(-1.0j * np.pi / 4.0)]], dtype=complex)

def rx_gate(theta: float) -> np.ndarray:
    half = theta / 2.0
    return np.array([
        [np.cos(half), -1.0j * np.sin(half)],
        [-1.0j * np.sin(half), np.cos(half)]
    ], dtype=complex)

def ry_gate(theta: float) -> np.ndarray:
    half = theta / 2.0
    return np.array([
        [np.cos(half), -np.sin(half)],
        [np.sin(half), np.cos(half)]
    ], dtype=complex)

def rz_gate(theta: float) -> np.ndarray:
    half = theta / 2.0
    return np.array([
        [np.exp(-1.0j * half), 0.0],
        [0.0, np.exp(1.0j * half)]
    ], dtype=complex)

def phase_gate(phi: float) -> np.ndarray:
    return np.array([
        [1.0, 0.0],
        [0.0, np.exp(1.0j * phi)]
    ], dtype=complex)

def get_single_qubit_matrix(name: str, params: dict = None) -> np.ndarray:
    name_upper = name.upper()
    params = params or {}
    if name_upper == "H":
        return H_GATE
    elif name_upper == "X":
        return X_GATE
    elif name_upper == "Y":
        return Y_GATE
    elif name_upper == "Z":
        return Z_GATE
    elif name_upper == "S":
        return S_GATE
    elif name_upper in ("S_DAG", "SDG"):
        return SDG_GATE
    elif name_upper == "T":
        return T_GATE
    elif name_upper in ("T_DAG", "TDG"):
        return TDG_GATE
    elif name_upper == "RX":
        theta = float(params.get("theta", np.pi))
        return rx_gate(theta)
    elif name_upper == "RY":
        theta = float(params.get("theta", np.pi))
        return ry_gate(theta)
    elif name_upper == "RZ":
        theta = float(params.get("theta", np.pi))
        return rz_gate(theta)
    elif name_upper in ("P", "PHASE"):
        phi = float(params.get("phi", np.pi / 2.0))
        return phase_gate(phi)
    elif name_upper == "I":
        return I2
    else:
        raise ValueError(f"Unknown single-qubit gate: {name}")

def apply_single_qubit_gate(state_tensor: np.ndarray, gate_matrix: np.ndarray, target: int) -> np.ndarray:
    """
    Applies single-qubit gate U on target qubit axis in state tensor of shape (2,)*n.
    """
    contracted = np.tensordot(gate_matrix, state_tensor, axes=([1], [target]))
    return np.moveaxis(contracted, 0, target)

def apply_cnot_gate(state_tensor: np.ndarray, control: int, target: int) -> np.ndarray:
    """
    Applies CNOT (CX) where control qubit toggles Pauli X on target qubit.
    """
    # Create slicing where control qubit is |1>
    num_qubits = state_tensor.ndim
    idx_one = [slice(None)] * num_qubits
    idx_one[control] = 1

    sub_tensor = state_tensor[tuple(idx_one)]
    # Target qubit index in sub_tensor is adjusted if target > control
    sub_target = target - 1 if target > control else target

    # Apply X gate on target in this subspace
    updated_sub = np.tensordot(X_GATE, sub_tensor, axes=([1], [sub_target]))
    updated_sub = np.moveaxis(updated_sub, 0, sub_target)

    # Assign back
    out = state_tensor.copy()
    out[tuple(idx_one)] = updated_sub
    return out

def apply_cz_gate(state_tensor: np.ndarray, control: int, target: int) -> np.ndarray:
    """
    Applies Controlled-Z (CZ) which negates state when both control and target are |1>.
    """
    num_qubits = state_tensor.ndim
    idx_both = [slice(None)] * num_qubits
    idx_both[control] = 1
    idx_both[target] = 1

    out = state_tensor.copy()
    out[tuple(idx_both)] = -1.0 * out[tuple(idx_both)]
    return out

def apply_swap_gate(state_tensor: np.ndarray, qubit_a: int, qubit_b: int) -> np.ndarray:
    """
    Applies SWAP gate between qubit_a and qubit_b.
    """
    return np.swapaxes(state_tensor, qubit_a, qubit_b)

def apply_toffoli_gate(state_tensor: np.ndarray, control1: int, control2: int, target: int) -> np.ndarray:
    """
    Applies Toffoli (CCX) gate where target is flipped if control1 == 1 and control2 == 1.
    """
    num_qubits = state_tensor.ndim
    idx = [slice(None)] * num_qubits
    idx[control1] = 1
    idx[control2] = 1

    sub = state_tensor[tuple(idx)]
    # Target index in sub-tensor (which has 2 fewer dimensions)
    removed_before = sum([1 for c in (control1, control2) if c < target])
    sub_target = target - removed_before

    updated_sub = np.tensordot(X_GATE, sub, axes=([1], [sub_target]))
    updated_sub = np.moveaxis(updated_sub, 0, sub_target)

    out = state_tensor.copy()
    out[tuple(idx)] = updated_sub
    return out

def apply_controlled_phase(state_tensor: np.ndarray, control: int, target: int, phi: float) -> np.ndarray:
    """
    Applies Controlled-Phase gate: multiplies phase exp(i*phi) when both are |1>.
    """
    num_qubits = state_tensor.ndim
    idx_both = [slice(None)] * num_qubits
    idx_both[control] = 1
    idx_both[target] = 1

    out = state_tensor.copy()
    out[tuple(idx_both)] = np.exp(1.0j * phi) * out[tuple(idx_both)]
    return out
