import React, { useState } from 'react';
import { useQuantum } from './context/QuantumContext';
import Navbar from './components/Navbar';
import CircuitBuilder from './components/CircuitBuilder';
import BlochSphere3D from './components/BlochSphere3D';
import StatevectorView from './components/StatevectorView';
import HistogramView from './components/HistogramView';
import AITutorPanel from './components/AITutorPanel';
import LessonViewer from './components/LessonViewer';
import ChallengeArena from './components/ChallengeArena';
import SavedCircuitsView from './components/SavedCircuitsView';
import AlgorithmPresets from './components/AlgorithmPresets';
import QiskitCodeModal from './components/QiskitCodeModal';
import SaveCircuitModal from './components/SaveCircuitModal';
import AuthModal from './components/AuthModal';
import QuantumProtocolsModal from './components/QuantumProtocolsModal';

export default function App() {
  const { activeTab, isAuthModalOpen, setIsAuthModalOpen } = useQuantum();

  // Modals state
  const [showPresets, setShowPresets] = useState(false);
  const [showExport, setShowExport] = useState(false);
  const [showSave, setShowSave] = useState(false);
  const [showProtocols, setShowProtocols] = useState(false);

  return (
    <div className="min-h-screen flex flex-col bg-[#060a12] text-slate-100">
      <Navbar onOpenProtocols={() => setShowProtocols(true)} />

      {/* Main View Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 lg:p-6">
        {activeTab === 'studio' && (
          <div className="flex flex-col gap-6">
            {/* Top: Circuit Studio Timeline */}
            <CircuitBuilder
              onOpenExport={() => setShowExport(true)}
              onOpenPresets={() => setShowPresets(true)}
              onOpenSave={() => setShowSave(true)}
            />

            {/* Bottom: Visualization Dashboard + AI Tutor Panel */}
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
              {/* Visualizations (8 cols) */}
              <div className="lg:col-span-8 flex flex-col gap-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <BlochSphere3D />
                  <HistogramView />
                </div>
                <StatevectorView />
              </div>

              {/* AI Quantum Tutor Sidebar (4 cols) */}
              <div className="lg:col-span-4">
                <AITutorPanel />
              </div>
            </div>
          </div>
        )}

        {activeTab === 'lessons' && <LessonViewer />}
        {activeTab === 'challenges' && <ChallengeArena />}
        {activeTab === 'saved' && <SavedCircuitsView />}
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-[#080d1a] py-4 px-6 text-center text-xs text-slate-500">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-2">
          <span>
            ⚛️ <strong>QuantumAI</strong> • Smart India Hackathon 2026 (Problem #26140)
          </span>
          <span>
            Designed & Developed by <strong>Team Human X</strong> (TEAM-186) • Theme: Smart Education
          </span>
          <span className="font-mono text-cyan-400/80">
            FastAPI • NumPy • Three.js • React • SQLite
          </span>
        </div>
      </footer>

      {/* Modals */}
      <AlgorithmPresets isOpen={showPresets} onClose={() => setShowPresets(false)} />
      <QiskitCodeModal isOpen={showExport} onClose={() => setShowExport(false)} />
      <SaveCircuitModal isOpen={showSave} onClose={() => setShowSave(false)} />
      <AuthModal isOpen={isAuthModalOpen} onClose={() => setIsAuthModalOpen(false)} />
      <QuantumProtocolsModal isOpen={showProtocols} onClose={() => setShowProtocols(false)} />
    </div>
  );
}
