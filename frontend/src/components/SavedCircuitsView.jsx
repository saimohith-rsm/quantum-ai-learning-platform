import React, { useState, useEffect } from 'react';
import { useQuantum } from '../context/QuantumContext';
import { getSavedCircuits, deleteSavedCircuit } from '../services/api';
import { Save, PlayCircle, Trash2, ArrowRight } from 'lucide-react';

export default function SavedCircuitsView() {
  const { loadCircuit, setActiveTab, refreshProfile } = useQuantum();
  const [circuits, setCircuits] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchCircuits = () => {
    setIsLoading(true);
    getSavedCircuits(1)
      .then(data => setCircuits(data))
      .catch(err => console.error(err))
      .finally(() => setIsLoading(false));
  };

  useEffect(() => {
    fetchCircuits();
  }, []);

  const handleLoad = (circRecord) => {
    try {
      const parsed = JSON.parse(circRecord.circuit_json);
      loadCircuit(parsed);
      setActiveTab('studio');
    } catch (err) {
      console.error('Failed to parse circuit JSON:', err);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Delete this circuit?')) return;
    try {
      await deleteSavedCircuit(id, 1);
      fetchCircuits();
      await refreshProfile();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-6 bg-[#0b1329] border border-cyan-500/20 rounded-2xl shadow-xl flex flex-col gap-6">
      <div className="flex items-center justify-between pb-4 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-xl bg-cyan-500/20 text-cyan-400">
            <Save className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold text-slate-100">Saved Quantum Circuits</h2>
            <p className="text-xs text-slate-400">Persisted locally in your SQLite database</p>
          </div>
        </div>

        <span className="text-xs font-mono px-3 py-1 rounded-full bg-slate-900 text-cyan-400 border border-slate-800">
          {circuits.length} Circuits Stored
        </span>
      </div>

      {isLoading ? (
        <div className="p-8 text-center text-slate-500 text-xs">Loading saved circuits...</div>
      ) : circuits.length === 0 ? (
        <div className="p-12 text-center text-slate-500 text-xs space-y-2">
          <p>No saved circuits found in your database.</p>
          <p className="text-slate-400">Create a circuit in the Circuit Studio and click "Save" to keep it here!</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {circuits.map((circ) => {
            let gateCount = 0;
            try {
              const parsed = JSON.parse(circ.circuit_json);
              gateCount = parsed.gates?.length || 0;
            } catch (e) {}

            return (
              <div
                key={circ.id}
                className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 hover:border-cyan-500/40 transition flex flex-col justify-between gap-3 group"
              >
                <div>
                  <h4 className="font-bold text-sm text-slate-100 group-hover:text-cyan-300 transition">
                    {circ.name}
                  </h4>
                  <p className="text-xs text-slate-400 mt-1 line-clamp-2">
                    {circ.description || 'No description provided.'}
                  </p>
                </div>

                <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 pt-2 border-t border-slate-800/80">
                  <span>{circ.num_qubits} Qubits • {gateCount} Gates</span>
                  
                  <div className="flex items-center gap-1.5">
                    <button
                      onClick={() => handleLoad(circ)}
                      className="flex items-center gap-1 px-3 py-1 rounded-lg bg-cyan-600/20 hover:bg-cyan-600 text-cyan-300 hover:text-white border border-cyan-500/30 text-xs font-medium transition"
                    >
                      <span>Load</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                    <button
                      onClick={() => handleDelete(circ.id)}
                      className="p-1.5 rounded-lg bg-slate-800 hover:bg-rose-500/20 text-slate-400 hover:text-rose-400 transition"
                      title="Delete Circuit"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
