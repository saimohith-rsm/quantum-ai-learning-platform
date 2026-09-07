import React, { createContext, useContext, useState, useEffect } from 'react';
import { 
  simulateCircuit, 
  getUserProfile, 
  getPresets, 
  loginUser, 
  registerUser, 
  demoLogin, 
  getMe, 
  setStoredToken, 
  getStoredToken 
} from '../services/api';

const QuantumContext = createContext();

export function QuantumProvider({ children }) {
  // Circuit state: default to 2 qubits with a Bell State
  const [circuit, setCircuit] = useState({
    qubits: 2,
    gates: [
      { name: 'H', target: 0, step: 0 },
      { name: 'CNOT', control: 0, target: 1, step: 1 }
    ]
  });

  const [simulationResult, setSimulationResult] = useState(null);
  const [activeStepIndex, setActiveStepIndex] = useState(null); // null = final state, or number 0..steps.length-1
  const [selectedQubit, setSelectedQubit] = useState(0);
  const [activeTab, setActiveTab] = useState('studio'); // 'studio' | 'lessons' | 'challenges' | 'saved'
  const [userProfile, setUserProfile] = useState(null);
  const [currentUser, setCurrentUser] = useState(null);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [presets, setPresets] = useState([]);
  const [isSimulating, setIsSimulating] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);

  // Initialize Authentication & Profile
  useEffect(() => {
    initAuth();
    getPresets()
      .then(data => setPresets(data))
      .catch(err => console.warn('Could not load presets:', err));
  }, []);

  const initAuth = async () => {
    const token = getStoredToken();
    if (token) {
      try {
        const user = await getMe(token);
        if (user) {
          setCurrentUser(user);
          setUserProfile(user);
          return;
        }
      } catch (e) {
        console.warn('Session expired:', e);
      }
    }
    // Fallback: auto-login as demo user
    try {
      const res = await demoLogin();
      setStoredToken(res.token);
      setCurrentUser(res.user);
      setUserProfile(res.user);
    } catch (e) {
      console.warn('Auto demo login failed:', e);
    }
  };

  const login = async (username, password) => {
    const res = await loginUser({ username, password });
    setStoredToken(res.token);
    setCurrentUser(res.user);
    setUserProfile(res.user);
    setIsAuthModalOpen(false);
    return res;
  };

  const register = async (userData) => {
    const res = await registerUser(userData);
    setStoredToken(res.token);
    setCurrentUser(res.user);
    setUserProfile(res.user);
    setIsAuthModalOpen(false);
    return res;
  };

  const quickDemoLogin = async () => {
    const res = await demoLogin();
    setStoredToken(res.token);
    setCurrentUser(res.user);
    setUserProfile(res.user);
    setIsAuthModalOpen(false);
    return res;
  };

  const logout = () => {
    setStoredToken(null);
    setCurrentUser(null);
    setUserProfile(null);
    quickDemoLogin(); // Revert to guest demo session
  };

  // Auto-simulate on initial mount
  useEffect(() => {
    runSimulation(circuit);
  }, []);

  const refreshProfile = async () => {
    const token = getStoredToken();
    if (token) {
      try {
        const p = await getMe(token);
        if (p) {
          setCurrentUser(p);
          setUserProfile(p);
          return;
        }
      } catch (err) {
        console.warn('Could not refresh profile:', err);
      }
    }
    try {
      const p = await getUserProfile(currentUser?.id || 1);
      setUserProfile(p);
    } catch (err) {
      console.warn('Could not load user profile:', err);
    }
  };

  const runSimulation = async (circToSim = circuit) => {
    setIsSimulating(true);
    setErrorMsg(null);
    try {
      const res = await simulateCircuit(circToSim, 1024, true);
      setSimulationResult(res);
      // Reset scrubber to final state
      setActiveStepIndex(null);
    } catch (err) {
      console.error('Simulation error:', err);
      setErrorMsg(err.message || 'Simulation error');
    } finally {
      setIsSimulating(false);
    }
  };

  const setQubits = (num) => {
    const valid = Math.max(1, Math.min(6, num));
    const filteredGates = circuit.gates.filter(g => 
      g.target < valid && (g.control === undefined || g.control < valid)
    );
    const newCircuit = { qubits: valid, gates: filteredGates };
    setCircuit(newCircuit);
    if (selectedQubit >= valid) setSelectedQubit(0);
    runSimulation(newCircuit);
  };

  const addGate = (gate) => {
    const existingIndex = circuit.gates.findIndex(
      g => g.target === gate.target && g.step === gate.step
    );
    let newGates = [...circuit.gates];
    if (existingIndex >= 0) {
      newGates[existingIndex] = gate;
    } else {
      newGates.push(gate);
    }
    const newCircuit = { ...circuit, gates: newGates };
    setCircuit(newCircuit);
    runSimulation(newCircuit);
  };

  const removeGate = (index) => {
    const newGates = circuit.gates.filter((_, i) => i !== index);
    const newCircuit = { ...circuit, gates: newGates };
    setCircuit(newCircuit);
    runSimulation(newCircuit);
  };

  const clearCircuit = () => {
    const newCircuit = { qubits: circuit.qubits, gates: [] };
    setCircuit(newCircuit);
    runSimulation(newCircuit);
  };

  const loadPreset = (preset) => {
    const newCircuit = {
      qubits: preset.qubits,
      gates: preset.gates
    };
    setCircuit(newCircuit);
    if (selectedQubit >= preset.qubits) setSelectedQubit(0);
    runSimulation(newCircuit);
  };

  const loadCircuit = (circuitObj) => {
    setCircuit(circuitObj);
    if (selectedQubit >= circuitObj.qubits) setSelectedQubit(0);
    runSimulation(circuitObj);
  };

  const currentStepData = () => {
    if (!simulationResult) return null;
    if (activeStepIndex === null || activeStepIndex >= simulationResult.steps.length) {
      return {
        statevector: simulationResult.statevector,
        probabilities: simulationResult.probabilities,
        bloch_vectors: simulationResult.bloch_vectors,
        isFinal: true
      };
    }
    const step = simulationResult.steps[activeStepIndex];
    return {
      statevector: step.statevector,
      probabilities: step.probabilities,
      bloch_vectors: step.bloch_vectors,
      gateApplied: step.gate_applied,
      isFinal: false
    };
  };

  return (
    <QuantumContext.Provider value={{
      circuit,
      simulationResult,
      activeStepIndex,
      setActiveStepIndex,
      selectedQubit,
      setSelectedQubit,
      activeTab,
      setActiveTab,
      userProfile,
      currentUser,
      isAuthModalOpen,
      setIsAuthModalOpen,
      login,
      register,
      quickDemoLogin,
      logout,
      refreshProfile,
      presets,
      isSimulating,
      errorMsg,
      setQubits,
      addGate,
      removeGate,
      clearCircuit,
      loadPreset,
      loadCircuit,
      runSimulation,
      currentStepData
    }}>
      {children}
    </QuantumContext.Provider>
  );
}

export function useQuantum() {
  return useContext(QuantumContext);
}
