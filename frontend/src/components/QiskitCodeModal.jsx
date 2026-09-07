import React, { useState, useEffect } from 'react';
import { useQuantum } from '../context/QuantumContext';
import { exportMultiSdk } from '../services/api';
import { Copy, Check, Code2, Cpu } from 'lucide-react';

const SDK_TABS = [
  { id: 'qiskit', label: 'IBM Qiskit 1.0+', tag: 'Superconducting' },
  { id: 'cirq', label: 'Google Cirq', tag: 'Google Quantum AI' },
  { id: 'pennylane', label: 'PennyLane (QML)', tag: 'Xanadu' },
  { id: 'braket', label: 'Amazon Braket', tag: 'AWS Local' },
  { id: 'qasm', label: 'OpenQASM 2.0/3.0', tag: 'Universal IR' }
];

export default function QiskitCodeModal({ isOpen, onClose }) {
  const { circuit, simulationResult } = useQuantum();
  const [activeTab, setActiveTab] = useState('qiskit');
  const [copied, setCopied] = useState(false);
  const [sdkCodes, setSdkCodes] = useState({});
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (isOpen && circuit) {
      setIsLoading(true);
      exportMultiSdk(circuit)
        .then((res) => {
          setSdkCodes(res);
        })
        .catch((err) => {
          console.error('Multi-SDK export failed:', err);
          // Fallback to simulationResult if present
          setSdkCodes({
            qiskit: simulationResult?.qiskit_code || '# Run simulation to generate Qiskit code',
            qasm: simulationResult?.qasm_code || '// Run simulation to generate OpenQASM',
            cirq: '# Transpiling to Google Cirq...',
            pennylane: '# Transpiling to PennyLane...',
            braket: '# Transpiling to Amazon Braket...'
          });
        })
        .finally(() => setIsLoading(false));
    }
  }, [isOpen, circuit, simulationResult]);

  if (!isOpen) return null;

  const currentCode = sdkCodes[activeTab] || '# Loading code...';

  const handleCopy = () => {
    navigator.clipboard.writeText(currentCode);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-[#0b1329] border border-cyan-500/30 rounded-2xl max-w-4xl w-full max-h-[85vh] flex flex-col shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
              <Code2 className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-slate-100">Universal Quantum Transpiler</h3>
                <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
                  Multi-SDK 5-in-1
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Instantly export and run your circuit across IBM Qiskit, Google Cirq, PennyLane, AWS Braket & OpenQASM
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1.5 rounded-lg text-sm bg-slate-900 border border-slate-800"
          >
            ✕
          </button>
        </div>

        {/* Tab & Copy bar */}
        <div className="flex flex-wrap items-center justify-between gap-2 px-5 py-3 border-b border-slate-800/80 bg-slate-900/50">
          <div className="flex flex-wrap items-center gap-1.5">
            {SDK_TABS.map((tab) => {
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-mono font-bold transition ${
                    isActive
                      ? 'bg-gradient-to-r from-cyan-500/20 to-blue-600/20 text-cyan-300 border border-cyan-500/40 shadow-sm'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50 border border-transparent'
                  }`}
                >
                  <Cpu className="w-3 h-3 opacity-70" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>

          <button
            onClick={handleCopy}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 border border-cyan-500/40 text-xs font-semibold transition"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied to Clipboard!' : 'Copy Code'}</span>
          </button>
        </div>

        {/* Code Content */}
        <div className="p-5 overflow-y-auto flex-1 font-mono text-xs text-cyan-200 bg-[#060a12] select-all leading-relaxed whitespace-pre border-t border-slate-900">
          {isLoading ? (
            <div className="flex items-center justify-center h-48 text-slate-400 animate-pulse">
              Generating code across quantum SDKs...
            </div>
          ) : (
            currentCode
          )}
        </div>
      </div>
    </div>
  );
}
