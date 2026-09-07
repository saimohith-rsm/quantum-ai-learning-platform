import React, { useState, useEffect } from 'react';
import { useQuantum } from '../context/QuantumContext';
import { getChallenges, submitChallenge, getChallengeHint } from '../services/api';
import { Trophy, Award, CheckCircle, AlertCircle, PlayCircle, Lightbulb, ArrowRight, Sparkles } from 'lucide-react';
import confetti from 'canvas-confetti';

export default function ChallengeArena() {
  const { circuit, setQubits, loadCircuit, setActiveTab, refreshProfile } = useQuantum();
  const [challenges, setChallenges] = useState([]);
  const [selectedChallenge, setSelectedChallenge] = useState(null);
  const [evalResult, setEvalResult] = useState(null);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [hintTier, setHintTier] = useState(1);
  const [hintText, setHintText] = useState(null);

  useEffect(() => {
    getChallenges()
      .then(data => {
        setChallenges(data);
        if (data.length > 0) setSelectedChallenge(data[0]);
      })
      .catch(err => console.error(err));
  }, []);

  const handleSelectChallenge = (c) => {
    setSelectedChallenge(c);
    setEvalResult(null);
    setHintText(null);
    setHintTier(1);
  };

  const handleSetupCircuit = () => {
    if (!selectedChallenge) return;
    setQubits(selectedChallenge.num_qubits);
    setActiveTab('studio');
  };

  const handleSubmit = async () => {
    if (!selectedChallenge) return;
    setIsSubmitting(true);
    try {
      const res = await submitChallenge(selectedChallenge.id, circuit, 1);
      setEvalResult(res);

      if (res.passed) {
        confetti({
          particleCount: 80,
          spread: 80,
          origin: { y: 0.6 }
        });
        await refreshProfile();
      }
    } catch (err) {
      console.error('Submission error:', err);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleGetHint = async () => {
    if (!selectedChallenge) return;
    try {
      const res = await getChallengeHint(selectedChallenge.id, circuit, hintTier);
      setHintText(res.explanation);
      setHintTier(prev => Math.min(3, prev + 1));
    } catch (err) {
      console.error(err);
    }
  };

  if (!selectedChallenge) {
    return <div className="p-8 text-center text-slate-400">Loading challenges...</div>;
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 max-w-7xl mx-auto p-4">
      {/* Sidebar: Challenge Cards */}
      <div className="lg:col-span-5 bg-[#0b1329] border border-cyan-500/20 rounded-2xl p-4 flex flex-col gap-4 shadow-xl">
        <div className="flex items-center gap-2 pb-3 border-b border-slate-800">
          <Trophy className="w-5 h-5 text-amber-400" />
          <h3 className="font-bold text-slate-100 text-sm">Challenge Quests</h3>
        </div>

        <div className="overflow-y-auto space-y-3 max-h-[70vh] pr-1">
          {challenges.map((c) => {
            const isSelected = selectedChallenge.id === c.id;
            return (
              <div
                key={c.id}
                onClick={() => handleSelectChallenge(c)}
                className={`p-4 rounded-xl border cursor-pointer transition ${
                  isSelected
                    ? 'bg-gradient-to-br from-cyan-950/60 to-purple-950/40 border-cyan-400/60 shadow-lg shadow-cyan-500/10'
                    : 'bg-slate-900/60 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-center justify-between gap-2 mb-1.5">
                  <h4 className={`text-sm font-bold ${isSelected ? 'text-cyan-300' : 'text-slate-200'}`}>
                    {c.title}
                  </h4>
                  <span className={`text-[10px] px-2 py-0.5 rounded-full font-semibold ${
                    c.difficulty === 'Beginner' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30' :
                    c.difficulty === 'Intermediate' ? 'bg-amber-500/10 text-amber-400 border border-amber-500/30' :
                    'bg-purple-500/10 text-purple-400 border border-purple-500/30'
                  }`}>
                    {c.difficulty}
                  </span>
                </div>
                <p className="text-xs text-slate-400 line-clamp-2 mb-2">
                  {c.description}
                </p>
                <div className="flex items-center justify-between text-[11px] font-mono text-slate-500 pt-1 border-t border-slate-800/60">
                  <span>{c.num_qubits} Qubits • Max {c.max_gates} Gates</span>
                  <span className="text-amber-400 font-bold">+{c.xp} XP</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Main Panel: Challenge Details & Grader */}
      <div className="lg:col-span-7 bg-[#0b1329] border border-cyan-500/20 rounded-2xl p-6 flex flex-col gap-6 shadow-xl overflow-y-auto max-h-[85vh]">
        {/* Header */}
        <div className="pb-4 border-b border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div className="flex items-center gap-2">
              <h2 className="text-xl font-bold text-slate-100">{selectedChallenge.title}</h2>
              <span className="text-xs px-2.5 py-0.5 rounded-full bg-amber-500/10 text-amber-300 border border-amber-500/30 font-bold font-mono">
                +{selectedChallenge.xp} XP
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1">{selectedChallenge.description}</p>
          </div>

          <button
            onClick={handleSetupCircuit}
            className="shrink-0 flex items-center gap-2 px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-cyan-400 border border-cyan-500/30 font-medium text-xs transition"
          >
            <PlayCircle className="w-4 h-4" />
            <span>Open in Circuit Studio</span>
          </button>
        </div>

        {/* Instructions */}
        <div className="space-y-3">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-300">
            Quest Objectives & Requirements
          </h4>
          <ul className="space-y-2">
            {selectedChallenge.instructions.map((inst, i) => (
              <li key={i} className="flex items-start gap-2 text-xs text-slate-300">
                <CheckCircle className="w-3.5 h-3.5 text-cyan-400 shrink-0 mt-0.5" />
                <span>{inst}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* AI Socratic Hint Box */}
        <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2 text-xs font-bold text-amber-300">
              <Lightbulb className="w-4 h-4 text-amber-400" />
              <span>Need Assistance? Ask AI Tutor for a Hint</span>
            </div>
            <button
              onClick={handleGetHint}
              className="px-2.5 py-1 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 border border-amber-500/30 text-xs font-medium transition"
            >
              Get Tier {hintTier} Hint
            </button>
          </div>
          {hintText && (
            <p className="text-xs text-slate-300 bg-slate-950/60 p-3 rounded-lg border border-amber-500/20 whitespace-pre-line">
              💡 {hintText}
            </p>
          )}
        </div>

        {/* Submit Circuit Button */}
        <div className="space-y-3 pt-2">
          <div className="flex items-center justify-between text-xs text-slate-400 font-mono">
            <span>Current Circuit in Studio: {circuit.qubits} Qubits, {circuit.gates.length} Gates</span>
            <span>Target Qubits: {selectedChallenge.num_qubits}</span>
          </div>

          <button
            onClick={handleSubmit}
            disabled={isSubmitting}
            className="w-full py-3 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 disabled:opacity-40 text-white font-bold text-sm shadow-lg shadow-emerald-500/25 transition flex items-center justify-center gap-2"
          >
            <Trophy className="w-4 h-4" />
            <span>{isSubmitting ? 'Evaluating Circuit Fidelity...' : 'Submit & Grade Circuit'}</span>
          </button>
        </div>

        {/* Grader Evaluation Result */}
        {evalResult && (
          <div className={`p-5 rounded-xl border space-y-3 transition ${
            evalResult.passed
              ? 'bg-emerald-500/10 border-emerald-500/40 text-emerald-300'
              : 'bg-rose-500/10 border-rose-500/40 text-rose-300'
          }`}>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2 font-bold text-base">
                {evalResult.passed ? '🏆 Challenge Passed!' : '❌ Challenge Not Passed'}
              </div>
              <span className="font-mono text-sm font-bold px-2 py-0.5 rounded bg-black/40">
                Fidelity: {(evalResult.fidelity * 100).toFixed(1)}%
              </span>
            </div>

            <p className="text-xs text-slate-200 leading-relaxed">
              {evalResult.feedback}
            </p>

            {evalResult.details?.target_comparison && (
              <div className="pt-2 border-t border-slate-800/80 space-y-1.5 font-mono text-[11px]">
                <div className="text-slate-400 font-bold">Target State Verification:</div>
                <div className="grid grid-cols-2 gap-2">
                  {Object.entries(evalResult.details.target_comparison).map(([st, data]) => (
                    <div key={st} className="p-2 rounded bg-slate-950/60 border border-slate-800 flex justify-between">
                      <span className="text-cyan-300">|{st}⟩</span>
                      <span>Exp: {(data.expected * 100).toFixed(0)}% | Act: {(data.actual * 100).toFixed(0)}%</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
