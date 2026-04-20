'use client';

import { useEffect } from 'react';
import { useExamSessionStore } from '@/lib/store';
import { Question } from '@/types';

export function useExamSession() {
  const {
    sessionId,
    examCode,
    currentQuestion,
    currentQuestionIndex,
    totalQuestions,
    answeredQuestions,
    timeElapsed,
    adaptiveState,
    isLoading,
    showResult,
    lastAnswer,
    startSession,
    setCurrentQuestion,
    submitAnswer,
    nextQuestion,
    setAdaptiveState,
    setTimeElapsed,
    setIsLoading,
    endSession,
    reset,
  } = useExamSessionStore();

  // Timer effect
  useEffect(() => {
    if (!sessionId) return;

    const interval = setInterval(() => {
      setTimeElapsed(timeElapsed + 1);
    }, 1000);

    return () => clearInterval(interval);
  }, [sessionId, timeElapsed, setTimeElapsed]);

  const formatTime = (seconds: number): string => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    if (hours > 0) {
      return `${hours}h ${minutes}m ${secs}s`;
    }
    return `${minutes}m ${secs}s`;
  };

  const getProgress = (): number => {
    if (totalQuestions === 0) return 0;
    return (answeredQuestions.length / totalQuestions) * 100;
  };

  const getAccuracy = (): number => {
    if (answeredQuestions.length === 0) return 0;
    // This would need to be tracked by the server
    return 0;
  };

  const startNewSession = (exam: string, total: number) => {
    const newSessionId = `session_${Date.now()}`;
    startSession(exam, newSessionId);
  };

  const selectAndSubmitAnswer = (questionId: string, selectedChoiceId: string, isCorrect: boolean) => {
    submitAnswer(questionId, isCorrect);
  };

  const moveToNextQuestion = () => {
    if (currentQuestionIndex < totalQuestions) {
      nextQuestion();
    }
  };

  const endCurrentSession = () => {
    endSession();
    reset();
  };

  return {
    // State
    sessionId,
    examCode,
    currentQuestion,
    currentQuestionIndex,
    totalQuestions,
    answeredQuestions,
    timeElapsed,
    adaptiveState,
    isLoading,
    showResult,
    lastAnswer,

    // Computed
    progress: getProgress(),
    accuracy: getAccuracy(),
    formattedTime: formatTime(timeElapsed),

    // Actions
    startNewSession,
    setCurrentQuestion,
    selectAndSubmitAnswer,
    moveToNextQuestion,
    setAdaptiveState,
    setIsLoading,
    endCurrentSession,
    reset,
  };
}
