import React from 'react';
import { useQuantum } from '../context/QuantumContext';
import { BarChart3 } from 'lucide-react';

export default function HistogramView() {
  const { simulationResult, currentStepData } = useQuantum();
  const stepData = currentStepData();
  const probs = stepData?.probabilities || {};
  const shotCounts = simulationResult?.shot_counts || {};

  const entries = Object.entries(probs).sort((a, b) => a[0].localeCompare(b[0]));
  const totalShots = 1024;

  return (
    <div className="bg-[#0b1329] border border-cyan-500/20 rounded-2xl p-4 flex flex-col shadow-xl">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <BarChart3 className="w-4 h-4 text-cyan-400" />
          <h3 className="text-sm font-bold text-slate-100">Measurement Probabilities</h3>
        </div>
        <span className="text-xs font-mono text-slate-400">
          N = {totalShots} Shots
        </span>
      </div>

      {/* Chart visualization */}
      <div className="py-4 flex items-end justify-around gap-2 h-44 border-b border-slate-800/80 px-2">
        {entries.map(([state, prob]) => {
          const heightPct = Math.max(4, Math.round(prob * 100));
          const count = shotCounts[state] || Math.round(prob * totalShots);
          const isHigh = prob > 0.1;

          return (
            <div key={state} className="flex-1 flex flex-col items-center gap-1 h-full justify-end group">
              <span className="text-[10px] font-mono text-slate-400 group-hover:text-cyan-300 transition">
                {(prob * 100).toFixed(1)}%
              </span>
              <div
                className={`w-full max-w-[36px] rounded-t-lg transition-all duration-500 ${
                  isHigh
                    ? 'bg-gradient-to-t from-cyan-600 to-cyan-400 shadow-lg shadow-cyan-500/30'
                    : 'bg-slate-800 group-hover:bg-slate-700'
                }`}
                style={{ height: `${heightPct}%` }}
              />
              <span className="text-xs font-mono font-bold text-slate-200 mt-1">
                |{state}⟩
              </span>
            </div>
          );
        })}
      </div>

      {/* Shot frequency table preview */}
      <div className="pt-3 flex flex-wrap items-center justify-between gap-2 text-xs font-mono text-slate-400">
        <span>Most Likely:</span>
        <div className="flex items-center gap-2">
          {entries
            .filter(([_, p]) => p > 0.05)
            .map(([state, p]) => (
              <span key={state} className="px-2 py-0.5 rounded bg-slate-900 border border-slate-800 text-cyan-300 font-bold">
                |{state}⟩: {(p * 100).toFixed(0)}%
              </span>
            ))}
        </div>
      </div>
    </div>
  );
}
