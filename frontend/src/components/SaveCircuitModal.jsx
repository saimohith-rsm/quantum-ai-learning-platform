import React, { useState } from 'react';
import { useQuantum } from '../context/QuantumContext';
import { saveCircuit } from '../services/api';
import { Save, Check } from 'lucide-react';

export default function SaveCircuitModal({ isOpen, onClose }) {
  const { circuit, refreshProfile } = useQuantum();
  const [name, setName] = useState('My Custom Circuit');
  const [description, setDescription] = useState('');
  const [isSaving, setIsSaving] = useState(false);
  const [success, setSuccess] = useState(false);

  if (!isOpen) return null;

  const handleSave = async (e) => {
    e.preventDefault();
    if (!name.trim()) return;

    setIsSaving(true);
    try {
      await saveCircuit({
        name,
        description,
        num_qubits: circuit.qubits,
        circuit_json: JSON.stringify(circuit),
        is_public: false
      }, 1);
      setSuccess(true);
      await refreshProfile();
      setTimeout(() => {
        setSuccess(false);
        onClose();
      }, 1200);
    } catch (err) {
      console.error(err);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-[#0b1329] border border-cyan-500/30 rounded-2xl max-w-md w-full p-6 shadow-2xl">
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <Save className="w-5 h-5 text-cyan-400" />
            <h3 className="font-bold text-slate-100 text-sm">Save Circuit to Database</h3>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-sm">✕</button>
        </div>

        <form onSubmit={handleSave} className="py-4 space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Circuit Name</label>
            <input
              type="text"
              required
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="e.g. 2-Qubit Entanglement Test"
              className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Description (Optional)</label>
            <textarea
              rows={3}
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Describe what this circuit computes..."
              className="w-full bg-slate-900 border border-slate-800 rounded-xl px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500"
            />
          </div>

          <div className="text-[11px] text-slate-500 font-mono">
            {circuit.qubits} Qubits • {circuit.gates.length} Gates
          </div>

          {success ? (
            <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs font-bold flex items-center justify-center gap-2">
              <Check className="w-4 h-4" />
              <span>Saved Successfully to Database!</span>
            </div>
          ) : (
            <button
              type="submit"
              disabled={isSaving}
              className="w-full py-2.5 rounded-xl bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-bold text-xs shadow-lg transition"
            >
              {isSaving ? 'Saving...' : 'Save Circuit'}
            </button>
          )}
        </form>
      </div>
    </div>
  );
}
