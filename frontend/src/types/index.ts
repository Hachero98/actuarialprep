export interface User {
  id: string;
  name: string;
  email: string;
  role: 'user' | 'admin';
  createdAt: string;
  updatedAt: string;
}

export interface Exam {
  code: string;
  name: string;
  description: string;
  totalQuestions: number;
  duration: number;
  topics: Topic[];
}

export interface Topic {
  id: string;
  name: string;
  description: string;
  examCode: string;
  questionCount: number;
  mastery: number;
}

export interface Question {
  id: string;
  examCode: string;
  topicId: string;
  text: string;
  difficulty: 'easy' | 'medium' | 'hard';
  choices: Choice[];
  explanation: string;
  correctChoiceId: string;
}

export interface Choice {
  id: string;
  label: string;
  text: string;
}

export interface QuestionResponse {
  questionId: string;
  selectedChoiceId: string;
  isCorrect: boolean;
  timeSpent: number;
}

export interface AnswerResponse {
  id: string;
  userId: string;
  questionId: string;
  selectedChoiceId: string;
  isCorrect: boolean;
  explanation: string;
  difficulty: 'easy' | 'medium' | 'hard';
  timeSpent: number;
  createdAt: string;
}

export interface AdaptiveState {
  currentDifficulty: 'easy' | 'medium' | 'hard';
  correctStreak: number;
  topicMastery: Record<string, number>;
  nextQuestionTopic: string;
  recommendedDifficulty: 'easy' | 'medium' | 'hard';
}

export interface PracticeSession {
  id: string;
  userId: string;
  examCode: string;
  startTime: string;
  endTime?: string;
  questionsAnswered: number;
  correctAnswers: number;
  accuracy: number;
  state: AdaptiveState;
}

export interface StudyPlan {
  id: string;
  userId: string;
  examCode: string;
  startDate: string;
  endDate: string;
  targetCompletionDate: string;
  dailyPlans: DailyPlan[];
  topics: TopicBreakdown[];
}

export interface DailyPlan {
  date: string;
  topicsToStudy: string[];
  videoLessonsToWatch: string[];
  questionsToAnswer: number;
  completed: boolean;
}

export interface VideoLesson {
  id: string;
  title: string;
  description: string;
  examCode: string;
  topicId: string;
  duration: number;
  url: string;
  watched: boolean;
  progress: number;
}

export interface ProgressSummary {
  userId: string;
  examCode: string;
  totalQuestionsAnswered: number;
  correctAnswers: number;
  overallAccuracy: number;
  readinessScore: number;
  weakTopics: TopicBreakdown[];
  strongTopics: TopicBreakdown[];
  lastPracticeDate: string;
  studyStreak: number;
}

export interface TopicBreakdown {
  topicId: string;
  topicName: string;
  mastery: number;
  questionsAnswered: number;
  correctAnswers: number;
  accuracy: number;
}

export interface ReadinessAssessment {
  examCode: string;
  readinessScore: number;
  recommendation: 'not_ready' | 'prepare' | 'ready' | 'well_prepared';
  estimatedPassRate: number;
  weakAreas: string[];
  strengthAreas: string[];
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresIn: number;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  name: string;
  email: string;
  password: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
}
