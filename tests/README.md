# Tests Directory

This directory contains the complete test suite for the innovation-team robotics project.

## Quick Start

```bash
# Install test dependencies
pip install -r requirements.txt

# Run all tests
python run_tests.py

# Run specific test module
python -m unittest test_ui_simulation.py -v
```

## Test Files

- `test_ui_simulation.py` - Tests for UI simulation and turtle graphics
- `test_rpi_serial.py` - Tests for RPI serial interface communication
- `test_spikeprime_commands.py` - Tests for Spike Prime robot control
- `test_integration.py` - System integration and end-to-end tests
- `run_tests.py` - Main test runner script

## Test Coverage

The test suite covers:
- ✅ Sensor simulation and collision detection
- ✅ Serial communication and message parsing  
- ✅ Robot command validation and BLE communication
- ✅ System integration and data flow
- ✅ Error handling and edge cases

## Dependencies

- `pytest` - Modern testing framework
- `pytest-mock` - Mocking utilities
- `unittest-mock` - Standard library mocking

## Usage Examples

```bash
# Run with verbose output
python -m unittest test_ui_simulation.py -v

# Run specific test method
python -m unittest test_ui_simulation.TestRobotSimulator.test_line_intersection_basic

# Run with pytest (alternative)
pytest tests/ -v
```

For detailed testing information, see [Testing Guide](../docs/testing-guide.md).