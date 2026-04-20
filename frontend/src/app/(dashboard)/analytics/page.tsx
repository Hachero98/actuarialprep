'use client';

import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, AlertTriangle, Award } from 'lucide-react';
import ReadinessGauge from '@/components/ReadinessGauge';

const ACCURACY_DATA = [
  { date: 'Apr 1', P: 65, FM: 72, FAM: 55, ALTAM: 60, SRM: 70, PA: 68 },
  { date: 'Apr 3', P: 68, FM: 74, FAM: 58, ALTAM: 62, SRM: 72, PA: 70 },
  { date: 'Apr 5', P: 70, FM: 76, FAM: 60, ALTAM: 64, SRM: 75, PA: 72 },
  { date: 'Apr 7', P: 72, FM: 78, FAM: 63, ALTAM: 66, SRM: 77, PA: 74 },
  { date: 'Apr 9', P: 75, FM: 80, FAM: 65, ALTAM: 68, SRM: 80, PA: 76 },
  { date: 'Apr 11', P: 76, FM: 82, FAM: 68, ALTAM: 70, SRM: 82, PA: 78 },
  { date: 'Apr 13', P: 78, FM: 85, FAM: 70, ALTAM: 72, SRM: 85, PA: 80 },
];

const TOPIC_DATA = [
  { topic: 'Probability Basics', mastery: 78, questions: 45 },
  { topic: 'Combinatorics', mastery: 82, questions: 32 },
  { topic: 'Time Value', mastery: 85, questions: 48 },
  { topic: 'Annuities', mastery: 72, questions: 28 },
  { topic: 'Bonds & Derivatives', mastery: 65, questions: 35 },
  { topic: 'Interest Rates', mastery: 58, questions: 22 },
];

const TIME_DISTRIBUTION = [
  { name: 'Practice Questions', value: 45, color: '#1a365d' },
  { name: 'Video Lessons', value: 20, color: '#d69e2e' },
  { name: 'Review', value: 25, color: '#38a169' },
  { name: 'Other', value: 10, color: '#cbd5e1' },
];

const WEAKNESS_ALERTS = [
  { topic: 'Complex Derivatives', examCode: 'FAM', accuracy: 42, recommendation: 'Review recommended' },
  { topic: 'Stochastic Modeling', examCode: 'ALTAM', accuracy: 48, recommendation: 'Focus area identified' },
  { topic: 'Time Series', examCode: 'SRM', accuracy: 51, recommendation: 'Practice more questions' },
];

export default function AnalyticsPage() {
  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Analytics & Performance
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Detailed insights into your exam preparation journey
        </p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="card">
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Overall Readiness</p>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">72%</p>
            </div>
            <Award className="w-6 h-6 text-primary-500" />
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            ↑ 5% from last week
          </p>
        </div>

        <div className="card">
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Total Questions Answered</p>
              <p className="text-3xl font-bold text-gray-900 dark:text-white">487</p>
            </div>
            <TrendingUp className="w-6 h-6 text-success-500" />
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            ↑ 42 this week
          </p>
        </div>

        <div className="card">
          <div className="flex items-start justify-between mb-4">
            <div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Weakest Area</p>
              <p className="text-lg font-bold text-gray-900 dark:text-white">FAM</p>
            </div>
            <AlertTriangle className="w-6 h-6 text-error-500" />
          </div>
          <p className="text-xs text-gray-500 dark:text-gray-400">
            Accuracy: 70% (needs work)
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Main Charts */}
        <div className="lg:col-span-2 space-y-6">
          {/* Accuracy Over Time */}
          <div className="card">
            <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-6">
              Accuracy Over Time
            </h2>
            <ResponsiveContainer width="100%" height={350}>
              <LineChart data={ACCURACY_DATA}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="date" stroke="#6b7280" />
                <YAxis stroke="#6b7280" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#fff',
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px',
                  }}
                />
                <Legend />
                <Line type="monotone" dataKey="P" stroke="#1a365d" strokeWidth={2} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="FM" stroke="#d69e2e" strokeWidth={2} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="FAM" stroke="#e53e3e" strokeWidth={2} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="SRM" stroke="#38a169" strokeWidth={2} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="PA" stroke="#5b21b6" strokeWidth={2} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Topic Breakdown */}
          <div className="card">
            <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-6">
              Topic Breakdown - Mastery Levels
            </h2>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={TOPIC_DATA}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                <XAxis dataKey="topic" stroke="#6b7280" angle={-45} textAnchor="end" height={100} />
                <YAxis stroke="#6b7280" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#fff',
                    border: '1px solid #e5e7eb',
                    borderRadius: '8px',
                  }}
                />
                <Bar dataKey="mastery" fill="#1a365d" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Right Sidebar */}
        <div className="space-y-6">
          {/* Readiness Gauge */}
          <div className="card">
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-6 text-center">
              Overall Readiness
            </h3>
            <ReadinessGauge score={72} />
          </div>

          {/* Time Distribution */}
          <div className="card">
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
              Time Distribution
            </h3>
            <div className="space-y-3">
              {TIME_DISTRIBUTION.map((item) => (
                <div key={item.name}>
                  <div className="flex justify-between mb-1">
                    <span className="text-sm text-gray-700 dark:text-gray-300">{item.name}</span>
                    <span className="text-sm font-bold text-gray-900 dark:text-white">
                      {item.value}%
                    </span>
                  </div>
                  <div className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                    <div
                      className="h-full"
                      style={{
                        backgroundColor: item.color,
                        width: `${item.value}%`,
                      }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Recommendations */}
          <div className="card bg-accent-50 dark:bg-accent-900 border border-accent-200 dark:border-accent-800">
            <h3 className="text-lg font-bold text-accent-900 dark:text-accent-100 mb-4 flex items-center">
              <AlertTriangle className="w-5 h-5 mr-2" />
              Focus Areas
            </h3>
            <div className="space-y-3">
              {WEAKNESS_ALERTS.map((alert, index) => (
                <div
                  key={index}
                  className="p-3 bg-white/70 dark:bg-black/30 rounded border border-accent-200 dark:border-accent-700"
                >
                  <p className="text-sm font-bold text-accent-900 dark:text-accent-100">
                    {alert.topic}
                  </p>
                  <p className="text-xs text-accent-800 dark:text-accent-200 mt-1">
                    {alert.examCode} - {alert.accuracy}% accuracy
                  </p>
                  <p className="text-xs font-medium text-accent-700 dark:text-accent-300 mt-2">
                    {alert.recommendation}
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
