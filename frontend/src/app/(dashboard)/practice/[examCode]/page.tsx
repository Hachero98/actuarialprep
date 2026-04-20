'use client';

import { useState, useEffect } from 'react';
import { useParams } from 'next/navigation';
import { ChevronRight, Send, AlertCircle } from 'lucide-react';
import QuestionCard from '@/components/QuestionCard';
import Timer from '@/components/Timer';
import { Question, Choice } from '@/types';

const MOCK_QUESTION: Question = {
  id: 'q1',
  examCode: 'P',
  topicId: 'probability_basics',
  text: 'A probability function p(x) = x/15 for x = 1, 2, 3, 4, 5. Find p(X ≤ 3)',
  difficulty: 'medium',
  choices: [
    {
      id: 'a',
      label: 'A',
      text: '1/5',
    },
    {
      id: 'b',
      label: 'B',
      text: '2/5',
    },
    {
      id: 'c',
      label: 'C',
      text: '3/5',
    },
    {
      id: 'd',
      label: 'D',
      text: '4/5',
    },
    {
      id: 'e',
      label: 'E',
      text: '1',
    },
  ],
  explanation: 'P(X ≤ 3) = p(1) + p(2) + p(3) = 1/15 + 2/15 + 3/15 = 6/15 = 2/5. The answer is B.',
  correctChoiceId: 'b',
};

export default function PracticePage() {
  const params = useParams();
  const examCode = params.examCode as string;
  const [currentQuestion, setCurrentQuestion] = useState<Question>(MOCK_QUESTION);
  const [selectedChoice, setSelectedChoice] = useState<string | null>(null);
  const [submitted, setSubmitted] = useState(false);
  const [isCorrect, setIsCorrect] = useState(false);
  const [questionIndex, setQuestionIndex] = useState(1);
  const [totalQuestions] = useState(20);
  const [timeElapsed, setTimeElapsed] = useState(0);

  const handleSubmit = () => {
    if (!selectedChoice) return;

    const correct = selectedChoice === currentQuestion.correctChoiceId;
    setIsCorrect(correct);
    setSubmitted(true);
  };

  const handleNextQuestion = () => {
    setSelectedChoice(null);
    setSubmitted(false);
    setQuestionIndex(questionIndex + 1);
  };

  const progress = (questionIndex / totalQuestions) * 100;

  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'easy':
        return 'text-success-600 dark:text-success-400';
      case 'medium':
        return 'text-accent-600 dark:text-accent-400';
      case 'hard':
        return 'text-error-600 dark:text-error-400';
      default:
        return 'text-gray-600 dark:text-gray-400';
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Practice Questions - {examCode}
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Question {questionIndex} of {totalQuestions}
          </p>
        </div>
        <div className="flex items-center space-x-4">
          <Timer initialTime={300} onTimeUp={() => alert('Time is up!')} />
        </div>
      </div>

      {/* Progress Bar */}
      <div className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
        <div
          className="h-full bg-gradient-to-r from-primary-600 to-accent-500 transition-all duration-300"
          style={{ width: `${progress}%` }}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Question Card */}
          <QuestionCard
            question={currentQuestion}
            selectedChoice={selectedChoice}
            onSelectChoice={setSelectedChoice}
            disabled={submitted}
          />

          {/* Result Display */}
          {submitted && (
            <div className="animate-slide-in">
              <div
                className={`p-6 rounded-lg border-2 ${
                  isCorrect
                    ? 'bg-success-50 dark:bg-success-900 border-success-300 dark:border-success-700'
                    : 'bg-error-50 dark:bg-error-900 border-error-300 dark:border-error-700'
                }`}
              >
                <div className="flex items-start space-x-3 mb-4">
                  <div
                    className={`w-6 h-6 rounded-full flex items-center justify-center text-white flex-shrink-0 ${
                      isCorrect ? 'bg-success-500' : 'bg-error-500'
                    }`}
                  >
                    {isCorrect ? '✓' : '✗'}
                  </div>
                  <div>
                    <h3
                      className={`font-bold text-lg mb-1 ${
                        isCorrect
                          ? 'text-success-900 dark:text-success-100'
                          : 'text-error-900 dark:text-error-100'
                      }`}
                    >
                      {isCorrect ? 'Correct!' : 'Incorrect'}
                    </h3>
                    <p
                      className={`text-sm ${
                        isCorrect
                          ? 'text-success-800 dark:text-success-200'
                          : 'text-error-800 dark:text-error-200'
                      }`}
                    >
                      {isCorrect
                        ? 'Great job! You have a strong understanding of this topic.'
                        : 'No worries! Review the explanation below to understand this concept better.'}
                    </p>
                  </div>
                </div>

                {!isCorrect && (
                  <div className="mt-4 p-3 bg-white/50 dark:bg-black/20 rounded">
                    <p className="text-sm font-medium text-gray-900 dark:text-white mb-1">
                      Correct Answer: {currentQuestion.choices.find(c => c.id === currentQuestion.correctChoiceId)?.label}
                    </p>
                  </div>
                )}
              </div>

              {/* Explanation */}
              <div className="p-6 bg-blue-50 dark:bg-blue-900 rounded-lg border border-blue-200 dark:border-blue-800">
                <h4 className="font-bold text-gray-900 dark:text-white mb-2 flex items-center">
                  <AlertCircle className="w-5 h-5 mr-2 text-blue-600 dark:text-blue-400" />
                  Explanation
                </h4>
                <p className="text-gray-700 dark:text-gray-300 text-sm leading-relaxed">
                  {currentQuestion.explanation}
                </p>
              </div>

              {/* Next Button */}
              {questionIndex < totalQuestions && (
                <button
                  onClick={handleNextQuestion}
                  className="btn btn-primary w-full justify-center"
                >
                  Next Question
                  <ChevronRight className="w-5 h-5 ml-2" />
                </button>
              )}

              {questionIndex === totalQuestions && (
                <button className="btn btn-success w-full justify-center">
                  Finish Practice Session
                </button>
              )}
            </div>
          )}

          {/* Submit Button */}
          {!submitted && (
            <button
              onClick={handleSubmit}
              disabled={!selectedChoice}
              className="btn btn-primary w-full justify-center disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-5 h-5 mr-2" />
              Submit Answer
            </button>
          )}
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Question Info */}
          <div className="card">
            <h3 className="font-bold text-gray-900 dark:text-white mb-4">Question Info</h3>
            <div className="space-y-3 text-sm">
              <div>
                <p className="text-gray-500 dark:text-gray-400 mb-1">Difficulty</p>
                <p className={`font-semibold capitalize ${getDifficultyColor(currentQuestion.difficulty)}`}>
                  {currentQuestion.difficulty}
                </p>
              </div>
              <div>
                <p className="text-gray-500 dark:text-gray-400 mb-1">Topic</p>
                <p className="font-semibold text-gray-900 dark:text-white">
                  Probability Basics
                </p>
              </div>
              <div>
                <p className="text-gray-500 dark:text-gray-400 mb-1">Time Spent</p>
                <p className="font-semibold text-gray-900 dark:text-white">
                  {Math.floor(timeElapsed / 60)}m {timeElapsed % 60}s
                </p>
              </div>
            </div>
          </div>

          {/* Tips */}
          <div className="card bg-primary-50 dark:bg-primary-900 border border-primary-200 dark:border-primary-700">
            <h3 className="font-bold text-primary-900 dark:text-primary-100 mb-3">
              💡 Pro Tips
            </h3>
            <ul className="text-sm text-primary-800 dark:text-primary-200 space-y-2">
              <li>• Take your time to read each option carefully</li>
              <li>• Eliminate obviously incorrect choices first</li>
              <li>• Double-check your calculations</li>
              <li>• Mark for review if unsure</li>
            </ul>
          </div>

          {/* Stats */}
          <div className="card">
            <h3 className="font-bold text-gray-900 dark:text-white mb-4">Session Stats</h3>
            <div className="space-y-3 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Correct</span>
                <span className="font-semibold text-success-600 dark:text-success-400">12</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600 dark:text-gray-400">Incorrect</span>
                <span className="font-semibold text-error-600 dark:text-error-400">3</span>
              </div>
              <div className="border-t border-gray-200 dark:border-gray-700 pt-3 flex justify-between">
                <span className="text-gray-600 dark:text-gray-400 font-medium">Accuracy</span>
                <span className="font-bold text-primary-700 dark:text-primary-300">80%</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
