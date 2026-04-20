'use client';

import { useState, useEffect, useRef, useCallback } from 'react';
import {
  ChevronRight, ChevronLeft, Clock, Zap, BookOpen, Video,
  CheckCircle, XCircle, AlertCircle, TrendingUp, BarChart2,
  PlayCircle, X, SkipForward, Flag, Info,
} from 'lucide-react';
import { QuestionV2, ChoiceV2 } from '@/types/question';
import { ELState, elTierLabel, updateEL } from '@/lib/el-algorithm';
import ReviewModal from './ReviewModal';

// ─── Props ────────────────────────────────────────────────────────────────────

interface ExamInterfaceProps {
  question: QuestionV2;
  elState: ELState;
  questionNumber: number;
  totalQuestions: number;
  sessionMode: 'adaptive' | 'timed' | 'review';
  timeLimitSeconds?: number;
  onAnswer: (choiceLabel: string, isCorrect: boolean, timeMs: number) => void;
  onNext: () => void;
  onSkip: () => void;
  onFlag: (questionId: string) => void;
  onEndSession: () => void;
}

// ─── Timer hook ───────────────────────────────────────────────────────────────

function useTimer(limitSeconds?: number, onExpire?: () => void) {
  const [elapsed, setElapsed] = useState(0);
  const ref = useRef<NodeJS.Timeout | null>(null);
  const startMs = useRef(Date.now());

  const reset = useCallback(() => {
    if (ref.current) clearInterval(ref.current);
    setElapsed(0);
    startMs.current = Date.now();
    ref.current = setInterval(() => {
      const s = Math.floor((Date.now() - startMs.current) / 1000);
      setElapsed(s);
      if (limitSeconds && s >= limitSeconds) {
        onExpire?.();
        if (ref.current) clearInterval(ref.current);
      }
    }, 500);
  }, [limitSeconds, onExpire]);

  const stop = useCallback(() => {
    if (ref.current) clearInterval(ref.current);
  }, []);

  const elapsedMs = useCallback(() => Date.now() - startMs.current, []);

  useEffect(() => {
    reset();
    return () => { if (ref.current) clearInterval(ref.current); };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return { elapsed, reset, stop, elapsedMs };
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function formatTime(s: number): string {
  const m = Math.floor(s / 60);
  const sec = s % 60;
  return `${m}:${sec.toString().padStart(2, '0')}`;
}

function difficultyBadge(d: number): { label: string; cls: string } {
  if (d <= 3)  return { label: `Lvl ${d} · Easy`,   cls: 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' };
  if (d <= 6)  return { label: `Lvl ${d} · Medium`, cls: 'bg-amber-500/20  text-amber-400  border-amber-500/30'  };
  if (d <= 8)  return { label: `Lvl ${d} · Hard`,   cls: 'bg-orange-500/20 text-orange-400 border-orange-500/30' };
  return              { label: `Lvl ${d} · Expert`, cls: 'bg-rose-500/20   text-rose-400   border-rose-500/30'   };
}

// ─── Component ────────────────────────────────────────────────────────────────

export default function ExamInterface({
  question,
  elState,
  questionNumber,
  totalQuestions,
  sessionMode,
  timeLimitSeconds,
  onAnswer,
  onNext,
  onSkip,
  onFlag,
  onEndSession,
}: ExamInterfaceProps) {
  const [selected, setSelected] = useState<string | null>(null);
  const [submitted, setSubmitted] = useState(false);
  const [flagged, setFlagged] = useState(false);
  const [showVideo, setShowVideo] = useState(false);
  const [showReviewModal, setShowReviewModal] = useState(false);
  const [panelTab, setPanelTab] = useState<'solution' | 'video' | 'stats'>('solution');
  const [elDelta, setElDelta] = useState<number | null>(null);

  const { elapsed, reset: resetTimer, stop: stopTimer, elapsedMs } = useTimer(
    sessionMode === 'timed' ? (timeLimitSeconds ?? question.estimatedSeconds * 3) : undefined,
    () => handleSubmit(true),
  );

  // Reset when question changes
  useEffect(() => {
    setSelected(null);
    setSubmitted(false);
    setFlagged(false);
    setShowVideo(false);
    setShowReviewModal(false);
    setPanelTab('solution');
    setElDelta(null);
    resetTimer();
  }, [question.id]); // eslint-disable-line react-hooks/exhaustive-deps

  function handleSelect(label: string) {
    if (submitted) return;
    setSelected(label);
  }

  function handleSubmit(timeUp = false) {
    if (submitted) return;
    const choice = timeUp ? null : selected;
    const correct = question.choices.find((c) => c.label === choice)?.correct ?? false;
    stopTimer();
    setSubmitted(true);
    setPanelTab('solution');

    // Compute EL delta for display
    const result = updateEL(
      elState,
      question.id,
      question.topicId,
      question.difficulty,
      correct,
    );
    setElDelta(result.delta);

    onAnswer(choice ?? '—', correct, elapsedMs());
  }

  function handleFlag() {
    setFlagged((f) => !f);
    onFlag(question.id);
  }

  const isCorrect = submitted
    ? question.choices.find((c) => c.label === selected)?.correct ?? false
    : null;

  const correctChoice = question.choices.find((c) => c.correct);
  const tier = elTierLabel(elState.earnedLevel);
  const badge = difficultyBadge(question.difficulty);
  const progressPct = ((questionNumber - 1) / totalQuestions) * 100;
  const timeWarning = timeLimitSeconds && elapsed > timeLimitSeconds * 0.75;

  const videoUrl = question.videoExplanation
    ? `https://www.youtube.com/embed/${question.videoExplanation.videoId}?start=${question.videoExplanation.timestampSeconds}&autoplay=1`
    : null;

  // ── Render ──────────────────────────────────────────────────────────────────
  return (
    <div className="flex flex-col h-screen bg-slate-950 text-slate-100 overflow-hidden">

      {/* ── Top bar ── */}
      <header className="flex items-center justify-between px-5 py-3 border-b border-slate-800 bg-slate-900/80 backdrop-blur shrink-0">
        {/* Left: session info */}
        <div className="flex items-center gap-4">
          <span className="text-xs font-semibold uppercase tracking-widest text-slate-500">
            Exam {question.exam}
          </span>
          <span className="text-xs text-slate-500">·</span>
          <span className="text-sm font-medium text-slate-300">
            {questionNumber} / {totalQuestions}
          </span>
          <div className="h-1 w-24 bg-slate-800 rounded-full overflow-hidden">
            <div
              className="h-full bg-indigo-500 rounded-full transition-all duration-300"
              style={{ width: `${progressPct}%` }}
            />
          </div>
        </div>

        {/* Center: EL display */}
        <div className="flex items-center gap-2 bg-slate-800 rounded-lg px-3 py-1.5">
          <Zap className="w-4 h-4 text-amber-400" />
          <span className="text-sm font-bold text-amber-400">
            EL {elState.earnedLevel.toFixed(2)}
          </span>
          <span className={`text-xs font-medium ${tier.color}`}>{tier.label}</span>
          {elDelta !== null && (
            <span className={`text-xs font-semibold ml-1 ${elDelta >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
              {elDelta >= 0 ? '+' : ''}{elDelta.toFixed(2)}
            </span>
          )}
        </div>

        {/* Right: timer + actions */}
        <div className="flex items-center gap-3">
          <div className={`flex items-center gap-1.5 text-sm font-mono font-semibold px-3 py-1 rounded-lg ${
            timeWarning ? 'bg-rose-500/20 text-rose-400' : 'bg-slate-800 text-slate-300'
          }`}>
            <Clock className="w-4 h-4" />
            {formatTime(elapsed)}
          </div>
          <button
            onClick={handleFlag}
            className={`p-2 rounded-lg transition-colors ${
              flagged ? 'bg-amber-500/20 text-amber-400' : 'text-slate-500 hover:text-slate-300 hover:bg-slate-800'
            }`}
            title="Flag for review"
          >
            <Flag className="w-4 h-4" />
          </button>
          <button
            onClick={onEndSession}
            className="text-xs text-slate-500 hover:text-slate-300 transition-colors px-2 py-1 rounded hover:bg-slate-800"
          >
            End Session
          </button>
        </div>
      </header>

      {/* ── Main split layout ── */}
      <div className="flex flex-1 min-h-0">

        {/* ════ LEFT PANE — Question ════ */}
        <div className={`flex flex-col transition-all duration-300 ${showVideo ? 'w-[58%]' : 'w-full'} border-r border-slate-800 overflow-y-auto`}>
          <div className="flex-1 px-8 py-7 max-w-3xl mx-auto w-full">

            {/* Topic + difficulty badges */}
            <div className="flex flex-wrap items-center gap-2 mb-5">
              <span className="text-xs bg-indigo-500/20 text-indigo-400 border border-indigo-500/30 rounded-full px-2.5 py-0.5 font-medium">
                {question.topicName}
              </span>
              <span className={`text-xs border rounded-full px-2.5 py-0.5 font-medium ${badge.cls}`}>
                {badge.label}
              </span>
              <span className="text-xs text-slate-500">~{Math.ceil(question.estimatedSeconds / 60)}m</span>
            </div>

            {/* Question stem */}
            <div
              className="text-base sm:text-lg leading-relaxed text-slate-100 mb-8 font-light"
              dangerouslySetInnerHTML={{ __html: question.stem }}
            />

            {/* Choices */}
            <div className="space-y-3">
              {question.choices.map((choice) => (
                <ChoiceButton
                  key={choice.label}
                  choice={choice}
                  selected={selected}
                  submitted={submitted}
                  onSelect={handleSelect}
                />
              ))}
            </div>

            {/* Submit / Skip row */}
            {!submitted && (
              <div className="flex items-center justify-between mt-8">
                <button
                  onClick={onSkip}
                  className="flex items-center gap-1.5 text-sm text-slate-500 hover:text-slate-300 transition-colors"
                >
                  <SkipForward className="w-4 h-4" />
                  Skip
                </button>
                <button
                  onClick={() => handleSubmit()}
                  disabled={!selected}
                  className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 disabled:cursor-not-allowed text-white font-semibold px-8 py-3 rounded-xl transition-colors"
                >
                  Submit Answer
                </button>
              </div>
            )}

            {/* Result banner */}
            {submitted && (
              <ResultBanner
                isCorrect={!!isCorrect}
                correctChoice={correctChoice}
                elDelta={elDelta}
                onNext={onNext}
                onWatchVideo={() => {
                  // Prefer the contextual API modal; fall back to static panel
                  if (question.topicId) {
                    setShowReviewModal(true);
                  } else {
                    setShowVideo(true);
                    setPanelTab('video');
                  }
                }}
                hasVideo
              />
            )}
          </div>
        </div>

        {/* ════ RIGHT PANE — Video / Solution / Stats ════ */}
        {showVideo && (
          <div className="flex flex-col w-[42%] bg-slate-900 overflow-hidden">

            {/* Panel header */}
            <div className="flex items-center justify-between px-5 py-3 border-b border-slate-800 shrink-0">
              <div className="flex items-center gap-1 bg-slate-800 rounded-lg p-0.5">
                {(['solution', 'video', 'stats'] as const).map((tab) => (
                  <button
                    key={tab}
                    onClick={() => setPanelTab(tab)}
                    className={`px-3 py-1.5 rounded-md text-xs font-semibold capitalize transition-colors ${
                      panelTab === tab
                        ? 'bg-slate-700 text-slate-100'
                        : 'text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    {tab === 'video' ? '▶ Video' : tab === 'solution' ? '⚡ Solution' : '📊 Stats'}
                  </button>
                ))}
              </div>
              <button
                onClick={() => setShowVideo(false)}
                className="text-slate-500 hover:text-slate-300 p-1 rounded-lg hover:bg-slate-800 transition-colors"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Panel content */}
            <div className="flex-1 overflow-y-auto">
              {panelTab === 'video' && <VideoPanel question={question} videoUrl={videoUrl} />}
              {panelTab === 'solution' && <SolutionPanel question={question} submitted={submitted} />}
              {panelTab === 'stats' && <StatsPanel elState={elState} question={question} />}
            </div>
          </div>
        )}

        {/* ── Floating panel toggle (when panel is hidden) ── */}
        {!showVideo && (
          <button
            onClick={() => setShowVideo(true)}
            className="fixed right-4 bottom-24 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl px-4 py-2.5 flex items-center gap-2 text-sm font-medium shadow-lg border border-slate-700 transition-colors"
          >
            <BookOpen className="w-4 h-4 text-indigo-400" />
            Resources
          </button>
        )}
      </div>

      {/* ── Contextual Review Modal ── */}
      {showReviewModal && (
        <ReviewModal
          topicId={question.topicDbId ?? 0}
          topicName={question.topicName}
          difficulty={question.difficulty}
          questionStem={question.stem.replace(/<[^>]*>/g, '')}
          onClose={() => setShowReviewModal(false)}
        />
      )}
    </div>
  );
}

// ─── Sub-components ───────────────────────────────────────────────────────────

function ChoiceButton({
  choice, selected, submitted, onSelect,
}: {
  choice: ChoiceV2;
  selected: string | null;
  submitted: boolean;
  onSelect: (l: string) => void;
}) {
  const isSelected = selected === choice.label;
  const isCorrect = choice.correct;

  let cls =
    'w-full flex items-start gap-4 px-5 py-4 rounded-xl border-2 text-left transition-all duration-150 ';

  if (submitted) {
    if (isCorrect)
      cls += 'border-emerald-500 bg-emerald-500/10 text-emerald-300';
    else if (isSelected)
      cls += 'border-rose-500 bg-rose-500/10 text-rose-300';
    else
      cls += 'border-slate-700 bg-slate-800/40 text-slate-500';
  } else if (isSelected) {
    cls += 'border-indigo-500 bg-indigo-500/15 text-slate-100 cursor-pointer';
  } else {
    cls += 'border-slate-700 bg-slate-800/50 text-slate-300 hover:border-slate-500 hover:bg-slate-800 cursor-pointer';
  }

  return (
    <button className={cls} onClick={() => onSelect(choice.label)} disabled={submitted}>
      <span className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold shrink-0 mt-0.5 ${
        submitted && isCorrect ? 'bg-emerald-500 text-white'
        : submitted && isSelected && !isCorrect ? 'bg-rose-500 text-white'
        : isSelected ? 'bg-indigo-600 text-white'
        : 'bg-slate-700 text-slate-400'
      }`}>
        {choice.label}
      </span>
      <span
        className="flex-1 leading-relaxed text-sm"
        dangerouslySetInnerHTML={{ __html: choice.text }}
      />
      {submitted && isCorrect && <CheckCircle className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />}
      {submitted && isSelected && !isCorrect && <XCircle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />}
    </button>
  );
}

function ResultBanner({
  isCorrect, correctChoice, elDelta, onNext, onWatchVideo, hasVideo,
}: {
  isCorrect: boolean;
  correctChoice?: ChoiceV2;
  elDelta: number | null;
  onNext: () => void;
  onWatchVideo: () => void;
  hasVideo: boolean;
}) {
  return (
    <div className={`mt-8 rounded-2xl border p-5 ${
      isCorrect ? 'bg-emerald-500/10 border-emerald-500/30' : 'bg-rose-500/10 border-rose-500/30'
    }`}>
      <div className="flex items-center gap-3 mb-3">
        {isCorrect
          ? <CheckCircle className="w-6 h-6 text-emerald-400 shrink-0" />
          : <XCircle    className="w-6 h-6 text-rose-400    shrink-0" />}
        <span className={`font-bold text-lg ${isCorrect ? 'text-emerald-400' : 'text-rose-400'}`}>
          {isCorrect ? 'Correct!' : `Incorrect — Answer: ${correctChoice?.label}`}
        </span>
        {elDelta !== null && (
          <span className={`ml-auto text-sm font-semibold px-2 py-0.5 rounded-lg ${
            elDelta >= 0 ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'
          }`}>
            EL {elDelta >= 0 ? '+' : ''}{elDelta.toFixed(2)}
          </span>
        )}
      </div>

      <div className="flex gap-3 mt-5">
        {hasVideo && (
          <button
            onClick={onWatchVideo}
            className="flex items-center gap-2 bg-indigo-600/80 hover:bg-indigo-600 text-white text-sm font-semibold px-4 py-2.5 rounded-xl transition-colors"
          >
            <PlayCircle className="w-4 h-4" />
            Watch Concept
          </button>
        )}
        <button
          onClick={onNext}
          className="flex items-center gap-2 bg-slate-700 hover:bg-slate-600 text-slate-100 text-sm font-semibold px-5 py-2.5 rounded-xl transition-colors ml-auto"
        >
          Next Question
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}

function VideoPanel({ question, videoUrl }: { question: QuestionV2; videoUrl: string | null }) {
  if (!question.videoExplanation || !videoUrl) {
    return (
      <div className="flex flex-col items-center justify-center h-64 text-slate-500 px-6 text-center">
        <Video className="w-10 h-10 mb-3 opacity-40" />
        <p className="text-sm">No video explanation available for this question yet.</p>
      </div>
    );
  }

  const v = question.videoExplanation;
  return (
    <div className="p-4">
      <div className="aspect-video rounded-xl overflow-hidden bg-black mb-4">
        <iframe
          src={videoUrl}
          className="w-full h-full"
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope"
          allowFullScreen
          title={v.clipTitle}
        />
      </div>
      <h3 className="text-sm font-semibold text-slate-200 mb-1">{v.clipTitle}</h3>
      <p className="text-xs text-slate-500">{v.channelName} · starts at {formatTime(v.timestampSeconds)}</p>
      <a
        href={v.url}
        target="_blank"
        rel="noopener noreferrer"
        className="mt-3 inline-flex items-center gap-1.5 text-xs text-indigo-400 hover:text-indigo-300 transition-colors"
      >
        <PlayCircle className="w-3.5 h-3.5" />
        Open on YouTube
      </a>
    </div>
  );
}

function SolutionPanel({ question, submitted }: { question: QuestionV2; submitted: boolean }) {
  if (!submitted) {
    return (
      <div className="flex flex-col items-center justify-center h-48 text-slate-500 px-6 text-center">
        <AlertCircle className="w-8 h-8 mb-2 opacity-40" />
        <p className="text-sm">Submit your answer to reveal the solution.</p>
      </div>
    );
  }

  return (
    <div className="p-5 space-y-5">
      {/* Calculation */}
      <div>
        <p className="text-xs font-semibold uppercase tracking-widest text-slate-500 mb-2">Calculation</p>
        <div
          className="text-sm text-slate-200 leading-relaxed bg-slate-800/60 rounded-xl p-4 border border-slate-700"
          dangerouslySetInnerHTML={{ __html: question.solution.calculation.replace(/\n/g, '<br/>') }}
        />
      </div>

      {/* Concept */}
      <div>
        <p className="text-xs font-semibold uppercase tracking-widest text-slate-500 mb-2">Key Concept</p>
        <div
          className="text-sm text-slate-300 leading-relaxed bg-indigo-500/10 rounded-xl p-4 border border-indigo-500/20 italic"
          dangerouslySetInnerHTML={{ __html: question.solution.concept }}
        />
      </div>

      {/* Common mistakes */}
      {question.solution.commonMistakes && question.solution.commonMistakes.length > 0 && (
        <div>
          <p className="text-xs font-semibold uppercase tracking-widest text-slate-500 mb-2">Common Mistakes</p>
          <ul className="space-y-1.5">
            {question.solution.commonMistakes.map((m, i) => (
              <li key={i} className="flex items-start gap-2 text-xs text-amber-300">
                <AlertCircle className="w-3.5 h-3.5 shrink-0 mt-0.5 text-amber-400" />
                {m}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Source */}
      <p className="text-xs text-slate-600">
        {question.source.reference} · {question.syllabusSection}
      </p>
    </div>
  );
}

function StatsPanel({ elState, question }: { elState: ELState; question: QuestionV2 }) {
  const topicEL = elState.topicEL[question.topicId] ?? elState.earnedLevel;
  const topicTier = elTierLabel(topicEL);
  const accuracy = elState.totalAnswered > 0
    ? Math.round((elState.totalCorrect / elState.totalAnswered) * 100)
    : 0;

  const recentDelta = elState.recentHistory.reduce((s, e) => s + e.delta, 0);

  return (
    <div className="p-5 space-y-4">
      <div>
        <p className="text-xs font-semibold uppercase tracking-widest text-slate-500 mb-3">Session Progress</p>
        <div className="grid grid-cols-2 gap-3">
          {[
            { label: 'Overall EL', value: elState.earnedLevel.toFixed(2), color: 'text-amber-400' },
            { label: `${question.topicName} EL`, value: topicEL.toFixed(2), color: topicTier.color },
            { label: 'Accuracy',   value: `${accuracy}%`,                 color: accuracy >= 70 ? 'text-emerald-400' : 'text-rose-400' },
            { label: 'Answered',   value: elState.totalAnswered,           color: 'text-slate-300' },
          ].map((stat) => (
            <div key={stat.label} className="bg-slate-800/60 rounded-xl p-3 border border-slate-700">
              <p className="text-xs text-slate-500 mb-1">{stat.label}</p>
              <p className={`text-xl font-bold ${stat.color}`}>{stat.value}</p>
            </div>
          ))}
        </div>
      </div>

      {/* EL trend sparkline (last 10 events) */}
      {elState.recentHistory.length > 1 && (
        <div>
          <p className="text-xs font-semibold uppercase tracking-widest text-slate-500 mb-2">Recent EL Trend</p>
          <div className="flex items-end gap-1 h-12">
            {elState.recentHistory.slice(0, 10).reverse().map((e, i) => {
              const h = Math.max(4, Math.round(((e.elAfter - 1) / 9) * 48));
              return (
                <div
                  key={i}
                  title={`Q${i + 1}: ${e.isCorrect ? '✓' : '✗'} EL ${e.elAfter.toFixed(2)}`}
                  className={`flex-1 rounded-sm transition-all ${e.isCorrect ? 'bg-emerald-500' : 'bg-rose-500'}`}
                  style={{ height: `${h}px` }}
                />
              );
            })}
          </div>
          <p className={`text-xs mt-1 ${recentDelta >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
            {recentDelta >= 0 ? '↑' : '↓'} {Math.abs(recentDelta).toFixed(2)} EL over last {elState.recentHistory.length} questions
          </p>
        </div>
      )}

      <div className="text-xs text-slate-600 leading-relaxed">
        <Info className="w-3 h-3 inline mr-1" />
        EL adjusts using an Elo-style algorithm. Answering harder questions correctly moves your level up faster.
      </div>
    </div>
  );
}
