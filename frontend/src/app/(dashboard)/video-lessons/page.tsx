'use client';

import { useState } from 'react';
import { Play, Clock, CheckCircle2, Search, Filter } from 'lucide-react';
import Image from 'next/image';

const VIDEOS = [
  {
    id: 'v1',
    title: 'Introduction to Probability',
    description: 'Learn the fundamentals of probability theory and sample spaces.',
    exam: 'P',
    topic: 'Probability Basics',
    duration: 45,
    progress: 100,
    thumbnail: '/videos/probability-101.jpg',
  },
  {
    id: 'v2',
    title: 'Combinatorics and Permutations',
    description: 'Master counting principles and combinatorial analysis.',
    exam: 'P',
    topic: 'Combinatorics',
    duration: 52,
    progress: 100,
    thumbnail: '/videos/combinatorics.jpg',
  },
  {
    id: 'v3',
    title: 'Time Value of Money Fundamentals',
    description: 'Understanding interest rates, annuities, and present values.',
    exam: 'FM',
    topic: 'Financial Math',
    duration: 60,
    progress: 75,
    thumbnail: '/videos/time-value.jpg',
  },
  {
    id: 'v4',
    title: 'Bonds and Fixed Income Securities',
    description: 'Comprehensive guide to bond pricing and yield analysis.',
    exam: 'FM',
    topic: 'Bonds',
    duration: 58,
    progress: 45,
    thumbnail: '/videos/bonds.jpg',
  },
  {
    id: 'v5',
    title: 'Introduction to Derivatives',
    description: 'Options, futures, and swaps - essential derivatives concepts.',
    exam: 'FM',
    topic: 'Derivatives',
    duration: 71,
    progress: 0,
    thumbnail: '/videos/derivatives.jpg',
  },
  {
    id: 'v6',
    title: 'Risk Management Framework',
    description: 'Value at Risk, stress testing, and portfolio risk analysis.',
    exam: 'SRM',
    topic: 'Risk Analysis',
    duration: 55,
    progress: 0,
    thumbnail: '/videos/risk-mgmt.jpg',
  },
  {
    id: 'v7',
    title: 'Machine Learning Basics',
    description: 'Introduction to supervised and unsupervised learning.',
    exam: 'PA',
    topic: 'Machine Learning',
    duration: 64,
    progress: 0,
    thumbnail: '/videos/ml-basics.jpg',
  },
  {
    id: 'v8',
    title: 'Regression Analysis',
    description: 'Linear and logistic regression for predictive modeling.',
    exam: 'PA',
    topic: 'Machine Learning',
    duration: 49,
    progress: 0,
    thumbnail: '/videos/regression.jpg',
  },
];

const EXAMS = ['All', 'P', 'FM', 'FAM', 'ALTAM', 'ASTAM', 'SRM', 'PA'];

export default function VideoLessonsPage() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedExam, setSelectedExam] = useState('All');
  const [filterStatus, setFilterStatus] = useState('all'); // all, completed, in-progress, not-started

  const filteredVideos = VIDEOS.filter((video) => {
    const matchesSearch =
      video.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      video.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
      video.topic.toLowerCase().includes(searchQuery.toLowerCase());

    const matchesExam = selectedExam === 'All' || video.exam === selectedExam;

    let matchesStatus = true;
    if (filterStatus === 'completed') {
      matchesStatus = video.progress === 100;
    } else if (filterStatus === 'in-progress') {
      matchesStatus = video.progress > 0 && video.progress < 100;
    } else if (filterStatus === 'not-started') {
      matchesStatus = video.progress === 0;
    }

    return matchesSearch && matchesExam && matchesStatus;
  });

  const getProgressColor = (progress: number) => {
    if (progress === 0) return 'text-gray-400';
    if (progress < 50) return 'text-error-500';
    if (progress < 100) return 'text-accent-500';
    return 'text-success-500';
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Video Lessons
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Comprehensive video explanations for every topic
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="card">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Total Lessons</p>
          <p className="text-2xl font-bold text-gray-900 dark:text-white">{VIDEOS.length}</p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Completed</p>
          <p className="text-2xl font-bold text-success-600 dark:text-success-400">
            {VIDEOS.filter((v) => v.progress === 100).length}
          </p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">In Progress</p>
          <p className="text-2xl font-bold text-accent-600 dark:text-accent-400">
            {VIDEOS.filter((v) => v.progress > 0 && v.progress < 100).length}
          </p>
        </div>
        <div className="card">
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Total Hours</p>
          <p className="text-2xl font-bold text-primary-600 dark:text-primary-400">
            {Math.round(VIDEOS.reduce((sum, v) => sum + v.duration, 0) / 60)}
          </p>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="card space-y-4">
        <div className="relative">
          <Search className="absolute left-3 top-3 w-5 h-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search lessons by title, topic, or keyword..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="input-field pl-10 w-full"
          />
        </div>

        <div className="flex flex-wrap gap-2">
          <div className="flex flex-wrap gap-2">
            {EXAMS.map((exam) => (
              <button
                key={exam}
                onClick={() => setSelectedExam(exam)}
                className={`px-4 py-2 rounded-lg font-medium transition-all ${
                  selectedExam === exam
                    ? 'bg-primary-700 text-white'
                    : 'bg-gray-100 text-gray-900 dark:bg-gray-700 dark:text-white hover:bg-gray-200 dark:hover:bg-gray-600'
                }`}
              >
                {exam}
              </button>
            ))}
          </div>
        </div>

        <div className="flex flex-wrap gap-2 border-t border-gray-200 dark:border-gray-700 pt-4">
          {[
            { value: 'all', label: 'All Status' },
            { value: 'completed', label: 'Completed' },
            { value: 'in-progress', label: 'In Progress' },
            { value: 'not-started', label: 'Not Started' },
          ].map((status) => (
            <button
              key={status.value}
              onClick={() => setFilterStatus(status.value)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all flex items-center ${
                filterStatus === status.value
                  ? 'bg-accent-600 text-white'
                  : 'bg-gray-100 text-gray-900 dark:bg-gray-700 dark:text-white hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              <Filter className="w-4 h-4 mr-2" />
              {status.label}
            </button>
          ))}
        </div>
      </div>

      {/* Videos Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredVideos.map((video) => (
          <div key={video.id} className="card-hover flex flex-col overflow-hidden">
            {/* Thumbnail */}
            <div className="relative w-full h-40 bg-gray-200 dark:bg-gray-700 flex items-center justify-center overflow-hidden mb-4">
              {/* Placeholder for video thumbnail */}
              <div className="w-full h-full bg-gradient-to-br from-primary-600 to-accent-500 flex items-center justify-center">
                <Play className="w-12 h-12 text-white opacity-80" />
              </div>

              {/* Duration Badge */}
              <div className="absolute bottom-2 right-2 bg-black/75 text-white px-2 py-1 rounded text-xs font-bold flex items-center">
                <Clock className="w-3 h-3 mr-1" />
                {video.duration}m
              </div>

              {/* Progress Indicator */}
              {video.progress > 0 && (
                <div className="absolute inset-x-0 bottom-0 h-1 bg-gray-300 dark:bg-gray-600">
                  <div
                    className="h-full bg-success-500 transition-all"
                    style={{ width: `${video.progress}%` }}
                  />
                </div>
              )}
            </div>

            {/* Content */}
            <div className="flex-1 flex flex-col">
              <h3 className="font-bold text-gray-900 dark:text-white mb-1 line-clamp-2">
                {video.title}
              </h3>

              <p className="text-sm text-gray-600 dark:text-gray-400 mb-3 line-clamp-2 flex-1">
                {video.description}
              </p>

              <div className="flex items-center justify-between mb-4 text-xs">
                <div className="flex gap-2">
                  <span className="badge badge-primary">{video.exam}</span>
                  <span className="badge badge-secondary">{video.topic}</span>
                </div>
              </div>

              {/* Progress Bar */}
              {video.progress > 0 && (
                <div className="mb-3">
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-xs font-medium text-gray-600 dark:text-gray-400">
                      Progress
                    </span>
                    <span className={`text-xs font-bold ${getProgressColor(video.progress)}`}>
                      {video.progress}%
                    </span>
                  </div>
                  <div className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gradient-to-r from-primary-600 to-accent-500 transition-all"
                      style={{ width: `${video.progress}%` }}
                    />
                  </div>
                </div>
              )}

              {/* Status and Button */}
              <div className="flex items-center justify-between pt-3 border-t border-gray-200 dark:border-gray-700">
                <div className="flex items-center">
                  {video.progress === 100 ? (
                    <CheckCircle2 className="w-4 h-4 text-success-500 mr-1" />
                  ) : video.progress > 0 ? (
                    <div className="w-4 h-4 rounded-full border-2 border-accent-500 mr-1" />
                  ) : null}
                  <span className="text-xs text-gray-600 dark:text-gray-400">
                    {video.progress === 100
                      ? 'Completed'
                      : video.progress > 0
                      ? `${video.progress}% done`
                      : 'Not started'}
                  </span>
                </div>
                <button className="btn btn-primary btn-sm">
                  {video.progress === 100 ? 'Review' : 'Play'}
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Empty State */}
      {filteredVideos.length === 0 && (
        <div className="card text-center py-12">
          <Search className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">
            No lessons found
          </h3>
          <p className="text-gray-600 dark:text-gray-400">
            Try adjusting your search or filters
          </p>
        </div>
      )}
    </div>
  );
}
