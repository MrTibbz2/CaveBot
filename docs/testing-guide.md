# Testing Guide

## Overview

The testing framework provides comprehensive coverage for all system components including unit tests, integration tests, and hardware-in-the-loop testing.

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── test_ui_simulation.py       # UI simulation tests
├── test_rpi_serial.py         # RPI serial interface tests  
├── test_spikeprime_commands.py # Spike Prime command tests
├── test_integration.py        # System integration tests
├── requirements.txt           # Test dependencies
└── run_tests.py              # Test runner script
```

## Running Tests

### Quick Start
```bash
# Install test dependencies
cd tests/
pip install -r requirements.txt

# Run all tests
python run_tests.py
```

### Individual Test Modules
```bash
# Run specific test file
python -m unittest test_ui_simulation.py

# Run with verbose output
python -m unittest test_ui_simulation.py -v

# Run specific test method
python -m unittest test_ui_simulation.TestRobotSimulator.test_line_intersection_basic
```

### Using pytest (Alternative)
```bash
# Install pytest
pip install pytest pytest-mock

# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test
pytest tests/test_ui_simulation.py::TestRobotSimulator::test_sensor_config_integrity
```

## Test Categories

### Unit Tests

#### UI Simulation Tests (`test_ui_simulation.py`)
- **Line intersection calculations**: Verify sensor ray collision detection
- **Sensor configuration**: Validate sensor positioning and angles
- **Robot movement**: Test movement and rotation functions
- **Data structures**: Verify sensor data queue operations

```python
def test_line_intersection_basic(self):
    # Test basic line segment intersection
    p1, p2 = (0, 0), (10, 0)
    p3, p4 = (5, -5), (5, 5)
    result = self.simulator._line_segment_intersection(p1, p2, p3, p4)
    self.assertEqual(result, (5, 0))
```

#### RPI Serial Tests (`test_rpi_serial.py`)
- **Port detection**: Test Pico USB port discovery
- **Message parsing**: Validate JSON message parsing
- **Connection handling**: Test connection establishment and error recovery
- **Data validation**: Verify incoming data format compliance

```python
def test_parse_pico_message_valid_json(self):
    test_message = 'INFO: { "type": "system_status", "status": "ready" }'
    result = self.interface._parse_pico_message(test_message)
    expected = {'identifier': 'INFO', 'type': 'system_status', 'status': 'ready'}
    self.assertEqual(result, expected)
```

#### Spike Prime Tests (`test_spikeprime_commands.py`)
- **Command formatting**: Test BLE command structure
- **Parameter validation**: Verify input parameter checking
- **Connection management**: Test BLE connection handling
- **Error handling**: Validate error response processing

### Integration Tests (`test_integration.py`)

#### Data Flow Testing
- **Pico to UI pipeline**: Test complete data flow from sensors to UI
- **Command protocol consistency**: Verify command formats across components
- **Message transformation**: Test data format conversions
- **Timing and synchronization**: Validate real-time data handling

#### System Protocol Testing
- **Communication protocols**: Test all inter-component communication
- **Error propagation**: Verify error handling across system boundaries
- **State synchronization**: Test system state consistency
- **Recovery procedures**: Validate system recovery from failures

## Mock Testing

### Hardware Mocking
Tests use extensive mocking to simulate hardware components:

```python
@patch('turtle.Screen')
@patch('turtle.Turtle') 
def setUp(self, mock_turtle, mock_screen):
    self.simulator = RobotSimulator()

@patch('serial.Serial')
def test_serial_connection(self, mock_serial):
    interface = PicoSerialInterface(baudrate=115200)
    # Test without actual hardware
```

### BLE Mocking
```python
@patch('primeCommands.BLEConnection')
def test_spike_prime_commands(self, mock_ble):
    prime = Prime("TEST_HUB")
    prime.moveForward(100)
    mock_ble.return_value.send_command.assert_called()
```

## Test Data

### Sample Messages
```python
# Pico message format
PICO_SENSOR_MESSAGE = 'Core1: { "type": "data_stream", "status": "active", "payload": [ {"sensor_id": "front_left", "average": 150.2} ] }'

# UI WebSocket format  
UI_WEBSOCKET_MESSAGE = {
    "type": "data_stream",
    "subtype": "distance_read", 
    "timestamp": "2025-01-01T12:00:00Z",
    "payload": {"sensor_leftfront": 150.2}
}
```

### Test Fixtures
```python
# Sensor configuration test data
EXPECTED_SENSORS = ["leftfront", "leftback", "rightfront", "rightback", 
                   "frontleft", "frontright", "backleft", "backright"]

# Valid distance ranges
VALID_DISTANCE_RANGE = (0, 400)  # HC-SR04 sensor range in cm
```

## Hardware-in-the-Loop Testing

### Manual Testing Procedures

#### Pico Firmware Testing
1. Flash firmware to Pico
2. Connect to serial terminal
3. Send test commands: `CMD_STATUS`, `CMD_START_SENSORREAD`
4. Verify response format and timing
5. Test error conditions (invalid commands)

#### RPI Interface Testing
1. Connect Pico to RPI
2. Run `python main.py` in rpi/ directory
3. Monitor console output for connection messages
4. Verify data parsing and forwarding
5. Test reconnection after Pico reset

#### Web UI Testing
1. Start Web UI server
2. Open browser to `http://localhost:8000`
3. Verify WebSocket connection
4. Test simulation controls
5. Validate real-time data display

#### Spike Prime Testing
1. Upload PyBricks code to hub
2. Run Python control script
3. Test movement commands
4. Verify BLE communication
5. Test error recovery

### Automated Hardware Tests
```python
def test_end_to_end_data_flow():
    """Test complete data flow from Pico to UI"""
    # Start all system components
    # Send test sensor data from Pico
    # Verify data appears in UI
    # Validate data accuracy and timing
```

## Performance Testing

### Timing Tests
- **Sensor reading frequency**: Verify 10Hz minimum data rate
- **Communication latency**: Test serial and WebSocket delays
- **Command response time**: Measure command execution timing
- **System throughput**: Test maximum sustainable data rate

### Memory Tests
- **Memory usage**: Monitor RAM consumption over time
- **Memory leaks**: Test for memory growth during operation
- **Buffer overflow**: Test with high data rates
- **Resource cleanup**: Verify proper resource deallocation

## Continuous Integration

### Automated Test Execution
```yaml
# Example GitHub Actions workflow
name: Run Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.10
      - name: Install dependencies
        run: pip install -r tests/requirements.txt
      - name: Run tests
        run: python tests/run_tests.py
```

### Test Coverage
- Target: >90% code coverage
- Tools: `pytest-cov`, `coverage.py`
- Reports: HTML and XML coverage reports
- Integration: Coverage reporting in CI/CD pipeline

## Debugging Tests

### Common Test Failures

#### Import Errors
```bash
# Fix Python path issues
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python -m unittest tests.test_ui_simulation
```

#### Mock Issues
```python
# Verify mock setup
@patch('module.Class')
def test_function(self, mock_class):
    mock_class.return_value.method.return_value = expected_value
    # Test code here
    mock_class.assert_called_once()
```

#### Timing Issues
```python
# Use time mocking for consistent tests
@patch('time.time')
def test_timing(self, mock_time):
    mock_time.return_value = 1640995200  # Fixed timestamp
    # Test time-dependent code
```

### Test Debugging Tools
- **pdb**: Python debugger for interactive debugging
- **pytest --pdb**: Drop into debugger on test failure
- **logging**: Add debug logging to tests
- **assert messages**: Include descriptive assertion messages

```python
def test_with_debugging(self):
    result = function_under_test()
    self.assertEqual(result, expected, f"Expected {expected}, got {result}")
```