import React, { useState } from 'react';
import { useQuantum } from '../context/QuantumContext';
import { 
  Atom, BookOpen, Trophy, Save, Sparkles, Award, Cpu, 
  User, LogIn, LogOut, ChevronDown, CheckCircle2, KeyRound 
} from 'lucide-react';

export default function Navbar({ onOpenAuth, onOpenProtocols }) {
  const { activeTab, setActiveTab, userProfile, currentUser, logout, setIsAuthModalOpen } = useQuantum();
  const [showBadgesModal, setShowBadgesModal] = useState(false);
  const [showUserDropdown, setShowUserDropdown] = useState(false);

  const tabs = [
    { id: 'studio', label: 'Circuit Studio', icon: Cpu },
    { id: 'lessons', label: 'Guided Lessons', icon: BookOpen },
    { id: 'challenges', label: 'Challenge Arena', icon: Trophy },
    { id: 'saved', label: 'Saved Circuits', icon: Save },
  ];

  return (
    <>
      <header className="sticky top-0 z-40 bg-[#080d1a]/90 backdrop-blur-md border-b border-cyan-500/20 px-4 lg:px-8 py-3">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-3">
          
          {/* Logo and SIH Hackathon Meta */}
          <div className="flex items-center gap-3">
            <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-cyan-500/20 to-purple-500/20 border border-cyan-400/40 text-cyan-400 shadow-lg shadow-cyan-500/20">
              <Atom className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-xl font-bold tracking-tight bg-gradient-to-r from-cyan-400 via-sky-300 to-purple-400 bg-clip-text text-transparent">
                  QuantumAI
                </h1>
                <span className="text-[10px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                  SIH 2026
                </span>
              </div>
              <p className="text-xs text-slate-400">
                PS #26140 • Team Human X • Smart Education
              </p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="flex items-center gap-1 bg-[#0d162d] p-1 rounded-xl border border-slate-800">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex items-center gap-2 px-3.5 py-1.5 rounded-lg text-xs md:text-sm font-medium transition-all ${
                    isActive
                      ? 'bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-md shadow-cyan-500/25'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>

          {/* User Profile & Auth Section */}
          <div className="flex items-center gap-2.5">
            {/* BB84 Quantum Cryptography Button */}
            <button
              onClick={onOpenProtocols}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-purple-500/15 hover:bg-purple-500/25 border border-purple-500/30 text-purple-300 text-xs font-semibold transition"
              title="Quantum Cryptography: BB84 Quantum Key Distribution"
            >
              <KeyRound className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">BB84 QKD</span>
            </button>

            {currentUser ? (
              <div className="relative">
                <button
                  onClick={() => setShowUserDropdown(!showUserDropdown)}
                  className="flex items-center gap-2.5 px-3 py-1.5 rounded-xl bg-slate-900 hover:bg-slate-800/80 border border-slate-800 hover:border-cyan-500/30 text-xs transition shadow-sm"
                >
                  <div className="w-6 h-6 rounded-full bg-gradient-to-tr from-cyan-500 to-purple-600 flex items-center justify-center text-white font-bold text-[10px]">
                    {currentUser.display_name?.charAt(0) || currentUser.username?.charAt(0) || 'Q'}
                  </div>

                  <div className="text-left hidden sm:block">
                    <div className="font-bold text-slate-200 text-xs truncate max-w-[100px]">
                      {currentUser.display_name || currentUser.username}
                    </div>
                    <div className="text-[10px] text-purple-300 font-mono">
                      {userProfile?.level || 'Beginner'} • {userProfile?.xp || 0} XP
                    </div>
                  </div>

                  <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
                </button>

                {/* Dropdown Menu */}
                {showUserDropdown && (
                  <div className="absolute right-0 mt-2 w-52 bg-[#0b1329] border border-cyan-500/30 rounded-2xl p-2 shadow-2xl z-50">
                    <div className="p-2 border-b border-slate-800 text-xs">
                      <div className="font-bold text-slate-100">{currentUser.display_name || currentUser.username}</div>
                      <div className="text-[10px] text-slate-400 font-mono truncate">@{currentUser.username}</div>
                    </div>

                    <div className="py-1 space-y-0.5">
                      <button
                        onClick={() => {
                          setShowUserDropdown(false);
                          setShowBadgesModal(true);
                        }}
                        className="w-full text-left px-3 py-2 rounded-lg text-xs text-slate-300 hover:text-white hover:bg-slate-800/80 flex items-center gap-2 transition"
                      >
                        <Award className="w-3.5 h-3.5 text-purple-400" />
                        <span>Badges & Stats</span>
                      </button>

                      <button
                        onClick={() => {
                          setShowUserDropdown(false);
                          setIsAuthModalOpen(true);
                        }}
                        className="w-full text-left px-3 py-2 rounded-lg text-xs text-slate-300 hover:text-white hover:bg-slate-800/80 flex items-center gap-2 transition"
                      >
                        <User className="w-3.5 h-3.5 text-cyan-400" />
                        <span>Switch Account / Sign In</span>
                      </button>

                      <button
                        onClick={() => {
                          setShowUserDropdown(false);
                          logout();
                        }}
                        className="w-full text-left px-3 py-2 rounded-lg text-xs text-rose-400 hover:text-rose-300 hover:bg-rose-500/10 flex items-center gap-2 transition"
                      >
                        <LogOut className="w-3.5 h-3.5" />
                        <span>Sign Out</span>
                      </button>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <button
                onClick={() => setIsAuthModalOpen(true)}
                className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold text-xs shadow-lg shadow-cyan-500/25 transition"
              >
                <LogIn className="w-3.5 h-3.5" />
                <span>Sign In / Register</span>
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Badges & Profile Modal */}
      {showBadgesModal && userProfile && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-[#0b1329] border border-cyan-500/30 rounded-2xl p-6 max-w-md w-full shadow-2xl">
            <div className="flex items-center justify-between pb-4 border-b border-slate-800">
              <div className="flex items-center gap-2">
                <Award className="w-6 h-6 text-purple-400" />
                <h3 className="text-lg font-bold text-slate-100">Learner Achievements</h3>
              </div>
              <button
                onClick={() => setShowBadgesModal(false)}
                className="text-slate-400 hover:text-white text-sm px-2 py-1"
              >
                ✕
              </button>
            </div>

            <div className="py-4 space-y-4">
              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                <div>
                  <div className="text-xs text-slate-400">Current Rank</div>
                  <div className="text-base font-bold text-purple-300">{userProfile.level}</div>
                </div>
                <div className="text-right">
                  <div className="text-xs text-slate-400">Total Score</div>
                  <div className="text-base font-mono font-bold text-cyan-400">{userProfile.xp} XP</div>
                </div>
              </div>

              <div>
                <div className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-2">
                  Earned Badges ({userProfile.badges?.length || 0})
                </div>
                <div className="flex flex-wrap gap-2">
                  {userProfile.badges && userProfile.badges.map((b, i) => (
                    <span
                      key={i}
                      className="px-2.5 py-1 rounded-lg text-xs font-medium bg-purple-500/10 border border-purple-500/30 text-purple-300 flex items-center gap-1.5"
                    >
                      🏅 {b}
                    </span>
                  ))}
                  {(!userProfile.badges || userProfile.badges.length === 0) && (
                    <p className="text-xs text-slate-500">Complete challenges to earn your first badge!</p>
                  )}
                </div>
              </div>

              <div className="grid grid-cols-3 gap-2 pt-2 text-center text-xs">
                <div className="p-2 rounded-lg bg-slate-900/40 border border-slate-800">
                  <div className="font-bold text-slate-200">{userProfile.stats?.saved_circuits || 0}</div>
                  <div className="text-[10px] text-slate-500">Saved</div>
                </div>
                <div className="p-2 rounded-lg bg-slate-900/40 border border-slate-800">
                  <div className="font-bold text-slate-200">{userProfile.stats?.completed_lessons || 0}</div>
                  <div className="text-[10px] text-slate-500">Lessons</div>
                </div>
                <div className="p-2 rounded-lg bg-slate-900/40 border border-slate-800">
                  <div className="font-bold text-slate-200">{userProfile.stats?.passed_challenges || 0}</div>
                  <div className="text-[10px] text-slate-500">Challenges</div>
                </div>
              </div>
            </div>

            <button
              onClick={() => setShowBadgesModal(false)}
              className="w-full mt-2 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-medium text-sm transition"
            >
              Close
            </button>
          </div>
        </div>
      )}
    </>
  );
}
