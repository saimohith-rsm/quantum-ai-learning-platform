import React, { useState } from 'react';
import { useQuantum } from '../context/QuantumContext';
import { explainCircuit, debugCircuit, chatWithTutor } from '../services/api';
import { Bot, Sparkles, Send, HelpCircle, CheckCircle2, AlertTriangle, Lightbulb, Brain, Cpu } from 'lucide-react';

export default function AITutorPanel() {
  const { circuit, userProfile } = useQuantum();
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      title: 'AI Quantum Tutor Ready',
      text: 'Hello! I am your AI Quantum Tutor. Build any circuit, test NISQ hardware noise, run BB84 quantum key distribution, or ask me any conceptual quantum questions!',
      insights: ['Toggle Socratic Mode for guided pedagogical discovery', 'Ask questions anytime or click "Explain"'],
      math: null
    }
  ]);
  const [inputVal, setInputVal] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [provider, setProvider] = useState('auto'); // 'auto', 'gemini', 'openai', 'offline'
  const [socraticMode, setSocraticMode] = useState(false);

  const handleExplain = async () => {
    setIsLoading(true);
    try {
      const resp = await explainCircuit(circuit, userProfile?.level || 'Beginner');
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          title: resp.title,
          text: resp.explanation,
          insights: resp.key_insights,
          math: resp.quantum_math
        }
      ]);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDebug = async () => {
    setIsLoading(true);
    try {
      const resp = await debugCircuit(circuit, 'Bell State or Grover Search', userProfile?.level || 'Beginner');
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          title: resp.title,
          text: resp.explanation,
          insights: resp.key_insights,
          math: resp.quantum_math
        }
      ]);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (customPrompt) => {
    const textToSend = customPrompt || inputVal;
    if (!textToSend.trim()) return;

    setMessages(prev => [...prev, { role: 'user', text: textToSend }]);
    setInputVal('');
    setIsLoading(true);

    try {
      const resp = await chatWithTutor(
        textToSend,
        circuit,
        userProfile?.level || 'Beginner',
        provider,
        socraticMode
      );
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          title: resp.title,
          text: resp.explanation,
          insights: resp.key_insights,
          math: resp.quantum_math
        }
      ]);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const quickChips = [
    "What does Hadamard do?",
    "How does Quantum Teleportation work?",
    "How does BB84 QKD detect Eve?",
    "What causes T1 and T2 decoherence?",
    "How does Grover's search work?"
  ];

  return (
    <div className="bg-[#0b1329] border border-cyan-500/20 rounded-2xl p-4 flex flex-col h-[580px] shadow-xl">
      {/* Header */}
      <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-purple-500 to-cyan-500 flex items-center justify-center text-white shadow-md shadow-purple-500/20">
            <Bot className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-100 flex items-center gap-1.5">
              <span>AI Quantum Tutor</span>
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            </h3>
            <p className="text-[11px] text-slate-400">SIH 2026 Multi-Model Intelligence</p>
          </div>
        </div>

        {/* Quick Action buttons */}
        <div className="flex items-center gap-1.5">
          <button
            onClick={handleExplain}
            disabled={isLoading}
            className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 text-xs font-medium transition"
          >
            <Sparkles className="w-3.5 h-3.5" />
            <span>Explain</span>
          </button>
          <button
            onClick={handleDebug}
            disabled={isLoading}
            className="flex items-center gap-1 px-2.5 py-1 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 border border-amber-500/30 text-xs font-medium transition"
          >
            <AlertTriangle className="w-3.5 h-3.5" />
            <span>Diagnose</span>
          </button>
        </div>
      </div>

      {/* Model Provider & Socratic Controls Bar */}
      <div className="flex items-center justify-between py-2 px-1 border-b border-slate-850 text-xs gap-2">
        <div className="flex items-center gap-1.5">
          <Cpu className="w-3.5 h-3.5 text-cyan-400" />
          <select
            value={provider}
            onChange={(e) => setProvider(e.target.value)}
            className="bg-slate-900 border border-slate-700 rounded px-2 py-0.5 text-slate-200 text-[11px] font-mono"
          >
            <option value="auto">Auto (Gemini/ChatGPT)</option>
            <option value="gemini">Google Gemini</option>
            <option value="openai">OpenAI ChatGPT</option>
            <option value="offline">Verified Quantum KB</option>
          </select>
        </div>

        {/* Socratic Mode Toggle */}
        <button
          onClick={() => setSocraticMode(!socraticMode)}
          className={`flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[11px] font-medium transition ${
            socraticMode
              ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40'
              : 'bg-slate-900 text-slate-400 hover:text-slate-200 border border-slate-800'
          }`}
          title="Socratic mode guides you with pedagogical questions rather than giving immediate answers"
        >
          <Brain className="w-3 h-3 text-purple-400" />
          <span>Socratic Mode</span>
          {socraticMode && <span className="w-1.5 h-1.5 rounded-full bg-purple-400" />}
        </button>
      </div>

      {/* Chat Messages */}
      <div className="flex-1 overflow-y-auto py-3 space-y-3 pr-1">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`p-3 rounded-xl text-xs transition ${
              m.role === 'user'
                ? 'bg-cyan-500/10 border border-cyan-500/30 text-cyan-100 ml-6'
                : 'bg-slate-900/80 border border-slate-800 text-slate-200 mr-2'
            }`}
          >
            {m.title && (
              <div className="font-bold text-xs text-cyan-300 mb-1 flex items-center gap-1.5">
                <Lightbulb className="w-3.5 h-3.5 text-amber-400" />
                <span>{m.title}</span>
              </div>
            )}
            <p className="leading-relaxed whitespace-pre-line">{m.text}</p>

            {m.math && (
              <div className="mt-2.5 p-2 rounded-lg bg-black/40 border border-slate-800 font-mono text-[11px] text-purple-300 select-all">
                {m.math}
              </div>
            )}

            {m.insights && m.insights.length > 0 && (
              <div className="mt-2 pt-2 border-t border-slate-800/60 space-y-1">
                {m.insights.map((ins, i) => (
                  <div key={i} className="flex items-start gap-1.5 text-[11px] text-slate-400">
                    <CheckCircle2 className="w-3 h-3 text-emerald-400 shrink-0 mt-0.5" />
                    <span>{ins}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-400 flex items-center gap-2">
            <Bot className="w-4 h-4 text-cyan-400 animate-bounce" />
            <span>AI Tutor is reasoning through your circuit...</span>
          </div>
        )}
      </div>

      {/* Quick Chips */}
      <div className="py-2 flex items-center gap-1.5 overflow-x-auto no-scrollbar">
        {quickChips.map((chip, idx) => (
          <button
            key={idx}
            onClick={() => handleSendMessage(chip)}
            className="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 hover:border-cyan-500/30 text-[11px] text-slate-300 whitespace-nowrap transition"
          >
            {chip}
          </button>
        ))}
      </div>

      {/* Input Form */}
      <form
        onSubmit={(e) => {
          e.preventDefault();
          handleSendMessage();
        }}
        className="flex items-center gap-2 pt-2 border-t border-slate-800"
      >
        <input
          type="text"
          value={inputVal}
          onChange={(e) => setInputVal(e.target.value)}
          placeholder={socraticMode ? "Ask a question (Socratic mode active)..." : "Ask about your circuit, gates, or quantum physics..."}
          className="flex-1 bg-slate-900 border border-slate-700 focus:border-cyan-500 rounded-xl px-3 py-2 text-xs text-slate-200 placeholder-slate-500 focus:outline-none"
        />
        <button
          type="submit"
          disabled={!inputVal.trim() || isLoading}
          className="p-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold disabled:opacity-40 transition"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}
