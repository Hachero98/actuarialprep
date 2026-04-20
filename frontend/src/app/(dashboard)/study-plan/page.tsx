'use client';

import { Calendar, CheckCircle2, Circle, Zap } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const DAILY_PLANS = [
  {
    date: '2024-04-14',
    dayOfWeek: 'Monday',
    topics: ['Probability Basics', 'Combinatorics'],
    questionsTarget: 15,
    videoLessons: 2,
    completed: false,
  },
  {
    date: '2024-04-15',
    dayOfWeek: 'Tuesday',
    topics: ['Time Value of Money'],
    questionsTarget: 12,
    videoLessons: 1,
    completed: false,
  },
  {
    date: '2024-04-16',
    dayOfWeek: 'Wednesday',
    topics: ['Annuities', 'Interest Rates'],
    questionsTarget: 18,
    videoLessons: 3,
    completed: false,
  },
  {
    date: '2024-04-17',
    dayOfWeek: 'Thursday',
    topics: ['Review'],
    questionsTarget: 20,
    videoLessons: 0,
    completed: false,
  },
  {
    date: '2024-04-18',
    dayOfWeek: 'Friday',
    topics: ['Derivatives', 'Bonds'],
    questionsTarget: 15,
    videoLessons: 2,
    completed: false,
  },
  {
    date: '2024-04-19',
    dayOfWeek: 'Saturday',
    topics: ['Full Practice Exam'],
    questionsTarget: 60,
    videoLessons: 0,
    completed: false,
  },
  {
    date: '2024-04-20',
    dayOfWeek: 'Sunday',
    topics: ['Rest & Review'],
    questionsTarget: 5,
    videoLessons: 1,
    completed: false,
  },
];

const TOPIC_ALLOCATION = [
  { topic: 'Probability', weeks: 3, progress: 60 },
  { topic: 'Financial Math', weeks: 4, progress: 40 },
  { topic: 'Derivatives & Bonds', weeks: 3, progress: 25 },
  { topic: 'Practice Exams', weeks: 2, progress: 10 },
];

const WEEK_PROGRESS = [
  { week: 'Week 1', target: 100, completed: 95, percentage: 95 },
  { week: 'Week 2', target: 100, completed: 88, percentage: 88 },
  { week: 'Week 3', target: 100, completed: 72, percentage: 72 },
  { week: 'Week 4', target: 100, completed: 45, percentage: 45 },
];

export default function StudyPlanPage() {
  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Study Plan - Exam P
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Personalized 4-week preparation schedule
        </p>
      </div>

      {/* Plan Info */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Start Date</p>
          <p className="text-lg font-bold text-gray-900 dark:text-white">Mar 25, 2024</p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Target Date</p>
          <p className="text-lg font-bold text-gray-900 dark:text-white">Apr 22, 2024</p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Total Questions</p>
          <p className="text-lg font-bold text-gray-900 dark:text-white">280+</p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Study Hours</p>
          <p className="text-lg font-bold text-gray-900 dark:text-white">84 hours</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Content */}
        <div className="lg:col-span-2 space-y-6">
          {/* Weekly Progress */}
          <div className="card">
            <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-6">
              Weekly Progress
            </h2>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={WEEK_PROGRESS}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="week" stroke="#6b7280" />
                <YAxis stroke="#6b7280" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#fff',
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px',
                  }}
                />
                <Bar dataKey="completed" fill="#1a365d" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Daily Schedule */}
          <div className="space-y-3">
            <h2 className="text-lg font-bold text-gray-900 dark:text-white flex items-center">
              <Calendar className="w-5 h-5 mr-2" />
              This Week's Schedule
            </h2>
            {DAILY_PLANS.map((plan, index) => (
              <div
                key={index}
                className={`card ${plan.completed ? 'bg-gray-50 dark:bg-gray-700' : ''}`}
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      {plan.completed ? (
                        <CheckCircle2 className="w-6 h-6 text-success-500 flex-shrink-0" />
                      ) : (
                        <Circle className="w-6 h-6 text-gray-400 flex-shrink-0" />
                      )}
                      <div>
                        <h3 className="font-bold text-gray-900 dark:text-white">
                          {plan.dayOfWeek}
                        </h3>
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                          {plan.date}
                        </p>
                      </div>
                    </div>

                    <div className="ml-9 space-y-2">
                      <div>
                        <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
                          Topics:
                        </p>
                        <div className="flex flex-wrap gap-2 mt-1">
                          {plan.topics.map((topic, idx) => (
                            <span
                              key={idx}
                              className="badge badge-primary text-xs"
                            >
                              {topic}
                            </span>
                          ))}
                        </div>
                      </div>

                      <div className="flex flex-wrap gap-6 text-sm">
                        <div>
                          <span className="text-gray-600 dark:text-gray-400">Questions: </span>
                          <span className="font-bold text-gray-900 dark:text-white">
                            {plan.questionsTarget}
                          </span>
                        </div>
                        {plan.videoLessons > 0 && (
                          <div>
                            <span className="text-gray-600 dark:text-gray-400">Videos: </span>
                            <span className="font-bold text-gray-900 dark:text-white">
                              {plan.videoLessons}
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>

                  <button className="btn btn-primary btn-sm flex-shrink-0">
                    Start
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Sidebar */}
        <div className="space-y-6">
          {/* Topic Allocation */}
          <div className="card">
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
              Topic Allocation
            </h3>
            <div className="space-y-4">
              {TOPIC_ALLOCATION.map((item, index) => (
                <div key={index}>
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      {item.topic}
                    </span>
                    <span className="text-xs font-bold text-gray-900 dark:text-white">
                      {item.progress}%
                    </span>
                  </div>
                  <div className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-primary-600 to-accent-500"
                      style={{ width: `${item.progress}%` }}
                    />
                  </div>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {item.weeks} weeks
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Recommendations */}
          <div className="card bg-primary-50 dark:bg-primary-900 border border-primary-200 dark:border-primary-700">
            <h3 className="text-lg font-bold text-primary-900 dark:text-primary-100 mb-4 flex items-center">
              <Zap className="w-5 h-5 mr-2" />
              Recommendations
            </h3>
            <ul className="text-sm text-primary-800 dark:text-primary-200 space-y-2">
              <li className="flex items-start">
                <span className="mr-2">→</span>
                <span>You're on track! Continue your consistent efforts.</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">→</span>
                <span>Focus on derivatives - it's your weakest area.</span>
              </li>
              <li className="flex items-start">
                <span className="mr-2">→</span>
                <span>Take a full practice exam this weekend.</span>
              </li>
            </ul>
          </div>

          {/* Quick Actions */}
          <div className="space-y-2">
            <button className="btn btn-primary w-full justify-center">
              Start Today's Plan
            </button>
            <button className="btn btn-secondary w-full justify-center">
              Adjust Schedule
            </button>
            <button className="btn btn-secondary w-full justify-center">
              Download Plan
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
