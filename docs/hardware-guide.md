# Hardware Setup Guide

## Component Overview

### Raspberry Pi Pico
- **Model**: Raspberry Pi Pico (RP2040)
- **Purpose**: Sensor data collection and processing
- **Connections**: USB serial to RPI, GPIO pins to sensors

### HC-SR04 Ultrasonic Sensors
- **Quantity**: 8 sensors
- **Range**: 2cm - 400cm
- **Accuracy**: ±3mm
- **Operating Voltage**: 5V DC

### LEGO Spike Prime Hub
- **Purpose**: Robot movement and motor control
- **Communication**: Bluetooth LE to computer
- **Firmware**: PyBricks (replaces LEGO firmware)

### Raspberry Pi (Interface)
- **Model**: Any Pi with USB ports
- **Purpose**: Serial communication bridge
- **OS**: Raspberry Pi OS or compatible Linux

## Wiring Diagrams

### Pico to HC-SR04 Sensor Connections

```
Pico GPIO Layout:
┌─────────────────────────────────────┐
│  GP0  GP1  GND  GP2  GP3  GP4  GP5 │
│  GP6  GP7  GND  GP8  GP9  GP10 GP11│
│  GP12 GP13 GND GP14 GP15 3V3  GP16 │
│  GP17 GND GP18 GP19 GP20 GP21 GP22 │
│  RUN  GP26 GP27 GND  GP28 ADC  3V3 │
│  3V3  VSYS GND  EN   GND  VBUS    │
└─────────────────────────────────────┘
```

### Sensor Pin Assignments
| Sensor Position | Trigger Pin | Echo Pin |
|----------------|-------------|----------|
| Front Left     | GP2         | GP3      |
| Front Right    | GP4         | GP5      |
| Left Front     | GP6         | GP7      |
| Left Back      | GP8         | GP9      |
| Right Front    | GP10        | GP11     |
| Right Back     | GP12        | GP13     |
| Back Left      | GP14        | GP15     |
| Back Right     | GP16        | GP17     |

### Power Distribution
- **5V Supply**: External power supply for HC-SR04 sensors
- **3.3V**: Pico internal supply for logic levels
- **Ground**: Common ground for all components

```
Power Supply Schematic:
5V Supply ──┬── HC-SR04 VCC (×8)
            │
            └── Level Shifter (5V side)
            
Pico 3.3V ──┬── Level Shifter (3.3V side)
            │
            └── Pico GPIO pins
            
Common GND ──┴── All component grounds
```

## Physical Mounting

### Robot Chassis Layout
```
    Front
     ↑
[FL] [FR]  ← Front sensors
[LF]   [RF] ← Side sensors  
[LB]   [RB] ← Side sensors
[BL] [BR]  ← Back sensors
     ↓
    Back
```

### Sensor Positioning
- **Height**: 10-15cm above ground
- **Angle**: Perpendicular to robot surface
- **Clearance**: 5cm minimum from obstacles
- **Protection**: Sensor housings recommended

### Cable Management
- Use ribbon cables for organized wiring
- Secure cables to prevent interference with movement
- Label all connections for maintenance
- Provide strain relief at connection points

## Spike Prime Configuration

### Motor Connections
- **Port A**: Left drive motor
- **Port B**: Right drive motor  
- **Port C**: Optional auxiliary motor
- **Port D**: Optional auxiliary motor

### Sensor Connections (Optional)
- **Port 1**: Color sensor (if used)
- **Port 2**: Distance sensor (if used)
- **Port 3**: Force sensor (if used)
- **Port 4**: Gyro sensor (built-in)

### PyBricks Firmware Installation
1. Connect hub via USB
2. Visit [code.pybricks.com](https://code.pybricks.com)
3. Follow firmware installation wizard
4. Verify installation with test program

## Testing and Calibration

### Sensor Testing
```python
# Test individual sensor
def test_sensor(trigger_pin, echo_pin):
    # Send trigger pulse
    # Measure echo response
    # Calculate distance
    # Verify range and accuracy
```

### Calibration Procedure
1. **Distance Calibration**
   - Place known objects at measured distances
   - Record sensor readings
   - Calculate correction factors
   - Update firmware constants

2. **Angular Calibration**
   - Verify sensor mounting angles
   - Test detection patterns
   - Adjust physical positioning if needed

### System Integration Test
1. Power on all components
2. Verify serial communication
3. Test sensor data flow
4. Validate movement commands
5. Check emergency stop functionality

## Troubleshooting

### Common Hardware Issues

#### Sensor Problems
- **No readings**: Check power and wiring
- **Erratic readings**: Verify ground connections
- **Short range**: Clean sensor surfaces
- **Interference**: Separate sensors physically

#### Communication Issues
- **No serial data**: Check USB connections
- **Garbled data**: Verify baudrate settings
- **Intermittent connection**: Check cable integrity

#### Power Issues
- **System resets**: Check power supply capacity
- **Voltage drops**: Verify wire gauge and connections
- **Noise**: Add decoupling capacitors

### Diagnostic Tools
- Multimeter for voltage/continuity testing
- Oscilloscope for signal analysis
- Logic analyzer for digital communication
- Serial terminal for message monitoring

## Safety Considerations

### Electrical Safety
- Use appropriate fuses/circuit breakers
- Verify polarity before connecting power
- Isolate high and low voltage sections
- Provide emergency stop capability

### Mechanical Safety
- Secure all mounting hardware
- Protect exposed wiring
- Ensure stable robot base
- Test emergency stop procedures

### Software Safety
- Implement watchdog timers
- Add bounds checking for all inputs
- Provide graceful failure modes
- Log all system events for debugging