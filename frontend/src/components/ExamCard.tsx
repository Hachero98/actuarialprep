'use client';

import Link from 'next/link';
import { ArrowRight } from 'lucide-react';

interface ExamCardProps {
  exam: {
    code: string;
    name: string;
    readiness: number;
    lastPractice: string;
  };
  onSelect?: (examCode: string) => void;
}

const getReadinessColor = (score: number) => {
  if (score < 30) return 'text-error-600 dark:text-error-400';
  if (score < 50) return 'text-accent-600 dark:text-accent-400';
  if (score < 70) return 'text-blue-600 dark:text-blue-400';
  return 'text-success-600 dark:text-success-400';
};

const getReadinessBgColor = (score: number) => {
  if (score < 30) return 'bg-error-50 dark:bg-error-900';
  if (score < 50) return 'bg-accent-50 dark:bg-accent-900';
  if (score < 70) return 'bg-blue-50 dark:bg-blue-900';
  return 'bg-success-50 dark:bg-success-900';
};

const getLastPracticeDays = (dateString: string): number => {
  const lastDate = new Date(dateString);
  const today = new Date();
  const diffTime = Math.abs(today.getTime() - lastDate.getTime());
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays;
};

export default function ExamCard({ exam, onSelect }: ExamCardProps) {
  const daysSincePractice = getLastPracticeDays(exam.lastPractice);

  return (
    <div className="card-hover flex flex-col">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <p className="text-sm font-mono text-primary-700 dark:text-primary-300 font-bold mb-1">
            Exam {exam.code}
          </p>
          <h3 className="font-bold text-gray-900 dark:text-white text-sm">
            {exam.name}
          </h3>
        </div>
      </div>

      {/* Readiness Score */}
      <div className={`p-3 rounded-lg mb-4 ${getReadinessBgColor(exam.readiness)}`}>
        <p className={`text-xs font-medium mb-1 ${getReadinessColor(exam.readiness)}`}>
          Readiness Score
        </p>
        <div className="flex items-end space-x-2">
          <p className={`text-2xl font-bold ${getReadinessColor(exam.readiness)}`}>
            {exam.readiness}%
          </p>
          <div className="flex-1 h-2 bg-gray-300 dark:bg-gray-600 rounded-full overflow-hidden">
            <div
              className={`h-full transition-all ${
                exam.readiness < 30
                  ? 'bg-error-500'
                  : exam.readiness < 50
                  ? 'bg-accent-500'
                  : exam.readiness < 70
                  ? 'bg-blue-500'
                  : 'bg-success-500'
              }`}
              style={{ width: `${exam.readiness}%` }}
            />
          </div>
        </div>
      </div>

      {/* Last Practice */}
      <p className="text-xs text-gray-600 dark:text-gray-400 mb-4">
        Last practiced: <span className="font-medium">{daysSincePractice}d ago</span>
      </p>

      {/* Progress Status */}
      <div className="mb-4">
        <div className="flex items-center space-x-2">
          <div className="flex-1 h-1 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-primary-600 to-accent-500"
              style={{ width: `${exam.readiness}%` }}
            />
          </div>
        </div>
      </div>

      {/* CTA */}
      <Link
        href={`/practice/${exam.code}`}
        onClick={() => onSelect?.(exam.code)}
        className="btn btn-primary btn-sm w-full justify-center mt-auto"
      >
        Start Practice
        <ArrowRight className="w-4 h-4 ml-2" />
      </Link>
    </div>
  );
}
