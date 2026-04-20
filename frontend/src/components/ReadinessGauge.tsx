'use client';

interface ReadinessGaugeProps {
  score: number;
  size?: 'sm' | 'md' | 'lg';
}

export default function ReadinessGauge({ score, size = 'md' }: ReadinessGaugeProps) {
  const clampScore = Math.max(0, Math.min(100, score));
  const rotation = (clampScore / 100) * 180 - 90;

  const getScoreColor = (score: number) => {
    if (score < 30) return '#e53e3e'; // error
    if (score < 50) return '#d69e2e'; // accent
    if (score < 70) return '#ecc94b'; // warning
    if (score < 90) return '#38a169'; // success
    return '#22c55e'; // success bright
  };

  const getScoreLabel = (score: number) => {
    if (score < 30) return 'Not Ready';
    if (score < 50) return 'Needs Work';
    if (score < 70) return 'Getting There';
    if (score < 90) return 'Well Prepared';
    return 'Ready to Test';
  };

  const sizeClasses = {
    sm: { container: 'w-32 h-32', text: 'text-lg', inner: 'w-24 h-24' },
    md: { container: 'w-48 h-48', text: 'text-3xl', inner: 'w-40 h-40' },
    lg: { container: 'w-64 h-64', text: 'text-4xl', inner: 'w-56 h-56' },
  };

  const { container, text, inner } = sizeClasses[size];

  return (
    <div className="flex flex-col items-center justify-center space-y-4">
      {/* Gauge SVG */}
      <div className={`relative ${container} mx-auto`}>
        <svg className="w-full h-full" viewBox="0 0 200 200">
          {/* Background Arc */}
          <circle
            cx="100"
            cy="100"
            r="90"
            fill="none"
            stroke="#e5e7eb"
            strokeWidth="12"
            strokeDasharray="283"
            strokeDashoffset="283"
            opacity="0.3"
            transform="rotate(-90 100 100)"
          />

          {/* Score Arc */}
          <circle
            cx="100"
            cy="100"
            r="90"
            fill="none"
            stroke={getScoreColor(clampScore)}
            strokeWidth="12"
            strokeDasharray={`${(clampScore / 100) * 283} 283`}
            opacity="1"
            transform="rotate(-90 100 100)"
            style={{
              transition: 'stroke-dasharray 0.5s ease-in-out',
            }}
          />

          {/* Needle */}
          <line
            x1="100"
            y1="100"
            x2="100"
            y2="20"
            stroke={getScoreColor(clampScore)}
            strokeWidth="4"
            opacity="0.8"
            transform={`rotate(${rotation} 100 100)`}
            style={{
              transition: 'transform 0.5s ease-in-out',
            }}
          />

          {/* Center Circle */}
          <circle cx="100" cy="100" r="8" fill={getScoreColor(clampScore)} />
        </svg>

        {/* Center Content */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <p className={`font-bold ${text}`} style={{ color: getScoreColor(clampScore) }}>
            {clampScore}
          </p>
          <p className="text-xs text-gray-600 dark:text-gray-400">Readiness</p>
        </div>
      </div>

      {/* Label */}
      <div className="text-center">
        <p className="font-bold text-gray-900 dark:text-white">
          {getScoreLabel(clampScore)}
        </p>
        <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
          {clampScore >= 80
            ? 'You are well-prepared for the exam.'
            : clampScore >= 70
            ? 'You are mostly prepared. Focus on weak areas.'
            : clampScore >= 50
            ? 'Continue practicing to improve your readiness.'
            : 'Dedicate more time to studying.'}
        </p>
      </div>
    </div>
  );
}
