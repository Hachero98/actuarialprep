/**
 * Spaced Repetition Engine (SM-2 variant)
 *
 * Resurfaces questions the user got wrong on an expanding schedule:
 *   First wrong: review in 3 days
 *   Still struggling (ease < 2.0): stay at 3 days
 *   Correct once: review in 7 days
 *   Subsequent correct: interval *= ease_factor
 *
 * Ease factor adjusts based on answer quality (0–5 scale, mapped from correct/incorrect + EL gap).
 */

export interface SRCard {
  questionId: string;
  topicId: string;
  interval: number;       // days until next review
  easeFactor: number;     // 1.3 – 2.5 (SM-2 default: 2.5)
  repetitions: number;    // consecutive correct answers
  dueDate: number;        // Unix ms timestamp
  lastReviewed: number;   // Unix ms timestamp
}

export interface SRStore {
  cards: Record<string, SRCard>; // keyed by questionId
}

const MIN_EASE = 1.3;
const MAX_EASE = 2.5;
const DEFAULT_EASE = 2.5;

/**
 * Convert a correct/incorrect answer + difficulty gap into SM-2 quality (0–5).
 * Quality ≥ 3 is considered a passing review.
 */
function answerQuality(isCorrect: boolean, difficultyGap: number): number {
  if (!isCorrect) {
    // Wrong: quality 0 (completely forgot) or 1 (wrong but close)
    return difficultyGap > 2 ? 1 : 0;
  }
  // Correct: quality 3–5 based on how hard the question was relative to EL
  if (difficultyGap >= 2) return 5; // crushed a hard question
  if (difficultyGap >= 0) return 4; // answered at or above level
  return 3;                          // answered below level (expected)
}

/**
 * SM-2 new ease factor formula.
 */
function newEaseFactor(current: number, quality: number): number {
  const next = current + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02));
  return Math.min(MAX_EASE, Math.max(MIN_EASE, next));
}

/**
 * SM-2 interval calculation.
 */
function nextInterval(card: SRCard, quality: number): number {
  if (quality < 3) {
    // Failed: reset to 1 day (or 3 for first-time failures)
    return card.repetitions === 0 ? 3 : 1;
  }
  if (card.repetitions === 0) return 3;
  if (card.repetitions === 1) return 7;
  return Math.round(card.interval * card.easeFactor);
}

/**
 * Process a question answer and update the SRCard for that question.
 */
export function processAnswer(
  store: SRStore,
  questionId: string,
  topicId: string,
  isCorrect: boolean,
  studentEL: number,
  questionDifficulty: number,
): SRStore {
  const existing = store.cards[questionId] ?? {
    questionId,
    topicId,
    interval: 0,
    easeFactor: DEFAULT_EASE,
    repetitions: 0,
    dueDate: 0,
    lastReviewed: 0,
  };

  const gap = questionDifficulty - studentEL;
  const quality = answerQuality(isCorrect, gap);
  const newEase = newEaseFactor(existing.easeFactor, quality);
  const interval = nextInterval(existing, quality);
  const now = Date.now();
  const MS_PER_DAY = 86_400_000;

  const updated: SRCard = {
    ...existing,
    interval,
    easeFactor: newEase,
    repetitions: quality >= 3 ? existing.repetitions + 1 : 0,
    dueDate: now + interval * MS_PER_DAY,
    lastReviewed: now,
  };

  return { cards: { ...store.cards, [questionId]: updated } };
}

/**
 * Return question IDs that are due for review today (dueDate <= now).
 * Sorted by overdue amount descending (most overdue first).
 */
export function getDueCards(store: SRStore, limit = 20): SRCard[] {
  const now = Date.now();
  return Object.values(store.cards)
    .filter((c) => c.dueDate <= now)
    .sort((a, b) => a.dueDate - b.dueDate)
    .slice(0, limit);
}

/**
 * Count how many cards are due today.
 */
export function dueTodayCount(store: SRStore): number {
  const now = Date.now();
  return Object.values(store.cards).filter((c) => c.dueDate <= now).length;
}

/**
 * Return upcoming review schedule: next 14 days.
 */
export function upcomingSchedule(store: SRStore): Array<{ date: string; count: number }> {
  const now = Date.now();
  const MS_PER_DAY = 86_400_000;
  const schedule: Record<number, number> = {};

  for (const card of Object.values(store.cards)) {
    const daysAhead = Math.ceil((card.dueDate - now) / MS_PER_DAY);
    if (daysAhead >= 0 && daysAhead < 14) {
      schedule[daysAhead] = (schedule[daysAhead] ?? 0) + 1;
    }
  }

  return Array.from({ length: 14 }, (_, i) => ({
    date: new Date(now + i * MS_PER_DAY).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    count: schedule[i] ?? 0,
  }));
}

export function initialSRStore(): SRStore {
  return { cards: {} };
}
