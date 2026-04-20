'use client';

import { useEffect, useState } from 'react';
import { Clock } from 'lucide-react';

interface TimerProps {
  initialTime: number; // in seconds
  onTimeUp?: () => void;
  showWarning?: boolean;
}

export default function Timer({ initialTime, onTimeUp, showWarning = true }: TimerProps) {
  const [timeLeft, setTimeLeft] = useState(initialTime);
  const [isWarning, setIsWarning] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setTimeLeft((prev) => {
        if (prev <= 1) {
          clearInterval(interval);
          onTimeUp?.();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(interval);
  }, [onTimeUp]);

  useEffect(() => {
    if (showWarning && timeLeft < 60) {
      setIsWarning(true);
    } else {
      setIsWarning(false);
    }
  }, [timeLeft, showWarning]);

  const minutes = Math.floor(timeLeft / 60);
  const seconds = timeLeft % 60;

  const formatTime = (value: number) => {
    return value.toString().padStart(2, '0');
  };

  return (
    <div
      className={`flex items-center space-x-3 px-4 py-2 rounded-lg font-bold transition-all ${
        isWarning
          ? 'bg-error-100 dark:bg-error-900 text-error-700 dark:text-error-300 animate-pulse'
          : 'bg-primary-100 dark:bg-primary-900 text-primary-700 dark:text-primary-300'
      }`}
    >
      <Clock className="w-5 h-5" />
      <div className="font-mono text-lg">
        {formatTime(minutes)}:{formatTime(seconds)}
      </div>
    </div>
  );
}
