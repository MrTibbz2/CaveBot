# Project Overview

## Project Description

This robotics project implements an autonomous navigation system using multiple components working together to provide real-time sensor data collection, processing, and robot control. The system combines embedded firmware, serial communication, web-based visualization, and robot movement control.

## Key Features

- **Real-time sensor data collection** using 8 HC-SR04 ultrasonic sensors
- **Dual-core processing** on Raspberry Pi Pico for concurrent operations
- **Web-based simulation and mapping** interface with live data visualization
- **Robot movement control** via LEGO Spike Prime with PyBricks
- **Structured communication protocols** for reliable data exchange
- **Comprehensive testing framework** for all system components

## Technology Stack

### Embedded Systems
- **Raspberry Pi Pico (RP2040)**: Dual-core ARM Cortex-M0+ microcontroller
- **C++**: Firmware development with Pico SDK
- **CMake + Ninja**: Build system for cross-compilation
- **ARM GNU Toolchain**: Cross-compiler for ARM architecture

### Communication & Interface
- **Python**: Serial interface and system integration
- **PySerial**: USB serial communication library
- **JSON**: Structured message format for data exchange
- **WebSockets**: Real-time web communication

### Web Interface
- **FastAPI**: Modern Python web framework
- **HTMX**: Dynamic web interactions
- **Tailwind CSS**: Utility-first CSS framework
- **JavaScript Canvas**: 2D graphics and mapping
- **Turtle Graphics**: Robot simulation

### Robot Control
- **PyBricks**: Python framework for LEGO robotics
- **Bluetooth LE**: Wireless communication to robot
- **LEGO Spike Prime**: Educational robotics platform

## System Components

### 1. Pico Firmware (`microcontrollers/`)
**Purpose**: Sensor data collection and real-time processing

**Key Features**:
- Dual-core architecture (Core0: commands, Core1: sensors)
- 8-sensor HC-SR04 ultrasonic distance measurement
- Structured JSON output format
- Command-based operation (START/STOP/STATUS)
- Thread management and error handling

**Communication Protocol**:
```
Format: <IDENTIFIER>: { "type": "<TYPE>", "status": "<STATUS>", "payload": {<DATA>} }
Commands: CMD_START_SENSORREAD, CMD_STOP, CMD_STATUS
```

### 2. RPI Serial Interface (`rpi/`)
**Purpose**: Bridge between Pico and web interface

**Key Features**:
- Automatic Pico device detection
- Threaded serial data reading
- JSON message parsing and validation
- WebSocket data forwarding
- Connection management and error recovery

**Data Flow**:
```
Pico (USB Serial) → RPI (Parser) → Web UI (WebSocket)
```

### 3. Web UI (`UI/`)
**Purpose**: Visualization, simulation, and system control

**Key Features**:
- Real-time sensor data visualization
- Robot simulation with turtle graphics
- 2D mapping interface
- WebSocket communication
- Interactive controls for robot movement

**Technologies**:
- FastAPI backend with WebSocket support
- HTML/CSS/JavaScript frontend
- Canvas-based mapping and visualization

### 4. Spike Prime Control (`spikeprime/`)
**Purpose**: Physical robot movement and motor control

**Key Features**:
- Bluetooth LE communication
- PyBricks-based motor control
- Movement commands (forward, backward, turn)
- Status monitoring and error handling

**API**:
```python
prime = Prime("HUB_NAME")
prime.moveForward(100)  # Move 100cm forward
prime.turnLeft(90)      # Turn 90 degrees left
```

## Development Setup Summary

### Prerequisites
- Windows 10/11 development environment
- Python 3.8+ with pip
- CMake and Ninja build tools
- ARM GNU Toolchain for cross-compilation
- Visual Studio Code with extensions

### Build Process
1. **Pico Firmware**: CMake build system with Pico SDK
2. **Python Components**: Direct execution with dependency management
3. **Web UI**: FastAPI development server
4. **Spike Prime**: PyBricks code upload via web interface

### Installation Steps
```bash
# Pico toolchain
choco install ninja cmake
# Download ARM GNU Toolchain from ARM Developer

# Python dependencies
pip install fastapi uvicorn jinja2 websockets pyserial bleak

# Build Pico firmware
cd microcontrollers && mkdir build && cd build
cmake .. && make
```

## Communication Protocols

### Pico Output Format
```json
{
  "identifier": "Core1|Command|INFO|ERROR",
  "type": "data_stream|thread_status|system_status", 
  "status": "active|success|ready|failure",
  "payload": { "sensor_data": [...] }
}
```

### Web UI WebSocket Format
```json
{
  "type": "data_stream|log",
  "subtype": "distance_read|pico_info",
  "timestamp": "2025-01-01T12:00:00Z",
  "payload": { "sensor_leftfront": 150.2 }
}
```

## Hardware Configuration

### Sensor Layout (8 HC-SR04 sensors)
```
    Front
     ↑
[FL] [FR]  ← frontleft, frontright (0° from heading)
[LF]   [RF] ← leftfront, rightfront (90°, 270°)  
[LB]   [RB] ← leftback, rightback (90°, 270°)
[BL] [BR]  ← backleft, backright (180°)
     ↓
    Back
```

### Pico GPIO Assignments
- GP2-GP3: Front Left sensor (Trigger/Echo)
- GP4-GP5: Front Right sensor
- GP6-GP7: Left Front sensor
- GP8-GP9: Left Back sensor
- GP10-GP11: Right Front sensor
- GP12-GP13: Right Back sensor
- GP14-GP15: Back Left sensor
- GP16-GP17: Back Right sensor

## Testing Framework

### Test Structure
```
tests/
├── test_ui_simulation.py       # UI and simulation tests
├── test_rpi_serial.py         # Serial communication tests
├── test_spikeprime_commands.py # Robot control tests
├── test_integration.py        # End-to-end system tests
└── run_tests.py              # Test runner
```

### Test Categories
- **Unit Tests**: Individual component functionality
- **Integration Tests**: Inter-component communication
- **Mock Tests**: Hardware simulation for CI/CD
- **Hardware-in-Loop**: Real hardware validation

## Project Status & Next Steps

### Completed Components
- ✅ Pico firmware with sensor reading
- ✅ RPI serial interface
- ✅ Web UI with simulation
- ✅ Spike Prime control API
- ✅ Communication protocols
- ✅ Testing framework
- ✅ Documentation

### Development Priorities
1. **System Integration**: End-to-end testing with all components
2. **Mapping Algorithm**: 2D SLAM implementation
3. **Navigation Logic**: Path planning and obstacle avoidance
4. **Performance Optimization**: Real-time processing improvements
5. **Error Recovery**: Robust failure handling

### Future Enhancements
- Machine learning for improved navigation
- Multi-robot coordination
- Advanced mapping algorithms (occupancy grids)
- Mobile app interface
- Cloud data logging and analysis

## Getting Started

1. **Hardware Setup**: Follow [Hardware Guide](hardware-guide.md)
2. **Software Installation**: Follow [Setup Guide](setup-guide.md)
3. **System Testing**: Use [Testing Guide](testing-guide.md)
4. **API Integration**: Reference [API Documentation](api-reference.md)
5. **Architecture Understanding**: Review [System Architecture](system-architecture.md)

## Support & Troubleshooting

- Check individual component documentation for specific issues
- Use test framework to isolate problems
- Monitor serial output for debugging information
- Verify hardware connections and power supply
- Ensure all dependencies are properly installed