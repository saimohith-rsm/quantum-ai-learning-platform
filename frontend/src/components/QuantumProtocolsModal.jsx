import React, { useState } from 'react';
import { runBB84Protocol } from '../services/api';
import { ShieldCheck, ShieldAlert, KeyRound, Radio, Eye, EyeOff, Play, Info } from 'lucide-react';

export default function QuantumProtocolsModal({ isOpen, onClose }) {
  const [numBits, setNumBits] = useState(24);
  const [evePresent, setEvePresent] = useState(false);
  const [eveRate, setEveRate] = useState(1.0);
  const [results, setResults] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  if (!isOpen) return null;

  const handleRun = async () => {
    setIsLoading(true);
    try {
      const data = await runBB84Protocol(numBits, evePresent, eveRate);
      setResults(data);
    } catch (err) {
      console.error('BB84 execution failed:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-[#0b1329] border border-cyan-500/30 rounded-2xl max-w-5xl w-full max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-5 border-b border-slate-800 bg-slate-900/60">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-xl bg-purple-500/20 text-purple-400 border border-purple-500/30">
              <KeyRound className="w-5 h-5" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-base font-bold text-slate-100">Quantum Cryptography Lab: BB84 QKD Protocol</h3>
                <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-purple-500/10 text-purple-300 border border-purple-500/20">
                  No-Cloning Security
                </span>
              </div>
              <p className="text-xs text-slate-400">
                Simulate quantum key distribution between Alice and Bob with live eavesdropper (Eve) detection
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

        {/* Protocol Control Bar */}
        <div className="p-5 border-b border-slate-800 bg-slate-900/40 flex flex-wrap items-center justify-between gap-4">
          <div className="flex flex-wrap items-center gap-6">
            {/* Photons count */}
            <div className="flex items-center gap-2">
              <span className="text-xs text-slate-300 font-medium">Photons:</span>
              <select
                value={numBits}
                onChange={(e) => setNumBits(Number(e.target.value))}
                className="bg-slate-950 border border-slate-700 rounded-lg px-2.5 py-1 text-xs text-cyan-300 font-mono"
              >
                <option value={16}>16 Photons</option>
                <option value={24}>24 Photons</option>
                <option value={32}>32 Photons</option>
                <option value={48}>48 Photons</option>
              </select>
            </div>

            {/* Eve Interception Toggle */}
            <div className="flex items-center gap-2 bg-slate-950 px-3 py-1.5 rounded-xl border border-slate-800">
              {evePresent ? <Eye className="w-4 h-4 text-rose-400" /> : <EyeOff className="w-4 h-4 text-slate-400" />}
              <span className="text-xs text-slate-300 font-medium">Eavesdropper (Eve):</span>
              <button
                onClick={() => setEvePresent(!evePresent)}
                className={`px-3 py-0.5 rounded-md text-xs font-bold transition ${
                  evePresent
                    ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40'
                    : 'bg-slate-800 text-slate-400 hover:text-slate-200'
                }`}
              >
                {evePresent ? 'ACTIVE (Intercepting)' : 'INACTIVE (Clean)'}
              </button>
            </div>

            {evePresent && (
              <div className="flex items-center gap-2 text-xs">
                <span className="text-slate-400">Intercept Rate:</span>
                <input
                  type="range"
                  min="0.2"
                  max="1.0"
                  step="0.1"
                  value={eveRate}
                  onChange={(e) => setEveRate(Number(e.target.value))}
                  className="w-24 accent-rose-500"
                />
                <span className="font-mono text-rose-300 font-bold">{Math.round(eveRate * 100)}%</span>
              </div>
            )}
          </div>

          <button
            onClick={handleRun}
            disabled={isLoading}
            className="flex items-center gap-2 px-5 py-2 rounded-xl bg-gradient-to-r from-purple-500 to-indigo-600 hover:from-purple-400 hover:to-indigo-500 text-white font-bold text-xs shadow-lg shadow-purple-500/25 transition disabled:opacity-50"
          >
            <Play className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin' : ''}`} />
            <span>{isLoading ? 'Simulating Photons...' : 'Run BB84 Protocol'}</span>
          </button>
        </div>

        {/* Results area */}
        <div className="p-5 overflow-y-auto flex-1 flex flex-col gap-5">
          {!results ? (
            <div className="flex flex-col items-center justify-center h-64 text-center text-slate-400 gap-3">
              <Radio className="w-12 h-12 text-purple-400/50 animate-pulse" />
              <div>
                <p className="font-medium text-slate-300 text-sm">BB84 Protocol Ready to Simulate</p>
                <p className="text-xs text-slate-500 max-w-md mt-1">
                  Click 'Run BB84 Protocol' above to transmit polarized photons between Alice and Bob. Test with Eve active to observe the No-Cloning quantum state collapse and QBER spike!
                </p>
              </div>
            </div>
          ) : (
            <>
              {/* Status Banner */}
              <div
                className={`p-4 rounded-xl border flex items-center justify-between gap-4 ${
                  results.channel_status.includes('SECURE')
                    ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                    : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
                }`}
              >
                <div className="flex items-center gap-3">
                  {results.channel_status.includes('SECURE') ? (
                    <ShieldCheck className="w-6 h-6 text-emerald-400 shrink-0" />
                  ) : (
                    <ShieldAlert className="w-6 h-6 text-rose-400 shrink-0" />
                  )}
                  <div>
                    <h4 className="font-bold text-sm">{results.channel_status}</h4>
                    <p className="text-xs opacity-80 mt-0.5">
                      {results.channel_status.includes('SECURE')
                        ? 'Quantum Bit Error Rate (QBER) is below the 11% Shor-Preskill threshold. The sifted key is cryptographically secure!'
                        : 'QBER exceeded the 11% security bound! Eve’s measurement collapsed photon states and triggered detection. Key discarded.'}
                    </p>
                  </div>
                </div>

                <div className="text-right shrink-0">
                  <span className="text-xs uppercase tracking-wider opacity-75">QBER</span>
                  <div className="text-xl font-mono font-black">
                    {results.qber_percentage}%
                  </div>
                </div>
              </div>

              {/* Metric Cards */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div className="bg-[#060a12] border border-slate-800 p-3.5 rounded-xl">
                  <span className="text-[11px] text-slate-400 uppercase">Photons Sent</span>
                  <div className="text-lg font-mono font-bold text-slate-100 mt-1">{results.total_photons_sent}</div>
                </div>
                <div className="bg-[#060a12] border border-slate-800 p-3.5 rounded-xl">
                  <span className="text-[11px] text-slate-400 uppercase">Sifted Key Length</span>
                  <div className="text-lg font-mono font-bold text-cyan-400 mt-1">{results.sifted_key_length} bits</div>
                </div>
                <div className="bg-[#060a12] border border-slate-800 p-3.5 rounded-xl">
                  <span className="text-[11px] text-slate-400 uppercase">Sifted Bit Errors</span>
                  <div className={`text-lg font-mono font-bold mt-1 ${results.errors_in_sifted_key > 0 ? 'text-rose-400' : 'text-emerald-400'}`}>
                    {results.errors_in_sifted_key} bits
                  </div>
                </div>
                <div className="bg-[#060a12] border border-slate-800 p-3.5 rounded-xl">
                  <span className="text-[11px] text-slate-400 uppercase">Eve Interception</span>
                  <div className="text-lg font-mono font-bold text-purple-400 mt-1">
                    {results.eve_present ? `${Math.round(results.eve_intercept_rate * 100)}% active` : 'None'}
                  </div>
                </div>
              </div>

              {/* Key Display */}
              {results.alice_sifted_key && (
                <div className="bg-[#060a12] border border-slate-800 p-4 rounded-xl flex flex-col gap-2 font-mono text-xs">
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400">Alice's Sifted Secret Key:</span>
                    <span className="text-cyan-300 font-bold tracking-widest">{results.alice_sifted_key}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400">Bob's Sifted Measured Key:</span>
                    <span className={`font-bold tracking-widest ${results.alice_sifted_key === results.bob_sifted_key ? 'text-emerald-400' : 'text-rose-400'}`}>
                      {results.bob_sifted_key}
                    </span>
                  </div>
                </div>
              )}

              {/* Transmission Table */}
              <div className="flex flex-col gap-2">
                <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">
                  Photon-by-Photon Transmission Log
                </span>
                <div className="border border-slate-800 rounded-xl overflow-hidden max-h-60 overflow-y-auto">
                  <table className="w-full text-left font-mono text-xs">
                    <thead className="bg-slate-900/80 text-slate-400 border-b border-slate-800 text-[11px]">
                      <tr>
                        <th className="p-2.5">#</th>
                        <th className="p-2.5">Alice Bit & Basis</th>
                        <th className="p-2.5">Photon State</th>
                        {results.eve_present && <th className="p-2.5 text-rose-300">Eve Basis & Bit</th>}
                        <th className="p-2.5">Bob Basis & Bit</th>
                        <th className="p-2.5">Bases Match?</th>
                        <th className="p-2.5">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-850 bg-[#060a12]">
                      {results.transmission_steps.map((s) => (
                        <tr
                          key={s.index}
                          className={s.error_detected ? 'bg-rose-500/10 text-rose-200' : s.bases_matched ? 'bg-emerald-500/5 text-slate-200' : 'text-slate-400'}
                        >
                          <td className="p-2.5">{s.index}</td>
                          <td className="p-2.5">
                            <span className="font-bold text-cyan-300">{s.alice_bit}</span> ({s.alice_basis})
                          </td>
                          <td className="p-2.5 text-purple-300 font-bold">{s.photon_state}</td>
                          {results.eve_present && (
                            <td className="p-2.5 text-rose-300">
                              {s.eve_basis !== 'None' ? `${s.eve_bit} (${s.eve_basis})` : '—'}
                            </td>
                          )}
                          <td className="p-2.5">
                            <span className="font-bold text-cyan-300">{s.bob_bit}</span> ({s.bob_basis})
                          </td>
                          <td className="p-2.5">
                            {s.bases_matched ? (
                              <span className="text-emerald-400 font-bold">MATCH (Keep)</span>
                            ) : (
                              <span className="text-slate-600">Mismatch (Discard)</span>
                            )}
                          </td>
                          <td className="p-2.5 font-bold">
                            {s.error_detected ? (
                              <span className="text-rose-400">ERROR (Eve!)</span>
                            ) : s.bases_matched ? (
                              <span className="text-emerald-400">OK</span>
                            ) : (
                              '—'
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Theory Insight */}
              <div className="p-4 rounded-xl bg-purple-500/10 border border-purple-500/20 text-xs text-purple-200 flex items-start gap-2.5">
                <Info className="w-4 h-4 text-purple-400 shrink-0 mt-0.5" />
                <p className="leading-relaxed">{results.theoretical_insight}</p>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
