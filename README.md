# AI Job Counselling System - Frontend

A modern React 18 application with Vite for AI-powered job counselling and career guidance.

## 📋 Features

✅ **Resume Upload** - Upload and analyze resumes (PDF, DOCX, TXT)  
✅ **Skill Extraction** - Automatically extract skills from resume  
✅ **Job Matching** - Get AI-powered job recommendations based on your skills  
✅ **Interactive Chatbot** - Talk to AI assistant for career guidance  
✅ **Modern UI** - Dark theme with smooth animations  
✅ **Responsive Design** - Works on desktop, tablet, and mobile  
✅ **Real-time Updates** - Live skill and job matching  

## 🛠️ Technology Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Axios** - HTTP client
- **React Router v6** - Client-side routing
- **CSS3** - Styling with animations and gradients

## 📂 Project Structure

```
Frontend/
├── src/
│   ├── api/
│   │   ├── chatbot_api.js
│   │   ├── jobs_api.js
│   │   └── resume_api.js
│   ├── components/
│   │   ├── Chatbot.jsx & Chatbot.css
│   │   ├── Hero.jsx & Hero.css
│   │   ├── JobCard.jsx & JobCard.css
│   │   ├── JobList.jsx & JobList.css
│   │   ├── navbar.jsx & navbar.css
│   │   ├── ResumeUpload.jsx & ResumeUpload.css
│   │   ├── SkillChips.jsx & SkillChips.css
│   │   └── SkillList.jsx & SkillList.css
│   ├── pages/
│   │   ├── Home.jsx & Home.css
│   │   └── Dashboard.jsx & Dashboard.css
│   ├── app.jsx & app.css
│   ├── index.js
│   └── index.css
├── index.html
├── vite.config.js
├── package.json
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Node.js 16.x or higher
- npm or yarn
- Backend server running on http://127.0.0.1:8000

### Installation

1. **Navigate to Frontend directory**
```bash
cd Frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Create environment file**
```bash
cp .env.example .env
```

4. **Verify .env settings**
```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

### Development

Start the development server:
```bash
npm run dev
```

The application will open automatically at `http://localhost:3000`

### Production Build

Build for production:
```bash
npm run build
```

Preview the build:
```bash
npm run preview
```

## 📝 Component Overview

### 🏠 Pages

#### **Home Page** (`pages/Home.jsx`)
- Landing page with navigation
- Hero section with call-to-action
- Smooth animations and background effects

#### **Dashboard Page** (`pages/Dashboard.jsx`)
- Resume upload section
- Skill extraction and display
- Job recommendations
- Chatbot assistant
- Two-column responsive layout

### 🎨 Components

#### **Navbar** (`components/navbar.jsx`)
- Sticky navigation
- Dark theme with blur background
- Responsive mobile menu
- Smooth hover animations

#### **Hero Section** (`components/Hero.jsx`)
- Large landing heading with gradient text
- Subheading explaining features
- Call-to-action button
- Animated background orbs

#### **Resume Upload** (`components/ResumeUpload.jsx`)
- Drag-and-drop file upload
- File validation
- Loading state
- Success state with extracted data
- Skill chips display

#### **Skill Chips** (`components/SkillChips.jsx`)
- Display skills as rounded badges
- Gradient backgrounds
- Hover animations
- Multiple color schemes

#### **Skill List** (`components/SkillList.jsx`)
- List view of extracted skills
- Statistics footer
- Empty state
- Responsive grid layout

#### **Job Card** (`components/JobCard.jsx`)
- Individual job display
- Match score progress bar
- Company and location info
- Required skills list
- Color-coded matching (green/orange/red)

#### **Job List** (`components/JobList.jsx`)
- Display multiple job cards
- Loading state
- Empty state message
- Responsive grid layout

#### **Chatbot** (`components/Chatbot.jsx`)
- Chat interface with messages
- User and bot message styling
- Input box with character count
- Loading indicator
- Clear chat functionality
- Auto-scroll to latest message

### 🔌 API Helpers

#### **resume_api.js**
```javascript
uploadResume(file)        // Upload and extract skills
getUploadedResumes()      // Fetch previous uploads
deleteResume(resumeId)    // Delete resume
```

#### **jobs_api.js**
```javascript
matchJobs(skills)         // Get job recommendations
searchJobs(params)        // Search by keyword/location
getJobDetails(jobId)      // Get detailed job info
getAllJobs(params)        // Fetch all jobs with pagination
```

#### **chatbot_api.js**
```javascript
sendMessage(message)      // Send message to chatbot
sendMessageWithContext()  // Send with user context
getConversationHistory()  // Fetch conversation history
clearConversationHistory() // Clear chat history
getSuggestions(params)    // Get AI suggestions
```

## 🎨 Styling

All components use custom CSS with:
- **Dark modern theme** - Slate and dark blue colors
- **Gradients** - Green, blue, purple, and pink gradients
- **Animations** - Smooth transitions and keyframe animations
- **Responsive design** - Mobile-first approach with media queries
- **Glassmorphism** - Frosted glass effects with backdrop blur
- **Box shadows** - Depth and elevation effects

### Color Palette

```css
Primary Colors:
- Emerald Green: #10b981
- Cobalt Blue: #3b82f6
- Violet Purple: #8b5cf6
- Rose Pink: #ec4899
- Amber Orange: #f59e0b

Background:
- Dark: #0f172a
- Medium: #1e293b
- Light: #334155
```

## 📱 Responsive Breakpoints

- **Desktop**: 1024px and above
- **Tablet**: 768px to 1023px
- **Mobile**: Below 768px
- **Small Mobile**: Below 480px

## 🔧 Configuration

### Vite Config
- Dev server port: 3000
- Build output: `dist/`
- API proxy configured for backend calls

### API Configuration
Base URL is set in Axios instances:
```javascript
const client = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  timeout: 30000
});
```

## ⚡ Performance

- Lazy loading of routes
- Optimized images and animations
- Minimal bundle size
- CSS-only animations (no heavy libraries)

## 🐛 Debugging

Enable debug mode in browser console:
```javascript
localStorage.setItem('debug', 'true');
```

Check network calls in DevTools Network tab to verify API communication.

## 📦 Dependencies

### Core
- `react@^18.2.0` - UI framework
- `react-dom@^18.2.0` - DOM rendering
- `react-router-dom@^6.20.0` - Routing
- `axios@^1.6.2` - HTTP client

### Development
- `vite@^5.0.8` - Build tool
- `@vitejs/plugin-react@^4.2.1` - React plugin for Vite
- `eslint@^8.54.0` - Code linting
- `eslint-plugin-react@^7.33.2` - React linting rules

## 🚨 Troubleshooting

### Issue: Frontend can't connect to backend
**Solution**: Ensure backend is running on `http://127.0.0.1:8000`

### Issue: Styles not loading
**Solution**: Clear browser cache and rebuild with `npm run build`

### Issue: Hot reload not working
**Solution**: Restart dev server with `npm run dev`

### Issue: Port 3000 already in use
**Solution**: Change port in `vite.config.js` server.port

## 📖 Usage Examples

### Upload Resume
```javascript
import { uploadResume } from './api/resume_api';

const response = await uploadResume(file);
console.log(response.skills);
```

### Get Job Matches
```javascript
import { matchJobs } from './api/jobs_api';

const result = await matchJobs(['React', 'NodeJS']);
console.log(result.matchedJobs);
```

### Send Chat Message
```javascript
import { sendMessage } from './api/chatbot_api';

const response = await sendMessage('What jobs match my skills?');
console.log(response.reply);
```

## 🤝 Contributing

1. Make changes in a new branch
2. Test thoroughly
3. Ensure responsive design works
4. Follow the existing code style

## 📄 License

This project is part of the AI Job Counselling System.

## 📞 Support

For issues or questions, check the backend API documentation or contact the development team.

---

**Built with ❤️ using React 18 & Vite**
