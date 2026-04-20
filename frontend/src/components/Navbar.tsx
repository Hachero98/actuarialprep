'use client';

import { useState } from 'react';
import Link from 'next/link';
import { Menu, X, ChevronDown, LogOut, Settings, User } from 'lucide-react';
import { useUiStore, useAuthStore } from '@/lib/store';

const EXAMS = ['P', 'FM', 'FAM', 'ALTAM', 'ASTAM', 'SRM', 'PA'];

export default function Navbar() {
  const { sidebarOpen, setSidebarOpen } = useUiStore();
  const { user, logout } = useAuthStore();
  const [showExamDropdown, setShowExamDropdown] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);

  const handleLogout = () => {
    logout();
    window.location.href = '/login';
  };

  return (
    // SOA dark navy header
    <nav className="bg-primary-900 border-b border-primary-800 sticky top-0 z-40">
      <div className="px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">

        {/* Left: Logo and Menu Button */}
        <div className="flex items-center space-x-4">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="lg:hidden p-2 hover:bg-primary-800 rounded-lg transition-colors"
          >
            {sidebarOpen ? (
              <X className="w-6 h-6 text-white" />
            ) : (
              <Menu className="w-6 h-6 text-white" />
            )}
          </button>

          <Link href="/dashboard" className="flex items-center space-x-2 font-bold text-xl">
            {/* SOA blue → yellow gradient logo mark */}
            <div className="w-8 h-8 rounded-lg flex items-center justify-center"
                 style={{ background: 'linear-gradient(135deg, #00538e, #ffd84e)' }}>
              <span className="text-white text-sm font-bold drop-shadow">AP</span>
            </div>
            <span className="hidden sm:inline text-white tracking-tight">
              Actuarial<span className="text-accent-300 font-extrabold">Prep</span>
            </span>
          </Link>
        </div>

        {/* Center: Exam Selector */}
        <div className="hidden md:flex items-center">
          <div className="relative">
            <button
              onClick={() => setShowExamDropdown(!showExamDropdown)}
              className="flex items-center space-x-2 px-4 py-2 hover:bg-primary-800 rounded-lg transition-colors text-gray-200 font-medium"
            >
              <span>Select Exam</span>
              <ChevronDown className={`w-4 h-4 transition-transform ${showExamDropdown ? 'rotate-180' : ''}`} />
            </button>

            {showExamDropdown && (
              <div className="absolute top-full left-0 mt-1 w-48 bg-primary-900 rounded-lg shadow-lg border border-primary-800 py-2 animate-slide-in">
                {EXAMS.map((exam) => (
                  <Link
                    key={exam}
                    href={`/practice/${exam}`}
                    onClick={() => setShowExamDropdown(false)}
                    className="block px-4 py-2 text-sm text-gray-200 hover:bg-primary-800 hover:text-white transition-colors"
                  >
                    Exam {exam}
                  </Link>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Right: User Menu */}
        <div className="flex items-center space-x-4">
          <div className="relative">
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="flex items-center space-x-2 p-2 hover:bg-primary-800 rounded-lg transition-colors"
            >
              {/* Avatar — SOA blue circle */}
              <div className="w-8 h-8 rounded-full flex items-center justify-center text-white font-bold text-sm"
                   style={{ backgroundColor: '#00538e' }}>
                {user?.name?.[0]?.toUpperCase() || 'A'}
              </div>
              <ChevronDown className={`w-4 h-4 text-gray-200 transition-transform hidden sm:block ${showUserMenu ? 'rotate-180' : ''}`} />
            </button>

            {showUserMenu && (
              <div className="absolute top-full right-0 mt-1 w-48 bg-primary-900 rounded-lg shadow-lg border border-primary-800 py-2 animate-slide-in">
                <div className="px-4 py-2 border-b border-primary-800">
                  <p className="text-sm font-bold text-white">
                    {user?.name || 'User'}
                  </p>
                  <p className="text-xs text-gray-400">
                    {user?.email}
                  </p>
                </div>

                <Link
                  href="/dashboard"
                  onClick={() => setShowUserMenu(false)}
                  className="flex items-center space-x-2 px-4 py-2 text-sm text-gray-200 hover:bg-primary-800 hover:text-white transition-colors"
                >
                  <User className="w-4 h-4" />
                  <span>Profile</span>
                </Link>

                <Link
                  href="/settings"
                  onClick={() => setShowUserMenu(false)}
                  className="flex items-center space-x-2 px-4 py-2 text-sm text-gray-200 hover:bg-primary-800 hover:text-white transition-colors"
                >
                  <Settings className="w-4 h-4" />
                  <span>Settings</span>
                </Link>

                <button
                  onClick={() => { setShowUserMenu(false); handleLogout(); }}
                  className="w-full flex items-center space-x-2 px-4 py-2 text-sm text-error-400 hover:bg-primary-800 hover:text-error-300 transition-colors border-t border-primary-800"
                >
                  <LogOut className="w-4 h-4" />
                  <span>Sign Out</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
