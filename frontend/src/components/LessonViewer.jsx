import React, { useState, useEffect } from 'react';
import { useQuantum } from '../context/QuantumContext';
import { getCurriculumModules, recordLessonProgress } from '../services/api';
import { BookOpen, CheckCircle, Clock, Award, PlayCircle, HelpCircle, ArrowRight } from 'lucide-react';
import confetti from 'canvas-confetti';

export default function LessonViewer() {
  const { loadCircuit, setActiveTab, refreshProfile } = useQuantum();
  const [modules, setModules] = useState([]);
  const [activeLesson, setActiveLesson] = useState(null);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [quizSubmitted, setQuizSubmitted] = useState(false);
  const [quizFeedback, setQuizFeedback] = useState(null);

  useEffect(() => {
    getCurriculumModules()
      .then(mods => {
        setModules(mods);
        if (mods.length > 0 && mods[0].lessons?.length > 0) {
          setActiveLesson(mods[0].lessons[0]);
        }
      })
      .catch(err => console.error('Failed to load modules:', err));
  }, []);

  const handleSelectLesson = (lesson) => {
    setActiveLesson(lesson);
    setSelectedAnswer(null);
    setQuizSubmitted(false);
    setQuizFeedback(null);
  };

  const handleLoadStarterCircuit = () => {
    if (activeLesson?.starter_circuit) {
      loadCircuit(activeLesson.starter_circuit);
      setActiveTab('studio');
    }
  };

  const handleQuizSubmit = async () => {
    if (selectedAnswer === null || !activeLesson?.quiz) return;

    const isCorrect = selectedAnswer === activeLesson.quiz.correct_index;
    setQuizSubmitted(true);
    setQuizFeedback({
      isCorrect,
      explanation: activeLesson.quiz.explanation
    });

    if (isCorrect) {
      confetti({
        particleCount: 50,
        spread: 60,
        origin: { y: 0.7 }
      });
      // Record progress in DB
      try {
        const parentMod = modules.find(m => m.lessons.some(l => l.id === activeLesson.id));
        await recordLessonProgress(parentMod?.id || 'module_1', activeLesson.id, 100.0, 1);
        await refreshProfile();
      } catch (err) {
        console.error('Failed to save progress:', err);
      }
    }
  };

  if (!activeLesson) {
    return <div className="p-8 text-center text-slate-400">Loading curriculum...</div>;
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 max-w-7xl mx-auto p-4">
      {/* Sidebar: Module Navigation */}
      <div className="lg:col-span-4 bg-[#0b1329] border border-cyan-500/20 rounded-2xl p-4 flex flex-col gap-4 shadow-xl">
        <div className="flex items-center gap-2 pb-3 border-b border-slate-800">
          <BookOpen className="w-5 h-5 text-cyan-400" />
          <h3 className="font-bold text-slate-100 text-sm">Learning Pathway</h3>
        </div>

        <div className="overflow-y-auto space-y-4 max-h-[70vh] pr-1">
          {modules.map((mod) => (
            <div key={mod.id} className="space-y-2">
              <div className="text-xs font-bold text-purple-300 uppercase tracking-wider">
                {mod.title}
              </div>
              <div className="space-y-1.5 pl-2 border-l border-slate-800">
                {mod.lessons.map((les) => {
                  const isCurrent = activeLesson.id === les.id;
                  return (
                    <button
                      key={les.id}
                      onClick={() => handleSelectLesson(les)}
                      className={`w-full text-left p-2 rounded-xl text-xs transition flex items-center justify-between ${
                        isCurrent
                          ? 'bg-cyan-500/20 text-cyan-300 font-bold border border-cyan-500/40'
                          : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
                      }`}
                    >
                      <span className="truncate pr-2">{les.title}</span>
                      <span className="text-[10px] text-slate-500 font-mono shrink-0 flex items-center gap-1">
                        <Clock className="w-3 h-3" />
                        {les.estimated_minutes}m
                      </span>
                    </button>
                  );
                })}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Main Lesson Content & Interactive Quiz */}
      <div className="lg:col-span-8 bg-[#0b1329] border border-cyan-500/20 rounded-2xl p-6 flex flex-col gap-6 shadow-xl overflow-y-auto max-h-[85vh]">
        {/* Lesson Header */}
        <div className="pb-4 border-b border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <h2 className="text-xl font-bold text-slate-100">{activeLesson.title}</h2>
            <p className="text-xs text-slate-400 mt-1">{activeLesson.summary}</p>
          </div>
          <button
            onClick={handleLoadStarterCircuit}
            className="shrink-0 flex items-center gap-2 px-4 py-2 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold text-xs shadow-lg shadow-cyan-500/25 transition"
          >
            <PlayCircle className="w-4 h-4" />
            <span>Open in Circuit Studio</span>
          </button>
        </div>

        {/* Lesson Text / Reading Material */}
        <div className="prose prose-invert max-w-none text-slate-300 text-sm leading-relaxed space-y-4">
          {activeLesson.content.split('\n\n').map((paragraph, pIdx) => {
            if (paragraph.startsWith('# ')) {
              return null; // Skip main title as shown above
            }
            if (paragraph.startsWith('### ')) {
              return <h4 key={pIdx} className="text-base font-bold text-cyan-300 mt-4">{paragraph.replace('### ', '')}</h4>;
            }
            if (paragraph.startsWith('$$') && paragraph.endsWith('$$')) {
              return (
                <div key={pIdx} className="p-3 my-2 rounded-xl bg-slate-950 font-mono text-center text-cyan-400 border border-cyan-500/20 text-sm overflow-x-auto">
                  {paragraph.replace(/\$\$/g, '')}
                </div>
              );
            }
            return <p key={pIdx}>{paragraph}</p>;
          })}
        </div>

        {/* Checkpoint Quiz */}
        {activeLesson.quiz && (
          <div className="mt-4 p-5 rounded-xl bg-slate-900/80 border border-purple-500/30 space-y-4">
            <div className="flex items-center gap-2">
              <HelpCircle className="w-5 h-5 text-purple-400" />
              <h3 className="font-bold text-slate-100 text-sm">Interactive Knowledge Checkpoint</h3>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-purple-500/10 text-purple-300 border border-purple-500/30 font-semibold">
                +30 XP
              </span>
            </div>

            <p className="text-xs text-slate-200 font-medium">
              {activeLesson.quiz.question}
            </p>

            <div className="space-y-2">
              {activeLesson.quiz.options.map((opt, oIdx) => (
                <button
                  key={oIdx}
                  disabled={quizSubmitted}
                  onClick={() => setSelectedAnswer(oIdx)}
                  className={`w-full text-left p-3 rounded-xl text-xs font-medium transition flex items-center justify-between ${
                    selectedAnswer === oIdx
                      ? 'bg-purple-600/30 border-purple-500 text-purple-200 ring-1 ring-purple-400'
                      : 'bg-slate-950/60 hover:bg-slate-950 border-slate-800 text-slate-300'
                  } border`}
                >
                  <span>{opt}</span>
                  {selectedAnswer === oIdx && <CheckCircle className="w-4 h-4 text-purple-400 shrink-0" />}
                </button>
              ))}
            </div>

            {!quizSubmitted ? (
              <button
                onClick={handleQuizSubmit}
                disabled={selectedAnswer === null}
                className="w-full py-2.5 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-500 hover:to-indigo-500 disabled:opacity-40 text-white font-bold text-xs shadow-lg shadow-purple-500/25 transition"
              >
                Submit Answer
              </button>
            ) : (
              <div className={`p-4 rounded-xl border text-xs space-y-1.5 ${
                quizFeedback?.isCorrect
                  ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
                  : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
              }`}>
                <div className="font-bold text-sm">
                  {quizFeedback?.isCorrect ? '🎉 Correct! +30 XP Awarded' : '❌ Not quite right'}
                </div>
                <p className="text-slate-300">{quizFeedback?.explanation}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
