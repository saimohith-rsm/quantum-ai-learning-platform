import React, { useState, useEffect } from 'react';
import { useQuantum } from '../context/QuantumContext';
import { optimizeCircuit, simulateNoisyCircuit } from '../services/api';
import { 
  Play, RotateCcw, Trash2, Plus, Minus, Download, 
  Sparkles, Save, ChevronRight, ChevronLeft, Pause,
  Zap, Activity, CheckCircle2, ShieldCheck, X
} from 'lucide-react';

const GATE_PALETTE = [
  { name: 'H', label: 'H', type: 'single', desc: 'Hadamard (Superposition)', color: 'from-cyan-500 to-blue-600' },
  { name: 'X', label: 'X', type: 'single', desc: 'Pauli-X (Bit-flip)', color: 'from-amber-500 to-rose-600' },
  { name: 'Y', label: 'Y', type: 'single', desc: 'Pauli-Y', color: 'from-emerald-500 to-teal-600' },
  { name: 'Z', label: 'Z', type: 'single', desc: 'Pauli-Z (Phase-flip)', color: 'from-purple-500 to-indigo-600' },
  { name: 'S', label: 'S', type: 'single', desc: 'Phase Gate (π/2)', color: 'from-violet-500 to-purple-600' },
  { name: 'T', label: 'T', type: 'single', desc: 'π/8 Gate', color: 'from-pink-500 to-rose-600' },
  { name: 'CNOT', label: 'CX', type: 'two_qubit', desc: 'Controlled-NOT', color: 'from-sky-500 to-indigo-600' },
  { name: 'CZ', label: 'CZ', type: 'two_qubit', desc: 'Controlled-Z', color: 'from-indigo-500 to-purple-700' },
  { name: 'SWAP', label: 'SWAP', type: 'two_qubit', desc: 'Swap 2 Qubits', color: 'from-teal-500 to-cyan-700' },
  { name: 'CCX', label: 'CCX', type: 'three_qubit', desc: 'Toffoli (3-qubit)', color: 'from-fuchsia-600 to-pink-700' },
  { name: 'MEASURE', label: 'M', type: 'single', desc: 'Measurement', color: 'from-slate-600 to-slate-800' }
];

const MAX_STEPS = 10;

export default function CircuitBuilder({ onOpenExport, onOpenPresets, onOpenSave }) {
  const {
    circuit,
    setQubits,
    addGate,
    removeGate,
    clearCircuit,
    loadCircuit,
    runSimulation,
    simulationResult,
    activeStepIndex,
    setActiveStepIndex,
    isSimulating
  } = useQuantum();

  const [selectedPaletteGate, setSelectedPaletteGate] = useState('H');
  const [controlQubit, setControlQubit] = useState(0);
  const [control2Qubit, setControl2Qubit] = useState(1);
  const [isPlayingSteps, setIsPlayingSteps] = useState(false);

  // Advanced SIH 2026 States: Optimizer & NISQ Hardware Noise
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [optReport, setOptReport] = useState(null);
  const [showNoiseDrawer, setShowNoiseDrawer] = useState(false);
  const [noisePreset, setNoisePreset] = useState('ibm_eagle');
  const [noiseResult, setNoiseResult] = useState(null);
  const [isSimulatingNoise, setIsSimulatingNoise] = useState(false);

  // Auto step-player effect
  useEffect(() => {
    let interval;
    if (isPlayingSteps && simulationResult?.steps) {
      interval = setInterval(() => {
        setActiveStepIndex((prev) => {
          if (prev === null) return 0;
          if (prev >= simulationResult.steps.length - 1) {
            setIsPlayingSteps(false);
            return null;
          }
          return prev + 1;
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isPlayingSteps, simulationResult]);

  const handleCellClick = (qIdx, stepIdx) => {
    const gateIndex = circuit.gates.findIndex(
      g => (g.target === qIdx || (g.control === qIdx && ['CNOT', 'CX', 'CZ', 'SWAP'].includes(g.name))) && g.step === stepIdx
    );

    if (gateIndex >= 0) {
      removeGate(gateIndex);
      return;
    }

    const gateDef = GATE_PALETTE.find(g => g.name === selectedPaletteGate);
    if (!gateDef) return;

    if (gateDef.type === 'single') {
      addGate({ name: selectedPaletteGate, target: qIdx, step: stepIdx });
    } else if (gateDef.type === 'two_qubit') {
      const ctrl = controlQubit === qIdx ? (qIdx === 0 ? 1 : 0) : controlQubit;
      addGate({ name: selectedPaletteGate, control: ctrl, target: qIdx, step: stepIdx });
    } else if (gateDef.type === 'three_qubit') {
      const c1 = controlQubit === qIdx ? (qIdx === 0 ? 1 : 0) : controlQubit;
      let c2 = control2Qubit === qIdx || control2Qubit === c1 ? (c1 === 1 ? 2 : 1) : control2Qubit;
      addGate({ name: 'CCX', control: c1, control2: c2, target: qIdx, step: stepIdx });
    }
  };

  const handleOptimize = async () => {
    setIsOptimizing(true);
    try {
      const res = await optimizeCircuit(circuit);
      setOptReport(res);
      if (loadCircuit) {
        loadCircuit(res.optimized_circuit);
      }
    } catch (err) {
      console.error('Optimization error:', err);
    } finally {
      setIsOptimizing(false);
    }
  };

  const handleRunNoisySim = async () => {
    setIsSimulatingNoise(true);
    try {
      const res = await simulateNoisyCircuit(circuit, noisePreset);
      setNoiseResult(res);
    } catch (err) {
      console.error('Noisy simulation error:', err);
    } finally {
      setIsSimulatingNoise(false);
    }
  };

  const activeGateCount = circuit.gates.length;
  const currentStep = activeStepIndex === null ? 'Final State' : `Step ${activeStepIndex} / ${simulationResult?.steps?.length - 1 || 0}`;

  return (
    <div className="bg-[#0b1329] border border-cyan-500/20 rounded-2xl p-5 shadow-xl flex flex-col gap-4">
      {/* Top Toolbar */}
      <div className="flex flex-wrap items-center justify-between gap-3 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2 bg-slate-900 px-3 py-1.5 rounded-xl border border-slate-800">
            <span className="text-xs text-slate-400 font-medium">Qubits:</span>
            <button
              onClick={() => setQubits(circuit.qubits - 1)}
              disabled={circuit.qubits <= 1}
              className="p-1 rounded bg-slate-800 hover:bg-slate-700 disabled:opacity-30 text-slate-200"
            >
              <Minus className="w-3.5 h-3.5" />
            </button>
            <span className="text-sm font-mono font-bold text-cyan-400 px-1">{circuit.qubits}</span>
            <button
              onClick={() => setQubits(circuit.qubits + 1)}
              disabled={circuit.qubits >= 6}
              className="p-1 rounded bg-slate-800 hover:bg-slate-700 disabled:opacity-30 text-slate-200"
            >
              <Plus className="w-3.5 h-3.5" />
            </button>
          </div>

          <button
            onClick={onOpenPresets}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-purple-500/10 hover:bg-purple-500/20 border border-purple-500/30 text-purple-300 text-xs font-medium transition"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Presets</span>
          </button>

          {/* ⚡ Optimizer Button */}
          <button
            onClick={handleOptimize}
            disabled={isOptimizing || circuit.gates.length === 0}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-amber-500/15 hover:bg-amber-500/25 border border-amber-500/30 text-amber-300 text-xs font-semibold transition disabled:opacity-40"
            title="Algebraic gate cancellation, rotation merging, and timeline depth compaction"
          >
            <Zap className={`w-3.5 h-3.5 ${isOptimizing ? 'animate-bounce' : ''}`} />
            <span>{isOptimizing ? 'Compiling...' : 'Optimize'}</span>
          </button>

          {/* 🔬 NISQ Hardware Noise Button */}
          <button
            onClick={() => {
              setShowNoiseDrawer(!showNoiseDrawer);
              if (!showNoiseDrawer && !noiseResult) handleRunNoisySim();
            }}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl border text-xs font-semibold transition ${
              showNoiseDrawer
                ? 'bg-rose-500/20 border-rose-500/50 text-rose-300'
                : 'bg-rose-500/10 hover:bg-rose-500/20 border-rose-500/30 text-rose-400'
            }`}
          >
            <Activity className="w-3.5 h-3.5" />
            <span>NISQ Hardware</span>
            {noiseResult && (
              <span className="ml-1 px-1.5 py-0.2 rounded-full bg-rose-500/30 text-[10px] font-mono font-bold">
                F: {Math.round(noiseResult.fidelity * 100)}%
              </span>
            )}
          </button>
        </div>

        {/* Action buttons */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => runSimulation()}
            disabled={isSimulating}
            className="flex items-center gap-1.5 px-4 py-1.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold text-xs shadow-lg shadow-cyan-500/25 transition disabled:opacity-50"
          >
            <Play className={`w-3.5 h-3.5 ${isSimulating ? 'animate-spin' : ''}`} />
            <span>{isSimulating ? 'Simulating...' : 'Simulate'}</span>
          </button>

          <button
            onClick={clearCircuit}
            className="p-2 rounded-xl bg-slate-900 hover:bg-rose-500/20 text-slate-400 hover:text-rose-300 border border-slate-800 transition"
            title="Clear Circuit"
          >
            <Trash2 className="w-4 h-4" />
          </button>

          <button
            onClick={onOpenSave}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 text-xs transition"
          >
            <Save className="w-3.5 h-3.5 text-cyan-400" />
            <span>Save</span>
          </button>

          <button
            onClick={onOpenExport}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-300 text-xs transition"
          >
            <Download className="w-3.5 h-3.5 text-purple-400" />
            <span>Multi-SDK Export</span>
          </button>
        </div>
      </div>

      {/* Optimizer Report Banner */}
      {optReport && (
        <div className="p-3 bg-amber-500/10 border border-amber-500/30 rounded-xl flex items-start justify-between gap-3 text-xs">
          <div className="flex items-start gap-2.5">
            <Zap className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
            <div>
              <div className="font-bold text-amber-300 flex items-center gap-2">
                <span>Circuit Optimized</span>
                <span className="px-2 py-0.5 rounded-md bg-amber-500/20 font-mono text-[10px]">
                  Gates: {optReport.metrics.original_gate_count} → {optReport.metrics.optimized_gate_count} (-{optReport.metrics.gate_reduction_pct}%)
                </span>
                <span className="px-2 py-0.5 rounded-md bg-amber-500/20 font-mono text-[10px]">
                  Depth: {optReport.metrics.original_depth} → {optReport.metrics.optimized_depth} (-{optReport.metrics.depth_reduction_pct}%)
                </span>
                <span className="px-2 py-0.5 rounded-md bg-amber-500/20 font-mono text-[10px]">
                  CNOTs: {optReport.metrics.cnot_count} | T-Count: {optReport.metrics.t_count}
                </span>
              </div>
              <p className="text-slate-300 text-[11px] mt-1">
                {optReport.optimizations_applied.join(' • ')}
              </p>
            </div>
          </div>
          <button
            onClick={() => setOptReport(null)}
            className="text-slate-400 hover:text-white p-1 rounded"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {/* NISQ Noise Simulation Panel Drawer */}
      {showNoiseDrawer && (
        <div className="p-4 bg-rose-500/10 border border-rose-500/30 rounded-xl flex flex-col gap-3 text-xs">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <Activity className="w-4 h-4 text-rose-400" />
              <span className="font-bold text-rose-200">NISQ Hardware Imperfection Model</span>
              <span className="text-slate-400 text-[11px]">(T1 decay, T2 dephasing, gate depolarizing & readout error)</span>
            </div>

            <div className="flex items-center gap-2">
              <select
                value={noisePreset}
                onChange={(e) => setNoisePreset(e.target.value)}
                className="bg-slate-900 border border-rose-500/40 rounded-lg px-2.5 py-1 text-rose-300 font-mono text-xs"
              >
                <option value="ibm_eagle">IBM Quantum Eagle (127Q Transmon)</option>
                <option value="ionq_aria">IonQ Aria (Trapped Ion)</option>
                <option value="high_decoherence">Extreme Noise Stress Test</option>
              </select>

              <button
                onClick={handleRunNoisySim}
                disabled={isSimulatingNoise}
                className="px-3 py-1 rounded-lg bg-rose-500 hover:bg-rose-400 text-slate-950 font-bold text-xs transition disabled:opacity-50"
              >
                {isSimulatingNoise ? 'Emulating QPU...' : 'Run Hardware Sim'}
              </button>
            </div>
          </div>

          {noiseResult && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2 pt-2 border-t border-rose-500/20">
              <div className="bg-[#060a12] p-2.5 rounded-lg border border-slate-800">
                <span className="text-[10px] text-slate-400 uppercase">State Fidelity (F)</span>
                <div className="text-base font-mono font-bold text-emerald-400 mt-0.5">
                  {Math.round(noiseResult.fidelity * 100)}%
                </div>
              </div>
              <div className="bg-[#060a12] p-2.5 rounded-lg border border-slate-800">
                <span className="text-[10px] text-slate-400 uppercase">Quantum Error Rate</span>
                <div className="text-base font-mono font-bold text-rose-400 mt-0.5">
                  {Math.round(noiseResult.quantum_error_rate * 100)}%
                </div>
              </div>
              <div className="bg-[#060a12] p-2.5 rounded-lg border border-slate-800">
                <span className="text-[10px] text-slate-400 uppercase">T1 / T2 Rates</span>
                <div className="text-base font-mono font-bold text-cyan-400 mt-0.5">
                  {Math.round(noiseResult.noise_parameters.t1_decay_rate * 100)}% / {Math.round(noiseResult.noise_parameters.t2_dephasing_rate * 100)}%
                </div>
              </div>
              <div className="bg-[#060a12] p-2.5 rounded-lg border border-slate-800">
                <span className="text-[10px] text-slate-400 uppercase">CNOT 2Q Error</span>
                <div className="text-base font-mono font-bold text-amber-400 mt-0.5">
                  {Math.round(noiseResult.noise_parameters.two_qubit_cnot_error * 100)}%
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Gate Palette */}
      <div className="flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
            Gate Palette (Select then click wire to place)
          </span>
          {selectedPaletteGate && ['CNOT', 'CX', 'CZ', 'SWAP', 'CCX'].includes(selectedPaletteGate) && (
            <div className="flex items-center gap-2 text-xs">
              <span className="text-slate-400">Control Qubit:</span>
              <select
                value={controlQubit}
                onChange={(e) => setControlQubit(Number(e.target.value))}
                className="bg-slate-900 border border-slate-700 rounded px-2 py-0.5 text-cyan-400 font-mono text-xs"
              >
                {Array.from({ length: circuit.qubits }).map((_, i) => (
                  <option key={i} value={i}>q[{i}]</option>
                ))}
              </select>
            </div>
          )}
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {GATE_PALETTE.map((g) => {
            const isSelected = selectedPaletteGate === g.name;
            return (
              <button
                key={g.name}
                onClick={() => setSelectedPaletteGate(g.name)}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-xl font-mono text-xs font-bold transition transform active:scale-95 ${
                  isSelected
                    ? `bg-gradient-to-r ${g.color} text-white ring-2 ring-cyan-400 ring-offset-2 ring-offset-[#0b1329] shadow-lg`
                    : 'bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800'
                }`}
                title={g.desc}
              >
                <span>{g.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Circuit Grid */}
      <div className="overflow-x-auto bg-[#070b16] border border-slate-800 rounded-xl p-4">
        <div className="min-w-[600px] flex flex-col gap-5">
          {Array.from({ length: circuit.qubits }).map((_, qIdx) => {
            return (
              <div key={qIdx} className="flex items-center relative group">
                {/* Qubit Label */}
                <div className="w-16 flex items-center gap-1.5 font-mono text-xs font-bold text-slate-400 shrink-0">
                  <span className="text-cyan-400">q[{qIdx}]</span>
                  <span className="text-[10px] text-slate-600">|0⟩</span>
                </div>

                {/* Wire Line */}
                <div className="flex-1 relative flex items-center h-10">
                  <div className="absolute inset-x-0 h-0.5 bg-slate-800 group-hover:bg-slate-700 transition" />

                  {/* Step Slots */}
                  <div className="relative z-10 w-full grid grid-cols-10 gap-2">
                    {Array.from({ length: MAX_STEPS }).map((_, stepIdx) => {
                      const activeGate = circuit.gates.find(
                        g => (g.target === qIdx || (g.control === qIdx && ['CNOT', 'CX', 'CZ', 'SWAP'].includes(g.name))) && g.step === stepIdx
                      );

                      const isScrubberActive = activeStepIndex === stepIdx;

                      if (activeGate) {
                        const isTarget = activeGate.target === qIdx;
                        const isControl = activeGate.control === qIdx;
                        const isMultiQubit = ['CNOT', 'CX', 'CZ', 'SWAP', 'CCX'].includes(activeGate.name.toUpperCase());
                        const pal = GATE_PALETTE.find(p => p.name.toUpperCase() === activeGate.name.toUpperCase());

                        return (
                          <div
                            key={stepIdx}
                            onClick={() => handleCellClick(qIdx, stepIdx)}
                            className={`h-9 flex items-center justify-center rounded-lg cursor-pointer font-mono text-xs font-bold transition transform hover:scale-105 shadow-md ${
                              isControl
                                ? 'bg-indigo-600 text-white ring-2 ring-indigo-400'
                                : `bg-gradient-to-r ${pal?.color || 'from-cyan-500 to-blue-600'} text-white`
                            } ${isScrubberActive ? 'ring-4 ring-yellow-400 ring-offset-1 ring-offset-slate-900' : ''}`}
                            title={`Click to remove ${activeGate.name}`}
                          >
                            {isControl ? '●' : (pal?.label || activeGate.name)}
                          </div>
                        );
                      }

                      return (
                        <div
                          key={stepIdx}
                          onClick={() => handleCellClick(qIdx, stepIdx)}
                          className={`h-9 border border-dashed border-slate-850 hover:border-cyan-500/50 hover:bg-cyan-500/5 rounded-lg flex items-center justify-center cursor-pointer transition ${
                            isScrubberActive ? 'bg-yellow-400/10 border-yellow-400/40' : ''
                          }`}
                          title={`Place ${selectedPaletteGate} on q[${qIdx}] at step ${stepIdx}`}
                        >
                          <span className="opacity-0 hover:opacity-40 text-[10px] font-mono text-cyan-400">+</span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Step Scrubber Timeline Controls */}
      <div className="flex flex-wrap items-center justify-between gap-3 pt-2 text-xs">
        <div className="flex items-center gap-2">
          <span className="text-slate-400 font-medium">Timeline Execution:</span>
          <span className="px-2.5 py-1 rounded-lg bg-slate-900 font-mono text-cyan-300 font-bold border border-slate-800">
            {currentStep}
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={() => setActiveStepIndex((prev) => (prev === null ? 0 : Math.max(0, prev - 1)))}
            disabled={activeStepIndex === 0}
            className="p-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 disabled:opacity-30 border border-slate-800 transition"
            title="Previous Step"
          >
            <ChevronLeft className="w-4 h-4" />
          </button>

          <button
            onClick={() => setIsPlayingSteps(!isPlayingSteps)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-cyan-300 border border-slate-800 transition font-medium text-xs"
          >
            {isPlayingSteps ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
            <span>{isPlayingSteps ? 'Pause' : 'Play Timeline'}</span>
          </button>

          <button
            onClick={() => {
              if (simulationResult?.steps) {
                setActiveStepIndex((prev) => {
                  if (prev === null) return 0;
                  return Math.min(simulationResult.steps.length - 1, prev + 1);
                });
              }
            }}
            disabled={activeStepIndex === (simulationResult?.steps?.length - 1)}
            className="p-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 disabled:opacity-30 border border-slate-800 transition"
            title="Next Step"
          >
            <ChevronRight className="w-4 h-4" />
          </button>

          <button
            onClick={() => {
              setActiveStepIndex(null);
              setIsPlayingSteps(false);
            }}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium transition ${
              activeStepIndex === null
                ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 font-bold'
                : 'bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800'
            }`}
          >
            Final State
          </button>
        </div>
      </div>
    </div>
  );
}
