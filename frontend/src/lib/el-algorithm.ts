/**
 * Earned Level (EL) Algorithm
 *
 * Built on an Elo-style rating system adapted for actuarial exam prep.
 *
 * Scale: EL 1.0–10.0 (continuous), stored as a float.
 * Question difficulty: 1–10 integer.
 *
 * The K-factor scales with the "surprise" of the result:
 *   - Answering a question far above your EL correctly → large gain
 *   - Getting a question far below your EL wrong → large loss
 *   - Expected outcomes (near your EL) → small adjustment
 */

export interface ELState {
  earnedLevel: number;          // 1.0 – 10.0
  totalAnswered: number;
  totalCorrect: number;
  topicEL: Record<string, number>; // per-topic sub-ratings
  recentHistory: ELEvent[];        // last 20 events for trend display
}

export interface ELEvent {
  questionId: string;
  difficulty: number;
  isCorrect: boolean;
  elBefore: number;
  elAfter: number;
  delta: number;
  topicId: string;
  timestamp: number;
}

export interface ELUpdateResult {
  newEL: number;
  newTopicEL: number;
  delta: number;
  topicDelta: number;
  expectedScore: number;
  kFactor: number;
}

const EL_MIN = 1.0;
const EL_MAX = 10.0;
const SPREAD = 2.5; // controls how steep the sigmoid is on a 1-10 scale

/**
 * Expected score probability: P(correct) given student EL and question difficulty.
 * Maps to the Elo expected-score formula with spread tuned for a 1-10 scale.
 */
export function expectedScore(studentEL: number, questionDifficulty: number): number {
  return 1 / (1 + Math.pow(10, (questionDifficulty - studentEL) / SPREAD));
}

/**
 * K-factor: maximum rating points exchangeable per question.
 * Scales with total questions answered (higher K early → faster calibration).
 * Also scales with the absolute difficulty gap to reward/punish "upsets."
 */
function kFactor(totalAnswered: number, difficultyGap: number): number {
  // Base K decreases as we accumulate more data (like Elo provisional → established)
  const baseK = totalAnswered < 20 ? 1.2 : totalAnswered < 50 ? 0.8 : 0.5;

  // Amplify K when the gap is large (answering well above/below your level)
  const gapMultiplier = 1 + 0.15 * Math.abs(difficultyGap);

  return baseK * gapMultiplier;
}

/**
 * Core EL update function.
 * Returns the new overall EL and the per-topic EL for the given question.
 */
export function updateEL(
  state: ELState,
  questionId: string,
  topicId: string,
  questionDifficulty: number,
  isCorrect: boolean,
): ELUpdateResult {
  const actual = isCorrect ? 1 : 0;
  const currentTopicEL = state.topicEL[topicId] ?? state.earnedLevel;

  // Global EL update
  const expected = expectedScore(state.earnedLevel, questionDifficulty);
  const gap = questionDifficulty - state.earnedLevel;
  const K = kFactor(state.totalAnswered, gap);
  const delta = K * (actual - expected);
  const newEL = Math.min(EL_MAX, Math.max(EL_MIN, state.earnedLevel + delta));

  // Per-topic EL update (uses same formula, independent tracking)
  const topicExpected = expectedScore(currentTopicEL, questionDifficulty);
  const topicGap = questionDifficulty - currentTopicEL;
  const topicK = kFactor(state.totalAnswered, topicGap);
  const topicDelta = topicK * (actual - topicExpected);
  const newTopicEL = Math.min(EL_MAX, Math.max(EL_MIN, currentTopicEL + topicDelta));

  return {
    newEL: Math.round(newEL * 100) / 100,
    newTopicEL: Math.round(newTopicEL * 100) / 100,
    delta: Math.round(delta * 100) / 100,
    topicDelta: Math.round(topicDelta * 100) / 100,
    expectedScore: Math.round(expected * 1000) / 1000,
    kFactor: Math.round(K * 100) / 100,
  };
}

/**
 * Apply an EL update result back into the state, returning the new state.
 */
export function applyELUpdate(
  state: ELState,
  questionId: string,
  topicId: string,
  questionDifficulty: number,
  isCorrect: boolean,
): ELState {
  const result = updateEL(state, questionId, topicId, questionDifficulty, isCorrect);

  const event: ELEvent = {
    questionId,
    difficulty: questionDifficulty,
    isCorrect,
    elBefore: state.earnedLevel,
    elAfter: result.newEL,
    delta: result.delta,
    topicId,
    timestamp: Date.now(),
  };

  return {
    earnedLevel: result.newEL,
    totalAnswered: state.totalAnswered + 1,
    totalCorrect: state.totalCorrect + (isCorrect ? 1 : 0),
    topicEL: { ...state.topicEL, [topicId]: result.newTopicEL },
    recentHistory: [event, ...state.recentHistory].slice(0, 20),
  };
}

/**
 * Select the optimal next question difficulty for maximum learning.
 * Targets questions slightly above the student's current EL (desirable difficulty).
 * Adds controlled randomness to prevent staleness.
 */
export function targetDifficulty(el: number): { min: number; max: number; ideal: number } {
  // Ideal challenge: 0.5–1.5 above current EL, clamped to 1–10
  const ideal = Math.min(EL_MAX, Math.round((el + 0.8) * 2) / 2);
  const min = Math.max(EL_MIN, Math.floor(el - 0.5));
  const max = Math.min(EL_MAX, Math.ceil(el + 2.0));
  return { ideal, min, max };
}

/**
 * Human-readable EL tier label.
 */
export function elTierLabel(el: number): { label: string; color: string } {
  if (el < 2.5) return { label: 'Beginner',      color: 'text-slate-400' };
  if (el < 4.0) return { label: 'Developing',    color: 'text-blue-400' };
  if (el < 5.5) return { label: 'Proficient',    color: 'text-teal-400' };
  if (el < 7.0) return { label: 'Advanced',      color: 'text-amber-400' };
  if (el < 8.5) return { label: 'Expert',        color: 'text-orange-400' };
  return             { label: 'Master',          color: 'text-rose-400' };
}

export function initialELState(seedEL = 3.0): ELState {
  return {
    earnedLevel: seedEL,
    totalAnswered: 0,
    totalCorrect: 0,
    topicEL: {},
    recentHistory: [],
  };
}
