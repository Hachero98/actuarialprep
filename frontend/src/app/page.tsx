'use client';

import Link from 'next/link';
import { ArrowRight, BarChart3, BookOpen, Zap, TrendingUp, Users } from 'lucide-react';
import { useState } from 'react';

const EXAMS = [
  {
    code: 'P',
    name: 'Probability (P)',
    description: 'Foundational probability and financial math concepts',
    candidates: '2,500+',
  },
  {
    code: 'FM',
    name: 'Financial Mathematics (FM)',
    description: 'Time value of money and financial instruments',
    candidates: '3,200+',
  },
  {
    code: 'FAM',
    name: 'Financial Analysis and Modeling (FAM)',
    description: 'Advanced financial analysis for actuaries',
    candidates: '1,800+',
  },
  {
    code: 'ALTAM',
    name: 'Advanced Long-Term Actuarial Mathematics (ALTAM)',
    description: 'Comprehensive actuarial mathematics and modeling',
    candidates: '1,200+',
  },
  {
    code: 'ASTAM',
    name: 'Advanced Short-Term Actuarial Mathematics (ASTAM)',
    description: 'Short-term insurance mathematics and applications',
    candidates: '900+',
  },
  {
    code: 'SRM',
    name: 'Statistics for Risk Modeling (SRM)',
    description: 'Advanced statistical methods for risk analysis',
    candidates: '2,100+',
  },
  {
    code: 'PA',
    name: 'Predictive Analytics (PA)',
    description: 'Machine learning and predictive modeling techniques',
    candidates: '2,800+',
  },
];

const FEATURES = [
  {
    icon: <Zap className="w-8 h-8" />,
    title: 'Adaptive Practice',
    description: 'AI-powered questions that adapt to your skill level, optimizing your learning path.',
  },
  {
    icon: <BarChart3 className="w-8 h-8" />,
    title: 'Smart Analytics',
    description: 'Detailed insights into your performance, weak topics, and readiness for exams.',
  },
  {
    icon: <BookOpen className="w-8 h-8" />,
    title: 'Personalized Plans',
    description: 'Custom study schedules tailored to your goals and available study time.',
  },
  {
    icon: <TrendingUp className="w-8 h-8" />,
    title: 'Video Lessons',
    description: 'Comprehensive video explanations for every topic and concept.',
  },
  {
    icon: <Users className="w-8 h-8" />,
    title: 'Community',
    description: 'Connect with other actuarial exam candidates and share resources.',
  },
  {
    icon: <Zap className="w-8 h-8" />,
    title: 'Progress Tracking',
    description: 'Real-time tracking of your progress with detailed performance metrics.',
  },
];

export default function HomePage() {
  const [hoveredExam, setHoveredExam] = useState<string | null>(null);

  return (
    <div className="min-h-screen bg-white" style={{ color: '#0d1c27' }}>

      {/* ── Navigation — SOA dark navy ── */}
      <nav className="sticky top-0 z-50 bg-primary-900 border-b border-primary-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 rounded-lg flex items-center justify-center"
                   style={{ background: 'linear-gradient(135deg, #00538e, #ffd84e)' }}>
                <span className="text-white font-bold text-sm drop-shadow">AP</span>
              </div>
              <span className="text-xl font-bold text-white tracking-tight">
                Actuarial<span className="text-accent-300 font-extrabold">Prep</span>
              </span>
            </div>
            <div className="flex items-center space-x-4">
              <Link
                href="/login"
                className="px-4 py-2 text-gray-200 hover:text-white transition-colors"
              >
                Login
              </Link>
              <Link
                href="/register"
                className="px-5 py-2 rounded-lg font-semibold text-white transition-colors"
                style={{ backgroundColor: '#00538e' }}
                onMouseEnter={e => (e.currentTarget.style.backgroundColor = '#196499')}
                onMouseLeave={e => (e.currentTarget.style.backgroundColor = '#00538e')}
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* ── Hero — white with SOA blue glow ── */}
      <section className="relative overflow-hidden pt-20 pb-20 sm:pt-32 sm:pb-32 bg-white">
        <div className="absolute inset-0 -z-10">
          <div className="absolute top-0 left-1/2 -translate-x-1/2 w-[800px] h-[800px] rounded-full blur-3xl"
               style={{ background: 'radial-gradient(circle, rgba(0,83,142,0.08) 0%, transparent 70%)' }} />
        </div>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold mb-6 leading-tight"
              style={{ color: '#0d1c27' }}>
            Master Actuarial Exams with<br />
            <span className="text-gradient">Adaptive Learning</span>
          </h1>
          <p className="text-lg sm:text-xl mb-8 max-w-2xl mx-auto leading-relaxed"
             style={{ color: '#566068' }}>
            Join thousands of candidates preparing for SOA actuarial exams. Our AI-powered
            platform adapts to your learning style and optimizes your path to success.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
            <Link
              href="/register"
              className="inline-flex items-center justify-center px-6 py-3 rounded-lg font-semibold text-lg text-white transition-colors"
              style={{ backgroundColor: '#00538e' }}
              onMouseEnter={e => (e.currentTarget.style.backgroundColor = '#196499')}
              onMouseLeave={e => (e.currentTarget.style.backgroundColor = '#00538e')}
            >
              Start Free Trial <ArrowRight className="w-5 h-5 ml-2" />
            </Link>
            <button
              className="inline-flex items-center justify-center px-6 py-3 rounded-lg font-semibold text-lg border transition-colors"
              style={{ borderColor: '#cfd2d4', color: '#0d1c27', backgroundColor: '#ffffff' }}
              onMouseEnter={e => (e.currentTarget.style.backgroundColor = '#f8f8f9')}
              onMouseLeave={e => (e.currentTarget.style.backgroundColor = '#ffffff')}
            >
              Watch Demo
            </button>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-3 gap-6 mt-16 max-w-2xl mx-auto">
            {[
              { value: '2,500+', label: 'Active Users' },
              { value: '50K+',   label: 'Practice Questions' },
              { value: '94%',    label: 'Pass Rate' },
            ].map(({ value, label }) => (
              <div key={label}>
                <div className="text-3xl font-bold text-gradient mb-2">{value}</div>
                <p className="text-sm" style={{ color: '#566068' }}>{label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Features — SOA light grey background ── */}
      <section className="py-20" style={{ backgroundColor: '#f2f6f9' }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4" style={{ color: '#0d1c27' }}>
              Why Choose ActuarialPrep?
            </h2>
            <p className="text-lg" style={{ color: '#566068' }}>
              Everything you need to pass your actuarial exams
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {FEATURES.map((feature, index) => (
              <div key={index}
                   className="rounded-lg border bg-white p-6 shadow-sm hover:shadow-md cursor-pointer transition-all group"
                   style={{ borderColor: '#cfd2d4' }}>
                <div className="w-12 h-12 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform"
                     style={{ backgroundColor: '#eaf3fa', color: '#00538e' }}>
                  {feature.icon}
                </div>
                <h3 className="text-xl font-bold mb-2" style={{ color: '#0d1c27' }}>
                  {feature.title}
                </h3>
                <p style={{ color: '#566068' }}>{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Exams — white background ── */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl sm:text-4xl font-bold mb-4" style={{ color: '#0d1c27' }}>
              Prepare for All SOA Exams
            </h2>
            <p className="text-lg" style={{ color: '#566068' }}>
              Comprehensive practice for every level and specialty
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {EXAMS.map((exam) => (
              <div
                key={exam.code}
                onMouseEnter={() => setHoveredExam(exam.code)}
                onMouseLeave={() => setHoveredExam(null)}
                className="rounded-lg border bg-white p-6 shadow-sm hover:shadow-md cursor-pointer transition-all hover:scale-105"
                style={{ borderColor: '#cfd2d4' }}
              >
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <div className="text-sm font-mono font-bold mb-1" style={{ color: '#00538e' }}>
                      {exam.code}
                    </div>
                    <h3 className="text-lg font-bold" style={{ color: '#0d1c27' }}>
                      {exam.name}
                    </h3>
                  </div>
                </div>
                <p className="text-sm mb-4" style={{ color: '#566068' }}>
                  {exam.description}
                </p>
                <div className="flex items-center justify-between pt-4"
                     style={{ borderTop: '1px solid #cfd2d4' }}>
                  <span className="text-xs" style={{ color: '#9ea4a9' }}>
                    {exam.candidates} preparing
                  </span>
                  {hoveredExam === exam.code && (
                    <Link
                      href={`/practice/${exam.code}`}
                      className="font-semibold text-sm animate-slide-in"
                      style={{ color: '#00538e' }}
                    >
                      Start Practice →
                    </Link>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA — SOA brand blue ── */}
      <section className="py-20" style={{ backgroundColor: '#00538e' }}>
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          {/* SOA-style yellow accent bar */}
          <div className="w-12 h-1 rounded-full mx-auto mb-6" style={{ backgroundColor: '#ffd84e' }} />
          <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
            Ready to Pass Your Exam?
          </h2>
          <p className="text-lg mb-8" style={{ color: 'rgba(255,255,255,0.85)' }}>
            Join thousands of successful actuarial candidates. Start your free trial today.
          </p>
          <Link
            href="/register"
            className="inline-flex items-center justify-center px-8 py-3 rounded-lg font-bold text-lg transition-colors"
            style={{ backgroundColor: '#ffd84e', color: '#0d1c27' }}
            onMouseEnter={e => (e.currentTarget.style.backgroundColor = '#ffe580')}
            onMouseLeave={e => (e.currentTarget.style.backgroundColor = '#ffd84e')}
          >
            Get Started Now <ArrowRight className="w-5 h-5 ml-2" />
          </Link>
        </div>
      </section>

      {/* ── Footer — SOA dark navy ── */}
      <footer style={{ backgroundColor: '#0d1c27', color: '#9ea4a9' }} className="py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-8">
            {[
              { title: 'Product', links: ['Practice', 'Analytics', 'Study Plans'] },
              { title: 'Company', links: ['About', 'Blog', 'Contact'] },
              { title: 'Resources', links: ['Docs', 'FAQ', 'Support'] },
              { title: 'Legal', links: ['Privacy', 'Terms'] },
            ].map(({ title, links }) => (
              <div key={title}>
                <h4 className="font-bold mb-4 text-white">{title}</h4>
                <ul className="space-y-2 text-sm">
                  {links.map((link) => (
                    <li key={link}>
                      <a href="#"
                         className="transition-colors"
                         style={{ color: '#9ea4a9' }}
                         onMouseEnter={e => (e.currentTarget.style.color = '#ffffff')}
                         onMouseLeave={e => (e.currentTarget.style.color = '#9ea4a9')}>
                        {link}
                      </a>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
          <div className="pt-8 flex flex-col sm:flex-row items-center justify-between"
               style={{ borderTop: '1px solid #1a2c3d' }}>
            <div className="flex items-center space-x-2 mb-4 sm:mb-0">
              <div className="w-6 h-6 rounded"
                   style={{ background: 'linear-gradient(135deg, #00538e, #ffd84e)' }} />
              <span className="font-bold text-white">ActuarialPrep</span>
            </div>
            <p className="text-sm" style={{ color: '#9ea4a9' }}>
              © 2024 ActuarialPrep. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}
