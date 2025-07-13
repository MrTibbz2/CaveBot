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

- `App.jsx`: Main application component with routing and WebSocket management
- `Navbar.jsx`: Top navigation bar with battery status and SSH connection indicator
- `Sidebar.jsx`: Resizable sidebar with logs and controls
- `MapContainer.jsx`: Desmos map visualization container
- `Terminal.jsx`: SSH terminal component with connection form and command interface

## Libraries

- `readingswebsocket.js`: WebSocket connection management for sensor data
- `sshwebsocket.js`: Dedicated WebSocket connection for SSH terminal
- `terminal.js`: Terminal input handling, command history, and keyboard shortcuts
- `desmos.js`: Desmos calculator initialization
- `bot.js`: Robot state and movement logic
- `mapper.js`: Sensor data processing and point plotting
- `mapperlib.js`: Core mapping utilities and sensor calculations
- `vecmath.js`: Vector math API calls for position calculations
- `expressions.js`: Default desmos mathematical expressions

## Pages

- `mapWindow.jsx`: Main map view with sidebar and Desmos integration
- `CLI.jsx`: SSH terminal page with persistent state and connection management
- `NotFound.jsx`: 404 error page with particle background

## Integration

The frontend builds to `../static/dist/` to integrate with the existing FastAPI backend serving static files.

## State Management

- **Global SSH State**: Terminal output and connection status persist across tab navigation
- **WebSocket Connections**: Separate connections for sensor data and SSH terminal
- **Event System**: Custom events for cross-component communication (SSH status updates)