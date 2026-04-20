# ActuarialPrep Frontend

A modern, responsive Next.js 14 (App Router) frontend for the ActuarialPrep platform - an adaptive learning system for actuarial exam preparation.

## Features

- **Adaptive Practice**: AI-powered questions that adapt to your skill level
- **Smart Analytics**: Detailed insights into performance and weak areas
- **Personalized Study Plans**: Custom schedules tailored to your goals
- **Video Lessons**: Comprehensive video explanations for every topic
- **Real-time Progress Tracking**: Track your improvement across all exams
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **HTTP Client**: Axios
- **Charts**: Recharts
- **Icons**: Lucide React

## Getting Started

### Prerequisites

- Node.js 18+ 
- npm or yarn

### Installation

1. Clone the repository:
```bash
cd "/Users/emmanuelhackman/SOA exams website/frontend"
```

2. Install dependencies:
```bash
npm install
```

3. Set up environment variables:
Create a `.env.local` file in the root directory:
```
NEXT_PUBLIC_API_URL=http://localhost:8001/api
```

### Development

Start the development server:
```bash
npm run dev
```

Open [http://localhost:3001](http://localhost:3001) in your browser to see the application.

### Build

Build for production:
```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── src/
│   ├── app/              # Next.js App Router pages
│   │   ├── (auth)/       # Authentication pages (login, register)
│   │   ├── (dashboard)/  # Protected dashboard routes
│   │   ├── layout.tsx    # Root layout
│   │   ├── page.tsx      # Landing page
│   │   └── globals.css   # Global styles
│   ├── components/       # Reusable React components
│   ├── hooks/           # Custom React hooks
│   ├── lib/             # Utility functions and state management
│   │   ├── api.ts       # API client with interceptors
│   │   └── store.ts     # Zustand stores
│   └── types/           # TypeScript interfaces
├── public/              # Static assets
├── tailwind.config.ts   # Tailwind CSS configuration
├── tsconfig.json        # TypeScript configuration
├── next.config.js       # Next.js configuration
└── package.json         # Dependencies
```

## Key Pages

### Authentication
- `/login` - User login page
- `/register` - User registration page

### Dashboard
- `/dashboard` - Main dashboard with stats and quick actions
- `/practice/[examCode]` - Practice questions for specific exam
- `/analytics` - Performance analytics and charts
- `/study-plan` - Personalized study schedule
- `/video-lessons` - Video lesson library
- `/admin` - Admin panel (admin only)

## Components

### Core Components
- **Navbar** - Top navigation bar with user menu
- **Sidebar** - Left sidebar with navigation
- **QuestionCard** - Question display with multiple choice options
- **ReadinessGauge** - Circular gauge showing readiness score
- **ExamCard** - Card component for exam shortcuts
- **Timer** - Countdown timer for timed sessions

## State Management

The app uses Zustand for state management with three main stores:

- **useAuthStore** - User authentication state
- **useExamSessionStore** - Current exam session state
- **useUiStore** - UI state (sidebar, theme)

## API Integration

The frontend communicates with the FastAPI backend at `http://localhost:8001/api`.

Key API modules:
- `authApi` - Authentication endpoints
- `questionApi` - Question endpoints
- `adaptiveApi` - Adaptive learning endpoints
- `sessionApi` - Session management
- `progressApi` - Progress tracking
- `studyPlanApi` - Study plan endpoints
- `videoApi` - Video lesson endpoints

## Styling

The app uses Tailwind CSS with custom brand colors:

- **Primary**: Deep Blue (#1a365d)
- **Accent**: Gold (#d69e2e)
- **Success**: Green (#38a169)
- **Error**: Red (#e53e3e)

### Custom Classes

Custom Tailwind components are defined in `globals.css`:
- `.btn` - Button base styles
- `.card` - Card/box component
- `.input-field` - Form input styles
- `.badge` - Badge component

## Performance Optimizations

- Code splitting with Next.js dynamic imports
- Image optimization
- CSS minification
- Tree-shaking of unused code
- Lazy loading of routes

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Deployment

The app can be deployed to Vercel, Netlify, or any Node.js hosting:

1. Build the app: `npm run build`
2. Deploy the `.next` directory and `public` folder
3. Set environment variables on your hosting platform

## Environment Variables

- `NEXT_PUBLIC_API_URL` - Backend API URL (required)

## Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit your changes (`git commit -m 'Add amazing feature'`)
3. Push to the branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## License

This project is proprietary software. All rights reserved.

## Support

For issues and questions, contact support@actuarialprep.com

## Mock Data

The application includes mock data for development and testing. Some key features use mock data while API integration is being completed:

- Practice questions
- User analytics
- Study plans
- Video lessons

These will be replaced with API calls once the backend is fully integrated.
