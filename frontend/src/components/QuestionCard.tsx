'use client';

import { Question } from '@/types';
import clsx from 'clsx';

interface QuestionCardProps {
  question: Question;
  selectedChoice: string | null;
  onSelectChoice: (choiceId: string) => void;
  disabled?: boolean;
}

export default function QuestionCard({
  question,
  selectedChoice,
  onSelectChoice,
  disabled = false,
}: QuestionCardProps) {
  const getChoiceBgColor = (choiceId: string, isCorrect: boolean, isSelected: boolean) => {
    if (!disabled) {
      if (isSelected) {
        return 'bg-primary-100 dark:bg-primary-900 border-2 border-primary-500';
      }
      return 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:bg-primary-50 dark:hover:bg-gray-700 hover:border-primary-300';
    }

    // Disabled state (showing results)
    if (isCorrect) {
      return 'bg-success-100 dark:bg-success-900 border-2 border-success-500';
    }
    if (isSelected && !isCorrect) {
      return 'bg-error-100 dark:bg-error-900 border-2 border-error-500';
    }
    return 'bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600';
  };

  const getChoiceTextColor = (choiceId: string, isCorrect: boolean, isSelected: boolean) => {
    if (!disabled) {
      return 'text-gray-900 dark:text-white';
    }

    if (isCorrect) {
      return 'text-success-900 dark:text-success-100 font-bold';
    }
    if (isSelected && !isCorrect) {
      return 'text-error-900 dark:text-error-100 font-bold';
    }
    return 'text-gray-600 dark:text-gray-400';
  };

  return (
    <div className="card space-y-6">
      {/* Question Text */}
      <div>
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
          {question.text}
        </h2>
        <p className="text-sm text-gray-600 dark:text-gray-400">
          Select the correct answer from the options below.
        </p>
      </div>

      {/* Choices */}
      <div className="space-y-3">
        {question.choices.map((choice) => {
          const isSelected = selectedChoice === choice.id;
          const isCorrect = choice.id === question.correctChoiceId;

          return (
            <button
              key={choice.id}
              onClick={() => !disabled && onSelectChoice(choice.id)}
              disabled={disabled}
              className={clsx(
                'w-full p-4 rounded-lg border-2 transition-all text-left',
                getChoiceBgColor(choice.id, isCorrect, isSelected),
                disabled && 'cursor-default',
                !disabled && 'cursor-pointer'
              )}
            >
              <div className="flex items-start space-x-4">
                {/* Choice Label */}
                <div className="flex-shrink-0">
                  <div
                    className={clsx(
                      'w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm transition-all',
                      isSelected
                        ? 'bg-primary-600 dark:bg-primary-500 text-white'
                        : 'bg-gray-200 dark:bg-gray-600 text-gray-900 dark:text-white'
                    )}
                  >
                    {choice.label}
                  </div>
                </div>

                {/* Choice Text */}
                <div className="flex-1">
                  <p className={clsx('font-medium break-words', getChoiceTextColor(choice.id, isCorrect, isSelected))}>
                    {choice.text}
                  </p>
                </div>

                {/* Status Indicator */}
                {disabled && (
                  <div className="flex-shrink-0">
                    {isCorrect && (
                      <div className="w-6 h-6 rounded-full bg-success-500 flex items-center justify-center text-white font-bold">
                        ✓
                      </div>
                    )}
                    {isSelected && !isCorrect && (
                      <div className="w-6 h-6 rounded-full bg-error-500 flex items-center justify-center text-white font-bold">
                        ✗
                      </div>
                    )}
                  </div>
                )}
              </div>
            </button>
          );
        })}
      </div>

      {/* Help Text */}
      <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
        <p className="text-xs text-gray-600 dark:text-gray-400">
          {disabled
            ? 'Review the explanation above to understand this concept better.'
            : 'Click on an answer option to select it.'}
        </p>
      </div>
    </div>
  );
}
