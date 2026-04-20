import axios, { AxiosInstance, AxiosError } from 'axios';
import {
  User,
  Question,
  AnswerResponse,
  AdaptiveState,
  LoginRequest,
  RegisterRequest,
  AuthTokens,
  StudyPlan,
  ProgressSummary,
  ReadinessAssessment,
  VideoLesson,
} from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api';

interface ApiClient extends AxiosInstance {
  setAuthToken: (token: string) => void;
  removeAuthToken: () => void;
}

const createApiClient = (): ApiClient => {
  const client = axios.create({
    baseURL: API_BASE_URL,
    headers: {
      'Content-Type': 'application/json',
    },
  }) as ApiClient;

  // Request interceptor to attach JWT token
  client.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('accessToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  // Response interceptor for token refresh
  client.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
      const originalRequest = error.config as any;

      if (error.response?.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true;

        try {
          const refreshToken = localStorage.getItem('refreshToken');
          if (!refreshToken) {
            throw new Error('No refresh token available');
          }

          const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
            refreshToken,
          });

          const { accessToken } = response.data.data;
          localStorage.setItem('accessToken', accessToken);
          client.setAuthToken(accessToken);

          originalRequest.headers.Authorization = `Bearer ${accessToken}`;
          return client(originalRequest);
        } catch (refreshError) {
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
          window.location.href = '/login';
          return Promise.reject(refreshError);
        }
      }

      return Promise.reject(error);
    }
  );

  client.setAuthToken = (token: string) => {
    client.defaults.headers.common.Authorization = `Bearer ${token}`;
    localStorage.setItem('accessToken', token);
  };

  client.removeAuthToken = () => {
    delete client.defaults.headers.common.Authorization;
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  };

  return client;
};

export const api = createApiClient();

// Auth endpoints
export const authApi = {
  login: async (credentials: LoginRequest): Promise<AuthTokens & { user: User }> => {
    const response = await api.post('/auth/login', credentials);
    return response.data.data;
  },

  register: async (data: RegisterRequest): Promise<AuthTokens & { user: User }> => {
    const response = await api.post('/auth/register', data);
    return response.data.data;
  },

  refreshToken: async (refreshToken: string): Promise<AuthTokens> => {
    const response = await api.post('/auth/refresh', { refreshToken });
    return response.data.data;
  },

  logout: async (): Promise<void> => {
    await api.post('/auth/logout');
  },

  getCurrentUser: async (): Promise<User> => {
    const response = await api.get('/auth/me');
    return response.data.data;
  },
};

// Question endpoints
export const questionApi = {
  generateQuestion: async (
    examCode: string,
    difficulty: string,
    topicId?: string
  ): Promise<Question> => {
    const response = await api.post('/questions/generate', {
      examCode,
      difficulty,
      topicId,
    });
    return response.data.data;
  },

  submitAnswer: async (
    questionId: string,
    selectedChoiceId: string
  ): Promise<AnswerResponse> => {
    const response = await api.post('/answers/submit', {
      questionId,
      selectedChoiceId,
    });
    return response.data.data;
  },

  getQuestion: async (questionId: string): Promise<Question> => {
    const response = await api.get(`/questions/${questionId}`);
    return response.data.data;
  },

  getQuestions: async (examCode: string, limit: number = 10): Promise<Question[]> => {
    const response = await api.get(`/questions`, {
      params: { examCode, limit },
    });
    return response.data.data;
  },
};

// Adaptive learning endpoints
export const adaptiveApi = {
  getAdaptiveState: async (examCode: string): Promise<AdaptiveState> => {
    const response = await api.get(`/adaptive/state/${examCode}`);
    return response.data.data;
  },

  getNextQuestion: async (examCode: string): Promise<Question> => {
    const response = await api.post(`/adaptive/next-question`, { examCode });
    return response.data.data;
  },

  updateDifficulty: async (examCode: string, isCorrect: boolean): Promise<AdaptiveState> => {
    const response = await api.post(`/adaptive/update-difficulty`, {
      examCode,
      isCorrect,
    });
    return response.data.data;
  },
};

// Session endpoints
export const sessionApi = {
  startSession: async (examCode: string): Promise<{ sessionId: string }> => {
    const response = await api.post('/sessions/start', { examCode });
    return response.data.data;
  },

  endSession: async (sessionId: string): Promise<{ accuracy: number; duration: number }> => {
    const response = await api.post(`/sessions/${sessionId}/end`);
    return response.data.data;
  },

  getSession: async (sessionId: string): Promise<any> => {
    const response = await api.get(`/sessions/${sessionId}`);
    return response.data.data;
  },
};

// Progress endpoints
export const progressApi = {
  getProgress: async (examCode: string): Promise<ProgressSummary> => {
    const response = await api.get(`/progress/${examCode}`);
    return response.data.data;
  },

  getReadiness: async (examCode: string): Promise<ReadinessAssessment> => {
    const response = await api.get(`/readiness/${examCode}`);
    return response.data.data;
  },

  getAllProgress: async (): Promise<ProgressSummary[]> => {
    const response = await api.get('/progress/all');
    return response.data.data;
  },
};

// Study plan endpoints
export const studyPlanApi = {
  getStudyPlan: async (examCode: string): Promise<StudyPlan> => {
    const response = await api.get(`/study-plan/${examCode}`);
    return response.data.data;
  },

  generateStudyPlan: async (
    examCode: string,
    weeks: number,
    hoursPerDay: number
  ): Promise<StudyPlan> => {
    const response = await api.post('/study-plan/generate', {
      examCode,
      weeks,
      hoursPerDay,
    });
    return response.data.data;
  },

  updateStudyPlan: async (planId: string, data: Partial<StudyPlan>): Promise<StudyPlan> => {
    const response = await api.patch(`/study-plan/${planId}`, data);
    return response.data.data;
  },
};

// Video lessons endpoints
export const videoApi = {
  getVideoLessons: async (examCode: string): Promise<VideoLesson[]> => {
    const response = await api.get(`/videos`, { params: { examCode } });
    return response.data.data;
  },

  getVideoLesson: async (lessonId: string): Promise<VideoLesson> => {
    const response = await api.get(`/videos/${lessonId}`);
    return response.data.data;
  },

  markVideoAsWatched: async (lessonId: string): Promise<VideoLesson> => {
    const response = await api.post(`/videos/${lessonId}/watched`);
    return response.data.data;
  },

  updateVideoProgress: async (lessonId: string, progress: number): Promise<VideoLesson> => {
    const response = await api.patch(`/videos/${lessonId}`, { progress });
    return response.data.data;
  },
};

export default api;
