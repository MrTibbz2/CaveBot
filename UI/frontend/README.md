# CaveBot Frontend

Modern Preact-based frontend for the CaveBot UI application.

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

3. Build for production:
```bash
npm run build
```

## Architecture

- **Preact**: Lightweight React alternative for component-based UI
- **Vite**: Fast build tool and dev server
- **Tailwind CSS**: Utility-first CSS framework
- **Desmos API**: Interactive mathematical graphing

## Components

- `App.jsx`: Main application component
- `Navbar.jsx`: Top navigation bar
- `Sidebar.jsx`: Resizable sidebar with logs and controls
- `MapContainer.jsx`: Desmos map visualization container

## Libraries

- `websocket.js`: WebSocket connection management
- `desmos.js`: Desmos calculator initialization
- `bot.js`: Robot state and movement logic
- `mapper.js`: Sensor data processing and point plotting
- `expressions.js`: Default desmos mathematical expressions

## Integration

The frontend builds to `../static/dist/` to integrate with the existing FastAPI backend serving static files.