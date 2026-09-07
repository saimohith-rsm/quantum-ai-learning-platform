import React from 'react';
import { useQuantum } from '../context/QuantumContext';
import { Sparkles, ArrowRight, Zap, CheckCircle } from 'lucide-react';

export default function AlgorithmPresets({ isOpen, onClose }) {
  const { presets, loadPreset, setActiveTab } = useQuantum();

  if (!isOpen) return null;

  const handleSelectPreset = (preset) => {
    loadPreset(preset);
    setActiveTab('studio');
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-[#0b1329] border border-cyan-500/30 rounded-2xl max-w-2xl w-full max-h-[85vh] flex flex-col shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-slate-800">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-purple-500/20 text-purple-400">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-slate-100">Quantum Algorithm Library</h2>
              <p className="text-xs text-slate-400">Pre-built, mathematically verified algorithms from SIH curriculum</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-white p-1 rounded-lg text-sm"
          >
            ✕
          </button>
        </div>

        {/* List of algorithms */}
        <div className="p-5 overflow-y-auto space-y-3">
          {presets.map((preset) => (
            <div
              key={preset.id}
              className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 hover:border-cyan-500/40 hover:bg-slate-900 transition flex flex-col sm:flex-row sm:items-center justify-between gap-4 group"
            >
              <div className="space-y-1.5 max-w-md">
                <div className="flex items-center gap-2">
                  <h4 className="font-bold text-slate-100 text-sm group-hover:text-cyan-300 transition">
                    {preset.name}
                  </h4>
                  <span className={`text-[10px] px-2 py-0.5 rounded-full font-semibold ${
                    preset.difficulty === 'Beginner' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' :
                    preset.difficulty === 'Intermediate' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/30' :
                    'bg-purple-500/10 text-purple-400 border border-purple-500/30'
                  }`}>
                    {preset.difficulty}
                  </span>
                </div>
                <p className="text-xs text-slate-400 leading-relaxed">
                  {preset.description}
                </p>
                <div className="flex items-center gap-3 text-[11px] text-slate-500 font-mono">
                  <span>{preset.qubits} Qubits</span>
                  <span>•</span>
                  <span>{preset.gates?.length || 0} Gates</span>
                  <span>•</span>
                  <span className="text-cyan-400">{preset.category}</span>
                </div>
              </div>

              <button
                onClick={() => handleSelectPreset(preset)}
                className="shrink-0 flex items-center gap-1.5 px-3.5 py-2 rounded-xl bg-cyan-600/20 hover:bg-cyan-600 text-cyan-300 hover:text-white border border-cyan-500/30 font-medium text-xs transition shadow-md"
              >
                <span>Load Circuit</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
