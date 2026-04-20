# Quick Start Guide - ActuarialPrep Frontend

## 🚀 Get Running in 3 Steps

### Step 1: Install Dependencies
```bash
cd "/Users/emmanuelhackman/SOA exams website/frontend"
npm install
```
**Time**: ~2-3 minutes

### Step 2: Start Development Server
```bash
npm run dev
```
**Output**: Server runs on http://localhost:3001

### Step 3: Open in Browser
Visit http://localhost:3001 in your browser!

---

## 📋 What You Get

### Landing Page
- Hero section with call-to-action
- Feature highlights
- All 7 exam cards (P, FM, FAM, ALTAM, ASTAM, SRM, PA)
- Statistics section
- Professional footer

### Authentication
- **Login Page**: Email/password login with demo credentials
  - Demo Email: `demo@actuarialprep.com`
  - Demo Password: `demo123`
- **Registration Page**: Create new account

### Dashboard
- Main stats (questions answered, accuracy, streak, time)
- Readiness scores for all exams
- Weak topics identification
- Recent activity feed
- Quick access to all features

### Practice Questions
- Full-featured question display
- 5 multiple-choice options (A-E)
- Progress tracking
- Timer
- Results with explanations
- Difficulty indicators

### Analytics
- Accuracy over time (line chart)
- Topic mastery breakdown (bar chart)
- Readiness gauge (circular)
- Time distribution
- Weakness alerts

### Study Plans
- Weekly schedule
- Daily tasks
- Topic allocation
- Progress tracking
- Study recommendations

### Video Library
- Search and filter lessons
- Progress indicators
- Lesson cards with details
- Status tracking (completed, in-progress, not-started)

### Admin Panel (if user is admin)
- User management
- Question templates
- Platform analytics

---

## 🔌 API Configuration

The app expects a backend at `http://localhost:8001/api`

Create `.env.local` (optional):
```
NEXT_PUBLIC_API_URL=http://localhost:8001/api
```

Currently uses **mock data** - no backend needed for testing!

---

## 🎨 Customize

### Change Brand Colors
Edit `tailwind.config.ts`:
```typescript
colors: {
  primary: { 700: '#1a365d' }, // Deep blue
  accent: { 500: '#d69e2e' },  // Gold
  success: { 500: '#38a169' }, // Green
  error: { 500: '#e53e3e' },   // Red
}
```

### Change API Endpoint
Update in `src/lib/api.ts` or `.env.local`:
```
NEXT_PUBLIC_API_URL=your-api-url
```

### Update Exam List
Edit in pages that reference exams:
- `src/app/page.tsx` - Landing page
- `src/components/Sidebar.tsx` - Navigation

---

## 📂 Important Files

| File | Purpose |
|------|---------|
| `package.json` | Dependencies |
| `src/app/page.tsx` | Landing page |
| `src/lib/api.ts` | API client |
| `src/lib/store.ts` | State management |
| `src/types/index.ts` | Type definitions |
| `tailwind.config.ts` | Styling config |

---

## 🧪 Test the App

### Try These Routes
- `/` - Landing page
- `/login` - Login (use demo account)
- `/register` - Create account
- `/dashboard` - Main dashboard
- `/practice/P` - Practice Exam P
- `/analytics` - View analytics
- `/study-plan` - Study schedule
- `/video-lessons` - Video library
- `/admin` - Admin panel (admin only)

### Test Features
1. **Login**: Use demo credentials on login page
2. **Practice**: Navigate to practice section
3. **View Analytics**: Check performance charts
4. **Admin**: Try admin panel (mock data)

---

## ⚙️ Build Commands

```bash
# Development
npm run dev          # Start dev server on port 3001

# Production
npm run build        # Build for production
npm start            # Start production server

# Linting
npm run lint         # Run ESLint
```

---

## 📱 Responsive Design

App is fully responsive:
- ✅ Desktop (1920px+)
- ✅ Tablet (768px-1920px)
- ✅ Mobile (320px-768px)

Test using Chrome DevTools device emulation!

---

## 🌙 Dark Mode

All components support dark mode automatically. Browser respects system preference.

Test: Open DevTools → Toggle `prefers-color-scheme` in CSS media queries.

---

## 🐛 Troubleshooting

### Port 3001 Already in Use
```bash
# Use different port
npm run dev -- --p 3001
```

### Dependencies Not Installing
```bash
# Clear cache and retry
rm -rf node_modules package-lock.json
npm install
```

### API Connection Issues
- Ensure backend is running on port 8001
- Check `.env.local` has correct API URL
- Currently works with mock data - no backend needed!

---

## 📚 Documentation

For more details, see:
- **README.md** - Full documentation
- **PROJECT_STRUCTURE.md** - Architecture details
- **IMPLEMENTATION_SUMMARY.md** - What was built

---

## 🎯 Next Steps

1. ✅ Install and run (`npm install && npm run dev`)
2. ✅ Test the landing page and features
3. ✅ Customize colors/branding as needed
4. ✅ Connect to backend when ready
5. ✅ Deploy to production

---

## 💡 Tips

- **Hot Reload**: Changes save automatically during dev
- **Dark Mode**: Press `⌘K` to toggle theme (if implemented)
- **Mobile Testing**: Use Chrome DevTools device emulation
- **Component Preview**: All components are standalone and reusable
- **Type Safety**: Full TypeScript for zero runtime errors

---

## 🚀 Ready to Go!

Your ActuarialPrep frontend is ready to use. Start with:

```bash
cd "/Users/emmanuelhackman/SOA exams website/frontend"
npm install
npm run dev
```

Visit http://localhost:3001 and explore!

---

**Questions?** Check the documentation files or review the component code - all files are well-commented!
