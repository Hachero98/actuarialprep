'use client';

import { useState, useEffect, useCallback } from 'react';
import {
  X, PlayCircle, Video, ExternalLink, AlertCircle,
  ChevronLeft, ChevronRight, Loader2, Info,
} from 'lucide-react';

// ─── Types ────────────────────────────────────────────────────────────────────

interface VideoClip {
  clip_id: number;
  lesson_id: number;
  topic_id: number;
  title: string;
  description: string | null;
  channel_name: string | null;
  youtube_video_id: string | null;
  start_seconds: number;
  end_seconds: number;
  duration_seconds: number;
  /** Primary embed URL — use this for the iframe src */
  video_url: string;
  /** Alias of start_seconds — content layer contract */
  timestamp_start: number;
  youtube_url: string | null;
  concept_tags: string[];
  min_difficulty: number;
  max_difficulty: number;
  subtopic_slug?: string | null;
}

interface ContextualVideoResponse {
  topic_id: number;
  subtopic_slug?: string | null;
  difficulty: number;
  clips: VideoClip[];
  fallback: boolean;
  seed_template_ids: string[];
}

interface ReviewModalProps {
  topicId: number;
  topicName: string;
  /** subtopic_slug e.g. "redington-immunization" — sent to /api/get-contextual-video */
  subtopicSlug?: string;
  difficulty: number;
  questionStem: string;
  onClose: () => void;
  /** Defaults to /api — matches the FastAPI /api/get-contextual-video route */
  apiBase?: string;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function formatSeconds(s: number): string {
  const m = Math.floor(s / 60);
  const sec = s % 60;
  return `${m}:${sec.toString().padStart(2, '0')}`;
}

function difficultyLabel(min: number, max: number): string {
  return `Lvl ${min}–${max}`;
}

// ─── Component ────────────────────────────────────────────────────────────────

export default function ReviewModal({
  topicId,
  topicName,
  subtopicSlug,
  difficulty,
  questionStem,
  onClose,
  apiBase = '/api',
}: ReviewModalProps) {
  const [data, setData] = useState<ContextualVideoResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeClipIdx, setActiveClipIdx] = useState(0);

  const fetchClips = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      // Use the Intelligent Content Layer endpoint when subtopicSlug is available,
      // falling back to the legacy lessons endpoint otherwise.
      const params = new URLSearchParams({
        topic_id: String(topicId),
        difficulty: String(difficulty),
        limit: '3',
        ...(subtopicSlug ? { subtopic_slug: subtopicSlug } : {}),
      });
      const endpoint = subtopicSlug
        ? `${apiBase}/get-contextual-video`
        : `${apiBase}/lessons/contextual-video`;
      const res = await fetch(`${endpoint}?${params}`, { credentials: 'include' });
      if (!res.ok) throw new Error(`API error ${res.status}`);
      const json: ContextualVideoResponse = await res.json();
      setData(json);
      setActiveClipIdx(0);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load video clips.');
    } finally {
      setLoading(false);
    }
  }, [apiBase, topicId, difficulty]);

  useEffect(() => { fetchClips(); }, [fetchClips]);

  // Close on Escape
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [onClose]);

  const activeClip = data?.clips[activeClipIdx] ?? null;

  return (
    /* Backdrop */
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4"
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
    >
      <div className="relative w-full max-w-3xl bg-slate-900 rounded-2xl border border-slate-700 shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">

        {/* ── Header ── */}
        <div className="flex items-start justify-between px-6 py-4 border-b border-slate-800 shrink-0">
          <div className="flex-1 min-w-0 mr-4">
            <div className="flex items-center gap-2 mb-1">
              <Video className="w-4 h-4 text-indigo-400 shrink-0" />
              <span className="text-xs font-semibold uppercase tracking-widest text-indigo-400">
                Concept Review
              </span>
              <span className="text-xs text-slate-500">·</span>
              <span className="text-xs text-slate-400">{topicName}</span>
            </div>
            <p className="text-sm text-slate-400 line-clamp-2 leading-snug">{questionStem}</p>
          </div>
          <button
            onClick={onClose}
            className="text-slate-500 hover:text-slate-200 p-1.5 rounded-lg hover:bg-slate-800 transition-colors shrink-0"
            aria-label="Close"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* ── Body ── */}
        <div className="flex-1 overflow-y-auto">

          {/* Loading */}
          {loading && (
            <div className="flex flex-col items-center justify-center py-20 text-slate-500">
              <Loader2 className="w-8 h-8 animate-spin mb-3 text-indigo-500" />
              <p className="text-sm">Finding the best video for this concept…</p>
            </div>
          )}

          {/* Error */}
          {!loading && error && (
            <div className="flex flex-col items-center justify-center py-16 px-6 text-center text-slate-500">
              <AlertCircle className="w-8 h-8 mb-3 text-rose-400" />
              <p className="text-sm text-rose-300 mb-4">{error}</p>
              <button
                onClick={fetchClips}
                className="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 px-4 py-2 rounded-lg transition-colors"
              >
                Try again
              </button>
            </div>
          )}

          {/* No clips */}
          {!loading && !error && data && data.clips.length === 0 && (
            <div className="flex flex-col items-center justify-center py-16 px-6 text-center text-slate-500">
              <Video className="w-10 h-10 mb-3 opacity-30" />
              <p className="text-sm">No video explanations available for this topic yet.</p>
              <p className="text-xs mt-1 text-slate-600">Check back soon — we're adding content regularly.</p>
            </div>
          )}

          {/* Content */}
          {!loading && !error && activeClip && data && (
            <div className="p-5 space-y-4">

              {/* Fallback notice */}
              {data.fallback && (
                <div className="flex items-start gap-2 bg-amber-500/10 border border-amber-500/20 rounded-xl px-4 py-3 text-xs text-amber-300">
                  <Info className="w-3.5 h-3.5 shrink-0 mt-0.5 text-amber-400" />
                  No exact match found — showing the closest related videos from this topic area.
                </div>
              )}

              {/* Video embed */}
              <div className="aspect-video rounded-xl overflow-hidden bg-black border border-slate-800">
                {activeClip.youtube_video_id ? (
                  <iframe
                    key={activeClip.clip_id}
                    src={activeClip.video_url}
                    className="w-full h-full"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                    title={activeClip.title}
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center text-slate-600">
                    <Video className="w-12 h-12 opacity-30" />
                  </div>
                )}
              </div>

              {/* Clip metadata */}
              <div className="flex items-start justify-between gap-3">
                <div className="flex-1 min-w-0">
                  <h3 className="text-sm font-semibold text-slate-100 leading-tight mb-1">
                    {activeClip.title}
                  </h3>
                  <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500">
                    {activeClip.channel_name && (
                      <span className="text-slate-400">{activeClip.channel_name}</span>
                    )}
                    <span>·</span>
                    <span>{formatSeconds(activeClip.timestamp_start)} – {formatSeconds(activeClip.end_seconds)}</span>
                    <span>·</span>
                    <span>{Math.round(activeClip.duration_seconds / 60)} min</span>
                    <span className="bg-slate-800 text-slate-400 rounded px-1.5 py-0.5">
                      {difficultyLabel(activeClip.min_difficulty, activeClip.max_difficulty)}
                    </span>
                  </div>
                  {activeClip.description && (
                    <p className="text-xs text-slate-500 mt-2 leading-relaxed line-clamp-2">
                      {activeClip.description}
                    </p>
                  )}
                  {activeClip.concept_tags.length > 0 && (
                    <div className="flex flex-wrap gap-1.5 mt-2">
                      {activeClip.concept_tags.map((tag) => (
                        <span
                          key={tag}
                          className="text-[11px] bg-indigo-500/15 text-indigo-400 border border-indigo-500/25 rounded-full px-2 py-0.5"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                {activeClip.youtube_url && (
                  <a
                    href={activeClip.youtube_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-1.5 text-xs text-indigo-400 hover:text-indigo-300 transition-colors shrink-0 mt-0.5"
                  >
                    <ExternalLink className="w-3.5 h-3.5" />
                    YouTube
                  </a>
                )}
              </div>

              {/* Multi-clip navigation */}
              {data.clips.length > 1 && (
                <div className="border-t border-slate-800 pt-4">
                  <p className="text-xs font-semibold uppercase tracking-widest text-slate-500 mb-3">
                    More Clips ({data.clips.length})
                  </p>
                  <div className="space-y-2">
                    {data.clips.map((clip, idx) => (
                      <button
                        key={clip.clip_id}
                        onClick={() => setActiveClipIdx(idx)}
                        className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl border text-left transition-all text-sm ${
                          idx === activeClipIdx
                            ? 'border-indigo-500/50 bg-indigo-500/10 text-slate-100'
                            : 'border-slate-800 bg-slate-800/40 text-slate-400 hover:border-slate-700 hover:text-slate-200'
                        }`}
                      >
                        <PlayCircle className={`w-4 h-4 shrink-0 ${idx === activeClipIdx ? 'text-indigo-400' : 'text-slate-600'}`} />
                        <span className="flex-1 truncate font-medium">{clip.title}</span>
                        <span className="text-xs text-slate-600 shrink-0">
                          {Math.round(clip.duration_seconds / 60)}m
                        </span>
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {/* ── Footer ── */}
        <div className="flex items-center justify-between px-6 py-4 border-t border-slate-800 shrink-0">
          <p className="text-xs text-slate-600">
            Videos are matched to the difficulty and topic of the question you missed.
          </p>
          <button
            onClick={onClose}
            className="bg-slate-800 hover:bg-slate-700 text-slate-200 text-sm font-medium px-5 py-2 rounded-xl transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
