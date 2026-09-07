import React from 'react';
import { useQuantum } from '../context/QuantumContext';

export default function StatevectorView() {
  const { currentStepData } = useQuantum();
  const stepData = currentStepData();
  const statevector = stepData?.statevector || [];

  return (
    <div className="bg-[#0b1329] border border-cyan-500/20 rounded-2xl p-4 flex flex-col shadow-xl">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div>
          <h3 className="text-sm font-bold text-slate-100">Statevector & Quantum Phase</h3>
          <p className="text-[11px] text-slate-400">Complex amplitudes α|x⟩ and relative phases</p>
        </div>
        <span className="text-xs font-mono text-cyan-400 font-bold">
          2^{Math.log2(statevector.length || 1)} = {statevector.length} States
        </span>
      </div>

      <div className="py-3 flex flex-col gap-2 max-h-[280px] overflow-y-auto pr-1">
        {statevector.map((entry) => {
          const pct = (entry.probability * 100).toFixed(1);
          const hasAmplitude = entry.probability > 0.001;

          // Compute phase hue (0° = red, 90° = yellow, 180° = cyan, 270° = blue)
          const phaseHue = entry.phase_deg;

          return (
            <div
              key={entry.index}
              className={`p-2 rounded-xl border transition ${
                hasAmplitude
                  ? 'bg-slate-900/80 border-cyan-500/30'
                  : 'bg-slate-950/40 border-slate-800/40 opacity-40'
              }`}
            >
              <div className="flex items-center justify-between text-xs font-mono mb-1.5">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-cyan-300 bg-cyan-950/60 px-2 py-0.5 rounded border border-cyan-500/30">
                    |{entry.label}⟩
                  </span>
                  <span className="text-slate-400 text-[11px]">
                    {entry.real >= 0 ? '+' : ''}{entry.real.toFixed(3)}
                    {entry.imag >= 0 ? '+' : ''}{entry.imag.toFixed(3)}i
                  </span>
                </div>

                <div className="flex items-center gap-3">
                  {/* Phase wheel badge */}
                  <span
                    className="text-[10px] px-1.5 py-0.5 rounded font-mono font-semibold"
                    style={{
                      backgroundColor: `hsla(${phaseHue}, 80%, 50%, 0.15)`,
                      color: `hsl(${phaseHue}, 90%, 65%)`,
                      border: `1px solid hsla(${phaseHue}, 80%, 50%, 0.4)`
                    }}
                  >
                    ∠ {entry.phase_deg.toFixed(0)}°
                  </span>
                  <span className="font-bold text-slate-100">{pct}%</span>
                </div>
              </div>

              {/* Progress bar */}
              <div className="w-full h-2 rounded-full bg-slate-950 overflow-hidden border border-slate-800">
                <div
                  className="h-full rounded-full transition-all duration-300 bg-gradient-to-r from-cyan-500 to-purple-500"
                  style={{ width: `${pct}%` }}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
