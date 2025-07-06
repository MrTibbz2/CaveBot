# Frontend Migration to Preact

## Overview

The CaveBot UI has been migrated from vanilla JavaScript to a modern Preact-based frontend while maintaining all existing functionality and backend compatibility.

## New Structure

```
UI/
├── frontend/                 # New Preact frontend
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── lib/             # Utility libraries
│   │   ├── App.jsx          # Main app component
│   │   ├── main.jsx         # Entry point
│   │   └── style.css        # Tailwind imports
│   ├── package.json         # Dependencies
│   ├── vite.config.js       # Build configuration
│   ├── tailwind.config.js   # Tailwind setup
│   └── index.html           # Dev HTML template
├── static/dist/             # Built frontend files
└── templates/index.html     # Updated to load Preact app
```

## VS Code Tasks

### Web Development Tasks
- **Start CaveBot (Full Stack)** - Runs backend + frontend dev servers
- **Start Backend** - FastAPI with uvicorn (cross-platform)
- **Start Frontend Dev** - Vite dev server with hot reload
- **Build Frontend** - Production build to static/dist/
- **Install Frontend Dependencies** - npm install
- **Start Production** - Build frontend then start backend

### Microcontroller Tasks (Existing)
- **Update Submodules** - Git submodule update
- **Configure Pico Project** - CMake configure
- **Build Pico Project** - CMake build  
- **Flash to Pico** - Copy .uf2 to Pico drive

### Usage
- `Ctrl+Shift+P` → "Tasks: Run Task" → Select desired task
- No default build task - shows selection menu

## Cross-Platform Support

All tasks work on Windows, macOS, and Linux:
- Backend uses `uvicorn` command (install: `pip install uvicorn`)
- Frontend uses `npm` (requires Node.js)
- Pico tasks use platform-specific file copy commands

## Development Workflow

### First Time Setup
```bash
cd UI/frontend
npm install
```

### Development
1. Run "Start CaveBot (Full Stack)" task
2. Backend: http://localhost:8000
3. Frontend dev: http://localhost:5173 (proxies to backend)

### Production
1. Run "Build Frontend" task
2. Run "Start Backend" task
3. Access: http://localhost:8000

## Features Preserved

✅ Identical UI/UX with Tailwind CSS  
✅ Desmos map integration  
✅ WebSocket real-time communication  
✅ Resizable sidebar  
✅ Robot movement tracking  
✅ Sensor data visualization  
✅ All backend APIs unchanged  

## Technical Details

- **Framework**: Preact (lightweight React alternative)
- **Build Tool**: Vite (fast dev server + build)
- **Styling**: Tailwind CSS (unchanged)
- **State Management**: Preact hooks
- **WebSocket**: Custom hook for connections
- **Map**: Desmos API integration maintained

## Migration Benefits

- Component-based architecture
- Hot module replacement in development
- Modern JavaScript tooling
- Better code organization
- Maintainable codebase
- TypeScript ready (if needed later)