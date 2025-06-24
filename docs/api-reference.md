# API Reference

## Pico Communication Protocol

### Command Format (Python → Pico)
Commands sent to Pico are simple string commands:

#### System Commands
- `CMD_STATUS` - Request system status (blocking Core0 operation)
- `CMD_STOP` - Terminate currently running Core1 thread

#### Core1 Commands  
- `CMD_START_<COMMAND_NAME>` - Start specific task on Core1
  - `CMD_START_SENSORREAD` - Begin continuous sensor reading

### Response Format (Pico → Python)
All Pico responses follow structured JSON format:

```
<IDENTIFIER>: { "type": "<MESSAGE_TYPE>", "status": "<STATUS_CODE>", "payload": {<DATA>} }
```

#### Identifiers
- `Core1` - Messages from Core1 thread
- `Command` - Command execution results  
- `INFO` - System information
- `ERROR` - Error messages

#### Message Types
- `data_stream` - Sensor data transmission
- `thread_status` - Core1 thread lifecycle events
- `system_status` - System health information
- `command_response` - Command execution results

#### Status Codes
- `active` - Thread/system is running
- `success` - Command completed successfully
- `failure` - Command failed
- `ready` - System ready for commands
- `thread_started` - Core1 thread initiated
- `thread_stopped` - Core1 thread terminated
- `thread_locked` - Core1 busy, cannot start new thread

### Example Messages

#### Sensor Data Stream
```json
Core1: {
  "type": "data_stream",
  "status": "active", 
  "payload": [
    {"sensor_id": "front_left", "average": 150.2},
    {"sensor_id": "rear_right", "average": 199.7}
  ]
}
```

#### System Status
```json
INFO: {
  "type": "system_status",
  "status": "ready",
  "details": {"firmware_version": "1.0.1"}
}
```

#### Error Response
```json
ERROR: {
  "type": "core1_management",
  "code": "THREAD_LOCKED",
  "message": "Core1 busy, cannot start new thread."
}
```

## Web UI WebSocket Protocol

### Message Format
```json
{
  "type": "<MESSAGE_TYPE>",
  "subtype": "<SUBTYPE>", 
  "timestamp": "2025-01-01T12:00:00Z",
  "payload": { /* message data */ }
}
```

### Message Types

#### Data Stream
```json
{
  "type": "data_stream",
  "subtype": "distance_read",
  "timestamp": "2025-01-01T12:00:00Z",
  "payload": {
    "sensor_leftfront": 150.2,
    "sensor_rightfront": 200.0,
    "sensor_leftback": 180.5
  }
}
```

#### Log Messages
```json
{
  "type": "log",
  "subtype": "pico_info",
  "timestamp": "2025-01-01T12:00:00Z", 
  "payload": {
    "message": "System initialized successfully"
  }
}
```

## Spike Prime API

### Prime Class Methods

#### Connection
```python
prime = Prime("HUB_NAME")  # Connect to named hub
```

#### Movement Commands
```python
prime.moveForward(distance_cm)    # Move forward specified distance
prime.moveBackward(distance_cm)   # Move backward specified distance  
prime.turnLeft(angle_degrees)     # Turn left by angle
prime.turnRight(angle_degrees)    # Turn right by angle
prime.stop()                      # Stop all motors
```

#### Special Commands
```python
prime.partyTime()                 # Execute celebration sequence
prime.getStatus()                 # Get hub status
```

### BLE Communication
- Uses `bleak` library for Bluetooth LE communication
- Automatic device discovery by hub name
- Command queuing for reliable transmission
- Connection retry logic with exponential backoff

## RPI Serial Interface

### PicoSerialInterface Class

#### Initialization
```python
interface = PicoSerialInterface(baudrate=115200)
```

#### Connection Methods
```python
result = interface.connect()           # Auto-detect and connect to Pico
port = interface._find_pico_port()     # Find Pico USB port
interface.disconnect()                 # Close serial connection
```

#### Communication Methods
```python
interface.send_command(command_str)    # Send command to Pico
interface.format_ostream()             # Parse incoming data (run in thread)
status = interface.poll_status()       # Request system status
```

#### Message Parsing
```python
parsed = interface._parse_pico_message(raw_message)
# Returns: {"identifier": "INFO", "type": "system_status", "status": "ready"}
```

## Error Codes

### Pico Error Codes
- `THREAD_LOCKED` - Core1 already running a task
- `SENSOR_INIT_FAIL` - Sensor initialization failed
- `CAL_TIMEOUT` - Sensor calibration timeout
- `UNKNOWN_COMMAND` - Invalid command received

### RPI Error Codes
- `CONNECTION_FAILED` - Cannot connect to Pico
- `PARSE_ERROR` - Invalid message format
- `TIMEOUT` - Communication timeout
- `PORT_NOT_FOUND` - Pico USB port not detected

### Spike Prime Error Codes
- `BLE_CONNECTION_FAILED` - Bluetooth connection error
- `HUB_NOT_FOUND` - Named hub not discoverable
- `COMMAND_TIMEOUT` - Command execution timeout
- `INVALID_PARAMETER` - Invalid command parameter

## Data Validation

### Sensor Data Validation
- Distance values: 0-400 cm (HC-SR04 range)
- Invalid readings: -1 (sensor error)
- Timestamp format: ISO 8601 UTC
- Sensor names: predefined set of 8 sensors

### Command Validation
- Distance parameters: positive numbers only
- Angle parameters: 0-360 degrees
- String commands: predefined command set
- JSON format: strict schema validation