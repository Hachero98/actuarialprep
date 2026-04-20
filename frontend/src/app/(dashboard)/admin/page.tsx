'use client';

import { useState } from 'react';
import { Users, FileText, BarChart3, Edit, Trash2, Plus } from 'lucide-react';

const USERS = [
  {
    id: 'u1',
    name: 'John Smith',
    email: 'john@example.com',
    role: 'user',
    exams: ['P', 'FM'],
    joined: '2024-02-15',
    status: 'active',
  },
  {
    id: 'u2',
    name: 'Sarah Johnson',
    email: 'sarah@example.com',
    role: 'user',
    exams: ['FM', 'FAM'],
    joined: '2024-03-01',
    status: 'active',
  },
  {
    id: 'u3',
    name: 'Mike Davis',
    email: 'mike@example.com',
    role: 'admin',
    exams: ['P', 'FM', 'SRM'],
    joined: '2024-01-10',
    status: 'active',
  },
  {
    id: 'u4',
    name: 'Emily Brown',
    email: 'emily@example.com',
    role: 'user',
    exams: ['PA'],
    joined: '2024-03-15',
    status: 'inactive',
  },
];

const STATISTICS = [
  { label: 'Total Users', value: 2500, change: '+12%' },
  { label: 'Active Users', value: 1850, change: '+8%' },
  { label: 'Total Questions', value: 50420, change: '+230' },
  { label: 'Avg. Accuracy', value: '72.3%', change: '+2.1%' },
];

export default function AdminPage() {
  const [selectedUser, setSelectedUser] = useState<string | null>(null);
  const [showUserModal, setShowUserModal] = useState(false);
  const [activeTab, setActiveTab] = useState('users');

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Admin Dashboard
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage users, questions, and platform statistics
          </p>
        </div>
        <button className="btn btn-primary flex items-center">
          <Plus className="w-5 h-5 mr-2" />
          Add New User
        </button>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {STATISTICS.map((stat, index) => (
          <div key={index} className="card">
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">{stat.label}</p>
            <div className="flex items-end justify-between">
              <p className="text-2xl font-bold text-gray-900 dark:text-white">
                {stat.value}
              </p>
              <span className="text-xs font-semibold text-success-600 dark:text-success-400">
                {stat.change}
              </span>
            </div>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 dark:border-gray-700 -mb-6">
        <div className="flex space-x-8">
          {[
            { id: 'users', label: 'User Management', icon: Users },
            { id: 'questions', label: 'Questions', icon: FileText },
            { id: 'analytics', label: 'Analytics', icon: BarChart3 },
          ].map((tab) => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`pb-4 px-2 border-b-2 font-medium transition-colors flex items-center space-x-2 ${
                  activeTab === tab.id
                    ? 'border-primary-700 text-primary-700 dark:border-primary-300 dark:text-primary-300'
                    : 'border-transparent text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white'
                }`}
              >
                <Icon className="w-4 h-4" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Content */}
      <div>
        {/* Users Tab */}
        {activeTab === 'users' && (
          <div className="space-y-4">
            <div className="card overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-50 dark:bg-gray-700 border-b border-gray-200 dark:border-gray-600">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-bold text-gray-900 dark:text-white uppercase">
                      User
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-bold text-gray-900 dark:text-white uppercase">
                      Email
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-bold text-gray-900 dark:text-white uppercase">
                      Role
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-bold text-gray-900 dark:text-white uppercase">
                      Exams
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-bold text-gray-900 dark:text-white uppercase">
                      Status
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-bold text-gray-900 dark:text-white uppercase">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                  {USERS.map((user) => (
                    <tr
                      key={user.id}
                      className="hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
                    >
                      <td className="px-6 py-4">
                        <p className="font-medium text-gray-900 dark:text-white">
                          {user.name}
                        </p>
                      </td>
                      <td className="px-6 py-4">
                        <p className="text-sm text-gray-600 dark:text-gray-400">{user.email}</p>
                      </td>
                      <td className="px-6 py-4">
                        <span
                          className={`badge ${
                            user.role === 'admin'
                              ? 'badge-accent'
                              : 'badge-primary'
                          }`}
                        >
                          {user.role}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex gap-1">
                          {user.exams.map((exam) => (
                            <span
                              key={exam}
                              className="px-2 py-1 bg-gray-100 dark:bg-gray-700 text-xs font-medium text-gray-900 dark:text-white rounded"
                            >
                              {exam}
                            </span>
                          ))}
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <span
                          className={`badge ${
                            user.status === 'active'
                              ? 'badge-success'
                              : 'bg-gray-100 dark:bg-gray-700 text-gray-900 dark:text-white'
                          }`}
                        >
                          {user.status}
                        </span>
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex gap-2">
                          <button className="btn btn-secondary btn-sm">
                            <Edit className="w-4 h-4" />
                          </button>
                          <button className="btn bg-error-100 dark:bg-error-900 text-error-700 dark:text-error-300 hover:bg-error-200 dark:hover:bg-error-800 btn-sm">
                            <Trash2 className="w-4 h-4" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Questions Tab */}
        {activeTab === 'questions' && (
          <div className="card">
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <div>
                  <h3 className="text-lg font-bold text-gray-900 dark:text-white">
                    Question Templates
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Manage and review question templates for all exams
                  </p>
                </div>
                <button className="btn btn-primary">Create Template</button>
              </div>

              <div className="space-y-3 mt-6">
                {[
                  {
                    title: 'Probability Distribution Problems',
                    exam: 'P',
                    count: 145,
                  },
                  {
                    title: 'Time Value of Money Calculations',
                    exam: 'FM',
                    count: 203,
                  },
                  {
                    title: 'Financial Derivative Analysis',
                    exam: 'FM',
                    count: 98,
                  },
                  {
                    title: 'Risk Modeling Scenarios',
                    exam: 'SRM',
                    count: 167,
                  },
                ].map((template, index) => (
                  <div
                    key={index}
                    className="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg flex items-center justify-between"
                  >
                    <div>
                      <h4 className="font-bold text-gray-900 dark:text-white">
                        {template.title}
                      </h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {template.exam} • {template.count} questions
                      </p>
                    </div>
                    <button className="btn btn-secondary btn-sm">Edit</button>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Analytics Tab */}
        {activeTab === 'analytics' && (
          <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="card">
                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
                  Platform Health
                </h3>
                <div className="space-y-3">
                  <div>
                    <div className="flex justify-between mb-1">
                      <span className="text-sm font-medium">System Uptime</span>
                      <span className="text-sm font-bold text-success-600">99.98%</span>
                    </div>
                    <div className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                      <div className="h-full w-full bg-success-500" />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-1">
                      <span className="text-sm font-medium">DB Performance</span>
                      <span className="text-sm font-bold text-accent-600">Excellent</span>
                    </div>
                    <div className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                      <div className="h-full w-9/12 bg-accent-500" />
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between mb-1">
                      <span className="text-sm font-medium">API Response Time</span>
                      <span className="text-sm font-bold text-primary-600">45ms avg</span>
                    </div>
                    <div className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                      <div className="h-full w-11/12 bg-primary-500" />
                    </div>
                  </div>
                </div>
              </div>

              <div className="card">
                <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
                  Recent Activity
                </h3>
                <div className="space-y-3">
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Last 24 hours statistics:
                  </p>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm">New Users</span>
                      <span className="font-bold">+42</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Questions Answered</span>
                      <span className="font-bold">+3,241</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Avg. Session Length</span>
                      <span className="font-bold">45m 12s</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
