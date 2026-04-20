'use client';

import { useState, useEffect } from 'react';
import Link from 'next/link';
import { Clock, TrendingUp, Target, Flame, Book } from 'lucide-react';
import ReadinessGauge from '@/components/ReadinessGauge';
import ExamCard from '@/components/ExamCard';

const EXAMS = [
  {
    code: 'P',
    name: 'Probability (P)',
    readiness: 72,
    lastPractice: '2024-04-14',
  },
  {
    code: 'FM',
    name: 'Financial Mathematics (FM)',
    readiness: 85,
    lastPractice: '2024-04-12',
  },
  {
    code: 'FAM',
    name: 'Financial Analysis & Modeling (FAM)',
    readiness: 45,
    lastPractice: '2024-04-10',
  },
  {
    code: 'ALTAM',
    name: 'Advanced Long-Term Actuarial Math',
    readiness: 62,
    lastPractice: '2024-04-08',
  },
  {
    code: 'ASTAM',
    name: 'Advanced Short-Term Actuarial Math',
    readiness: 58,
    lastPractice: '2024-04-06',
  },
  {
    code: 'SRM',
    name: 'Statistics for Risk Modeling (SRM)',
    readiness: 68,
    lastPractice: '2024-04-11',
  },
  {
    code: 'PA',
    name: 'Predictive Analytics (PA)',
    readiness: 75,
    lastPractice: '2024-04-13',
  },
];

const WEAK_TOPICS = [
  { name: 'Complex Derivatives', accuracy: 42, examCode: 'FAM' },
  { name: 'Interest Rate Models', accuracy: 48, examCode: 'ALTAM' },
  { name: 'Time Series Analysis', accuracy: 51, examCode: 'SRM' },
];

const RECENT_ACTIVITY = [
  { exam: 'FM', type: 'practice', value: '8/10 correct', time: '2 hours ago' },
  { exam: 'P', type: 'practice', value: '12/15 correct', time: '5 hours ago' },
  { exam: 'PA', type: 'video', value: 'Watched 2 lessons', time: '1 day ago' },
  { exam: 'SRM', type: 'practice', value: '6/10 correct', time: '2 days ago' },
];

export default function DashboardPage() {
  const [selectedExam, setSelectedExam] = useState<string | null>(null);

  return (
    <div className="space-y-8">
      {/* Welcome Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Welcome Back, Alex
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          You're on track! Keep practicing to improve your readiness scores.
        </p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Questions Answered</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">487</p>
            </div>
            <div className="w-12 h-12 bg-primary-100 dark:bg-primary-900 rounded-lg flex items-center justify-center">
              <Book className="w-6 h-6 text-primary-700 dark:text-primary-300" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Overall Accuracy</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">72%</p>
            </div>
            <div className="w-12 h-12 bg-success-100 dark:bg-success-900 rounded-lg flex items-center justify-center">
              <TrendingUp className="w-6 h-6 text-success-700 dark:text-success-300" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Study Streak</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">12 Days</p>
            </div>
            <div className="w-12 h-12 bg-accent-100 dark:bg-accent-900 rounded-lg flex items-center justify-center">
              <Flame className="w-6 h-6 text-accent-600 dark:text-accent-400" />
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Avg. Time/Question</p>
              <p className="text-2xl font-bold text-gray-900 dark:text-white">3m 24s</p>
            </div>
            <div className="w-12 h-12 bg-blue-100 dark:bg-blue-900 rounded-lg flex items-center justify-center">
              <Clock className="w-6 h-6 text-blue-700 dark:text-blue-300" />
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Exam Readiness Scores */}
        <div className="lg:col-span-2 space-y-6">
          <div>
            <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
              Exam Readiness Scores
            </h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
              {EXAMS.map((exam) => (
                <ExamCard
                  key={exam.code}
                  exam={exam}
                  onSelect={() => setSelectedExam(exam.code)}
                />
              ))}
            </div>
          </div>

          {/* Weak Topics */}
          <div className="card">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                Areas to Improve
              </h3>
              <Target className="w-5 h-5 text-error-500" />
            </div>
            <div className="space-y-3">
              {WEAK_TOPICS.map((topic, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
                  <div>
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      {topic.name}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      {topic.examCode}
                    </p>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-12 h-2 bg-gray-200 dark:bg-gray-600 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-error-500"
                        style={{ width: `${topic.accuracy}%` }}
                      />
                    </div>
                    <span className="text-sm font-semibold text-gray-900 dark:text-white w-10 text-right">
                      {topic.accuracy}%
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Sidebar */}
        <div className="space-y-6">
          {/* Quick Stats */}
          <div className="card">
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
              Quick Stats
            </h3>
            <div className="space-y-4">
              <ReadinessGauge score={72} />
              <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-2">
                  Overall Progress
                </p>
                <div className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-primary-600 to-accent-500" style={{ width: '72%' }} />
                </div>
              </div>
            </div>
          </div>

          {/* Recent Activity */}
          <div className="card">
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
              Recent Activity
            </h3>
            <div className="space-y-3">
              {RECENT_ACTIVITY.map((activity, index) => (
                <div key={index} className="flex items-start space-x-3 pb-3 border-b border-gray-200 dark:border-gray-700 last:border-b-0 last:pb-0">
                  <div className="w-2 h-2 bg-primary-500 rounded-full mt-2 flex-shrink-0" />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 dark:text-white">
                      {activity.exam}
                    </p>
                    <p className="text-xs text-gray-600 dark:text-gray-400">
                      {activity.value}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
                      {activity.time}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* CTA */}
          <Link href="/study-plan" className="btn btn-primary w-full justify-center">
            View Study Plan
          </Link>
        </div>
      </div>
    </div>
  );
}
