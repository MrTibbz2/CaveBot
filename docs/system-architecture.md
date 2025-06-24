# System Architecture

## Overview

The robotics system consists of four main components that work together to provide autonomous navigation and mapping capabilities:

1. **Pico Microcontroller** - Sensor data collection and processing
2. **Raspberry Pi Interface** - Serial communication bridge
3. **Web UI** - Visualization, simulation, and mapping
4. **Spike Prime** - Robot movement and control

## Component Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Pico Firmware │────│  RPI Interface  │────│    Web UI       │
│   (C++)         │    │   (Python)      │    │ (FastAPI/HTMX)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                                              │
         │                                              │
         └──────────────────────────────────────────────┘
                              │
                    ┌─────────────────┐
                    │  Spike Prime    │
                    │  (PyBricks)     │
                    └─────────────────┘
```

## Data Flow

### Sensor Data Pipeline
1. **Pico** collects distance sensor readings using HC-SR04 sensors
2. **Pico** formats data according to communication protocol
3. **RPI** receives serial data and parses JSON messages
4. **RPI** forwards processed data to Web UI via WebSocket
5. **Web UI** displays real-time sensor data and updates map

### Command Flow
1. **Web UI** sends movement commands
2. **RPI** processes and validates commands
3. **Spike Prime** receives movement instructions via BLE
4. **Spike Prime** executes motor commands for robot movement

## Communication Protocols

### Pico Output Format
```json
{
  "identifier": "Core1|Command|INFO|ERROR",
  "type": "data_stream|thread_status|system_status",
  "status": "active|success|ready|failure",
  "payload": { /* sensor data or messages */ }
}
```

### Web UI WebSocket Format
```json
{
  "type": "data_stream|log",
  "subtype": "distance_read|pico_info",
  "timestamp": "2025-01-01T12:00:00Z",
  "payload": {
    "sensor_leftfront": 150.2,
    "sensor_rightfront": 200.0
  }
}
```

## Sensor Configuration

The system uses 8 HC-SR04 ultrasonic sensors positioned around the robot:
- **leftfront, leftback** - Left side sensors (90° from robot heading)
- **rightfront, rightback** - Right side sensors (270° from robot heading)  
- **frontleft, frontright** - Front sensors (0° from robot heading)
- **backleft, backright** - Rear sensors (180° from robot heading)

## Threading Model

### Pico (Dual Core)
- **Core 0**: Command processing and serial communication
- **Core 1**: Sensor data collection and processing

### RPI
- **Main Thread**: Command processing and WebSocket management
- **Read Thread**: Continuous serial data reading from Pico

## Error Handling

- **Pico**: Returns structured error messages with error codes
- **RPI**: Implements connection retry logic and data validation
- **Web UI**: Displays connection status and error notifications
- **Spike Prime**: Handles BLE connection failures gracefully