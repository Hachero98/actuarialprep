import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import { User, AuthTokens, Question, PracticeSession, AdaptiveState } from '@/types';
import { ELState, initialELState, applyELUpdate } from '@/lib/el-algorithm';
import { SRStore, initialSRStore, processAnswer as srProcessAnswer } from '@/lib/spaced-repetition';

interface AuthState {
  user: User | null;
  accessToken: string | null;
  refreshToken: string | null;
  isLoading: boolean;
  error: string | null;
  setUser: (user: User | null) => void;
  setTokens: (tokens: AuthTokens) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  logout: () => void;
}

interface ExamSessionState {
  sessionId: string | null;
  examCode: string | null;
  currentQuestion: Question | null;
  currentQuestionIndex: number;
  totalQuestions: number;
  answeredQuestions: number[];
  timeElapsed: number;
  adaptiveState: AdaptiveState | null;
  isLoading: boolean;
  showResult: boolean;
  lastAnswer: { questionId: string; isCorrect: boolean } | null;

  startSession: (examCode: string, sessionId: string) => void;
  setCurrentQuestion: (question: Question) => void;
  submitAnswer: (questionId: string, isCorrect: boolean) => void;
  nextQuestion: () => void;
  setAdaptiveState: (state: AdaptiveState) => void;
  setTimeElapsed: (time: number) => void;
  setIsLoading: (loading: boolean) => void;
  endSession: () => void;
  reset: () => void;
}

interface UiState {
  sidebarOpen: boolean;
  theme: 'light' | 'dark';
  setSidebarOpen: (open: boolean) => void;
  setTheme: (theme: 'light' | 'dark') => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  accessToken: null,
  refreshToken: null,
  isLoading: false,
  error: null,

  setUser: (user) => set({ user }),

  setTokens: (tokens) =>
    set({
      accessToken: tokens.accessToken,
      refreshToken: tokens.refreshToken,
    }),

  setLoading: (loading) => set({ isLoading: loading }),

  setError: (error) => set({ error }),

  logout: () =>
    set({
      user: null,
      accessToken: null,
      refreshToken: null,
      error: null,
    }),
}));

export const useExamSessionStore = create<ExamSessionState>((set) => ({
  sessionId: null,
  examCode: null,
  currentQuestion: null,
  currentQuestionIndex: 0,
  totalQuestions: 0,
  answeredQuestions: [],
  timeElapsed: 0,
  adaptiveState: null,
  isLoading: false,
  showResult: false,
  lastAnswer: null,

  startSession: (examCode, sessionId) =>
    set({
      examCode,
      sessionId,
      currentQuestionIndex: 0,
      answeredQuestions: [],
      timeElapsed: 0,
      showResult: false,
      lastAnswer: null,
    }),

  setCurrentQuestion: (question) => set({ currentQuestion: question, showResult: false }),

  submitAnswer: (questionId, isCorrect) =>
    set((state) => ({
      answeredQuestions: [...state.answeredQuestions, questionId],
      showResult: true,
      lastAnswer: { questionId, isCorrect },
    })),

  nextQuestion: () =>
    set((state) => ({
      currentQuestionIndex: state.currentQuestionIndex + 1,
      currentQuestion: null,
      showResult: false,
    })),

  setAdaptiveState: (state) => set({ adaptiveState: state }),

  setTimeElapsed: (time) => set({ timeElapsed: time }),

  setIsLoading: (loading) => set({ isLoading: loading }),

  endSession: () =>
    set({
      sessionId: null,
      examCode: null,
      currentQuestion: null,
      currentQuestionIndex: 0,
    }),

  reset: () =>
    set({
      sessionId: null,
      examCode: null,
      currentQuestion: null,
      currentQuestionIndex: 0,
      totalQuestions: 0,
      answeredQuestions: [],
      timeElapsed: 0,
      adaptiveState: null,
      isLoading: false,
      showResult: false,
      lastAnswer: null,
    }),
}));

// ── Earned Level store (persisted to localStorage) ───────────────────────────
interface ELStoreState {
  byExam: Record<string, ELState>;
  getExamEL: (exam: string) => ELState;
  recordAnswer: (
    exam: string,
    questionId: string,
    topicId: string,
    difficulty: number,
    isCorrect: boolean,
  ) => void;
  resetExam: (exam: string) => void;
}

export const useELStore = create<ELStoreState>()(
  persist(
    (set, get) => ({
      byExam: {},

      getExamEL: (exam) => get().byExam[exam] ?? initialELState(3.0),

      recordAnswer: (exam, questionId, topicId, difficulty, isCorrect) =>
        set((state) => {
          const current = state.byExam[exam] ?? initialELState(3.0);
          const updated = applyELUpdate(current, questionId, topicId, difficulty, isCorrect);
          return { byExam: { ...state.byExam, [exam]: updated } };
        }),

      resetExam: (exam) =>
        set((state) => ({
          byExam: { ...state.byExam, [exam]: initialELState(3.0) },
        })),
    }),
    { name: 'ap-el-store' },
  ),
);

// ── Spaced Repetition store (persisted to localStorage) ──────────────────────
interface SRStoreState {
  store: SRStore;
  processAnswer: (
    questionId: string,
    topicId: string,
    isCorrect: boolean,
    studentEL: number,
    difficulty: number,
  ) => void;
}

export const useSRStore = create<SRStoreState>()(
  persist(
    (set, get) => ({
      store: initialSRStore(),

      processAnswer: (questionId, topicId, isCorrect, studentEL, difficulty) =>
        set((state) => ({
          store: srProcessAnswer(
            state.store,
            questionId,
            topicId,
            isCorrect,
            studentEL,
            difficulty,
          ),
        })),
    }),
    { name: 'ap-sr-store' },
  ),
);

export const useUiStore = create<UiState>((set) => ({
  sidebarOpen: true,
  theme: 'light',

  setSidebarOpen: (open) => set({ sidebarOpen: open }),

  setTheme: (theme) => set({ theme }),
}));
