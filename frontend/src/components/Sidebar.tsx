'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  BookOpen,
  BarChart3,
  CalendarDays,
  Video,
  Settings,
  X,
} from 'lucide-react';
import { useUiStore, useAuthStore } from '@/lib/store';

const MENU_ITEMS = [
  {
    label: 'Dashboard',
    href: '/dashboard',
    icon: LayoutDashboard,
  },
  {
    label: 'Practice',
    href: '/practice/P',
    icon: BookOpen,
  },
  {
    label: 'Analytics',
    href: '/analytics',
    icon: BarChart3,
  },
  {
    label: 'Study Plan',
    href: '/study-plan',
    icon: CalendarDays,
  },
  {
    label: 'Video Lessons',
    href: '/video-lessons',
    icon: Video,
  },
];

const ADMIN_ITEMS = [
  {
    label: 'Admin',
    href: '/admin',
    icon: Settings,
  },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { sidebarOpen, setSidebarOpen } = useUiStore();
  const { user } = useAuthStore();
  const isAdmin = user?.role === 'admin';

  const menuItems = isAdmin ? [...MENU_ITEMS, ...ADMIN_ITEMS] : MENU_ITEMS;

  const isActive = (href: string) => {
    return pathname === href || pathname.startsWith(href);
  };

  return (
    <>
      {/* Mobile Overlay */}
      {sidebarOpen && (
        <div
          className="lg:hidden fixed inset-0 bg-black/50 z-30"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div
        className={`fixed lg:static inset-y-16 left-0 z-30 w-64 bg-gray-50 dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 p-4 space-y-2 transition-all duration-300 overflow-y-auto ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        {/* Close Button (Mobile) */}
        <button
          onClick={() => setSidebarOpen(false)}
          className="lg:hidden absolute top-4 right-4 p-2 hover:bg-gray-200 dark:hover:bg-gray-700 rounded-lg"
        >
          <X className="w-5 h-5" />
        </button>

        {/* User Card */}
        <div className="mb-6 p-4 bg-white dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600 mt-10 lg:mt-0">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-primary-700 to-accent-500 rounded-full flex items-center justify-center text-white font-bold">
              {user?.name?.[0]?.toUpperCase() || 'A'}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-bold text-gray-900 dark:text-white truncate">
                {user?.name || 'User'}
              </p>
              <p className="text-xs text-gray-600 dark:text-gray-400 truncate">
                {user?.email}
              </p>
            </div>
          </div>
        </div>

        {/* Menu Items */}
        <nav className="space-y-1">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.href);

            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setSidebarOpen(false)}
                className={`flex items-center space-x-3 px-4 py-3 rounded-lg font-medium transition-all ${
                  active
                    ? 'bg-primary-700 text-white shadow-md'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-white dark:hover:bg-gray-700'
                }`}
              >
                <Icon className="w-5 h-5 flex-shrink-0" />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Quick Links */}
        <div className="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700 space-y-2">
          <p className="px-4 text-xs font-bold text-gray-600 dark:text-gray-400 uppercase">
            Resources
          </p>
          <a
            href="#"
            className="flex items-center space-x-3 px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-white dark:hover:bg-gray-700 rounded-lg transition-all text-sm"
          >
            Help & Support
          </a>
          <a
            href="#"
            className="flex items-center space-x-3 px-4 py-2 text-gray-700 dark:text-gray-300 hover:bg-white dark:hover:bg-gray-700 rounded-lg transition-all text-sm"
          >
            Documentation
          </a>
        </div>

        {/* Footer */}
        <div className="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
          <p className="text-xs text-gray-500 dark:text-gray-500 px-4">
            ActuarialPrep v1.0.0
          </p>
        </div>
      </div>
    </>
  );
}
