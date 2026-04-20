import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'ActuarialPrep - Master Your SOA Exams',
  description: 'Adaptive learning platform for actuarial exam preparation with AI-powered practice questions and personalized study plans.',
  keywords: 'actuarial exams, SOA, exam prep, practice questions, study plan',
  openGraph: {
    title: 'ActuarialPrep - Master Your SOA Exams',
    description: 'Adaptive learning platform for actuarial exam preparation',
    type: 'website',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        {children}
      </body>
    </html>
  );
}
