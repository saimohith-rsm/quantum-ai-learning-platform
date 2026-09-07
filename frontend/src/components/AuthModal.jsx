import React, { useState } from 'react';
import { useQuantum } from '../context/QuantumContext';
import { User, Lock, Mail, Sparkles, LogIn, UserPlus, Zap } from 'lucide-react';

export default function AuthModal({ isOpen, onClose }) {
  const { login, register, quickDemoLogin } = useQuantum();
  const [activeTab, setActiveTab] = useState('login'); // 'login' | 'register'
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [email, setEmail] = useState('');
  const [displayName, setDisplayName] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      if (activeTab === 'login') {
        await login(username, password);
      } else {
        await register({
          username,
          password,
          email: email || undefined,
          display_name: displayName || undefined
        });
      }
      onClose();
    } catch (err) {
      setError(err.message || 'Authentication failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDemoLogin = async () => {
    setError(null);
    setIsLoading(true);
    try {
      await quickDemoLogin();
      onClose();
    } catch (err) {
      setError(err.message || 'Demo login failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/80 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-[#0b1329] border border-cyan-500/30 rounded-2xl max-w-md w-full p-6 shadow-2xl relative">
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-5 right-5 text-slate-400 hover:text-white text-sm"
        >
          ✕
        </button>

        {/* Modal Header */}
        <div className="flex items-center gap-3 mb-5">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500 to-purple-600 flex items-center justify-center text-white shadow-lg shadow-cyan-500/20">
            <User className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-slate-100">Quantum Learner Account</h3>
            <p className="text-xs text-slate-400">Track progress, save circuits, and earn XP badges</p>
          </div>
        </div>

        {/* Tabs */}
        <div className="grid grid-cols-2 gap-1 p-1 rounded-xl bg-slate-900 border border-slate-800 mb-5">
          <button
            onClick={() => { setActiveTab('login'); setError(null); }}
            className={`py-2 text-xs font-bold rounded-lg transition flex items-center justify-center gap-1.5 ${
              activeTab === 'login'
                ? 'bg-cyan-600 text-white shadow-md shadow-cyan-500/20'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <LogIn className="w-3.5 h-3.5" />
            <span>Sign In</span>
          </button>

          <button
            onClick={() => { setActiveTab('register'); setError(null); }}
            className={`py-2 text-xs font-bold rounded-lg transition flex items-center justify-center gap-1.5 ${
              activeTab === 'register'
                ? 'bg-purple-600 text-white shadow-md shadow-purple-500/20'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <UserPlus className="w-3.5 h-3.5" />
            <span>Create Account</span>
          </button>
        </div>

        {/* Error Banner */}
        {error && (
          <div className="mb-4 p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs font-medium">
            {error}
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-3.5">
          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">
              Username {activeTab === 'login' ? 'or Email' : ''}
            </label>
            <div className="relative">
              <input
                type="text"
                required
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder={activeTab === 'login' ? 'e.g. quantum_explorer' : 'Choose a unique username'}
                className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-mono"
              />
              <User className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
            </div>
          </div>

          {activeTab === 'register' && (
            <>
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Display Name
                </label>
                <div className="relative">
                  <input
                    type="text"
                    value={displayName}
                    onChange={(e) => setDisplayName(e.target.value)}
                    placeholder="e.g. Marie Curie"
                    className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-purple-500"
                  />
                  <Sparkles className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Email Address (Optional)
                </label>
                <div className="relative">
                  <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="learner@university.edu"
                    className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-purple-500"
                  />
                  <Mail className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
                </div>
              </div>
            </>
          )}

          <div>
            <label className="block text-xs font-semibold text-slate-300 mb-1">Password</label>
            <div className="relative">
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-9 pr-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-cyan-500 font-mono"
              />
              <Lock className="w-4 h-4 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className={`w-full py-2.5 rounded-xl font-bold text-xs shadow-lg transition text-white ${
              activeTab === 'login'
                ? 'bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 shadow-cyan-500/20'
                : 'bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 shadow-purple-500/20'
            }`}
          >
            {isLoading ? 'Processing...' : (activeTab === 'login' ? 'Sign In to Account' : 'Create Quantum Account')}
          </button>
        </form>

        {/* Demo Fast Login */}
        <div className="mt-4 pt-4 border-t border-slate-800/80 text-center">
          <button
            onClick={handleDemoLogin}
            disabled={isLoading}
            className="w-full py-2 px-3 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-cyan-400 hover:text-cyan-300 text-xs font-medium transition flex items-center justify-center gap-1.5"
          >
            <Zap className="w-3.5 h-3.5 text-amber-400" />
            <span>One-Click Demo Login (Quantum Explorer)</span>
          </button>
        </div>
      </div>
    </div>
  );
}
