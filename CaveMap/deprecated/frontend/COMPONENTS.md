# Component Documentation

## Terminal.jsx

Interactive SSH terminal component with connection management.

**Props:**
- `onCommand(command)`: Callback for command execution
- `output[]`: Array of terminal output lines
- `isConnected`: SSH connection status
- `onConnect(connectionData)`: Callback for SSH connection
- `onDisconnect()`: Callback for SSH disconnection

**Features:**
- SSH connection form with host, port, username, password
- Command input with history navigation (arrow keys)
- Ctrl+C interrupt support
- Color-coded output (commands, errors, interrupts)
- Mac-style terminal window design

## Navbar.jsx

Top navigation bar with status indicators and routing.

**Features:**
- Battery status indicators (Pico and SPKPRM)
- Bot connection status
- SSH connection status (updates via custom events)
- Tab navigation with active state styling
- Responsive design with icons

**Events:**
- Listens for `ssh-status-change` custom events

## Sidebar.jsx

Resizable sidebar with logs and controls.

**Props:**
- `logs[]`: Array of log messages to display

**Features:**
- Resizable width with mouse drag
- Collapsible with toggle button
- Auto-scrolling log container
- Persistent width state

## MapContainer.jsx

Container for Desmos calculator integration.

**Features:**
- Desmos calculator initialization
- Window resize handling
- Bot calculator reference management
- Responsive container sizing

## App.jsx

Main application component with routing and WebSocket management.

**Features:**
- Preact Router setup
- WebSocket connection for sensor data
- Bot movement processing
- Log state management
- Route definitions for Map and CLI pages