# Setup Guide

## Prerequisites

### Development Environment
- **Windows 10/11** (primary development platform)
- **Python 3.8+** (recommended: 3.10+)
- **Git** for version control
- **Visual Studio Code** (recommended IDE)

### Hardware Requirements
- **Raspberry Pi Pico** with HC-SR04 sensors
- **Raspberry Pi** (for serial interface)
- **LEGO Spike Prime** hub with PyBricks firmware
- **Computer with Bluetooth LE** support

## Component Setup

### 1. Pico Microcontroller Setup

#### Install Build Tools
```bash
# Install CMake
# Download from: https://cmake.org/download/

# Install Ninja (using Chocolatey)
choco install ninja

# Install ARM GNU Toolchain
# Download: https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads
# Get: arm-gnu-toolchain-14.2.rel1-mingw-YOUR_SYSTEM-arm-none-eabi.exe
```

#### Configure Environment
1. Add CMake to PATH
2. Add ARM GNU Toolchain to PATH
3. Install CMake Tools extension in VS Code
4. Run `cmake: Configure` in VS Code

#### Build Firmware
```bash
cd microcontrollers/
mkdir build
cd build
cmake ..
make
```

### 2. Raspberry Pi Interface Setup

#### Install Dependencies
```bash
cd rpi/
pip install pyserial
```

#### Configure Serial Connection
- Connect Pico to RPI via USB
- Verify connection: `ls /dev/ttyACM*` (Linux) or check Device Manager (Windows)
- Update baudrate in `main.py` if needed (default: 115200)

### 3. Web UI Setup

#### Install Dependencies
```bash
cd UI/
pip install fastapi uvicorn jinja2 websockets
```

#### Run Development Server
```bash
python main.py
# Access at: http://localhost:8000
```

### 4. Spike Prime Setup

#### Install PyBricks Firmware
1. Visit [Pybricks Code editor](https://code.pybricks.com/)
2. Connect Spike Prime via USB
3. Install PyBricks firmware following official guide

#### Install Python Dependencies
```bash
cd spikeprime/
pip install bleak
```

#### Upload Robot Code
1. Open `src/prime-code.py` in Pybricks Code editor
2. Click "Run" button to upload to hub
3. Press center button on hub to start program

## Running the System

### Start Order
1. **Pico**: Flash firmware and connect to RPI
2. **RPI**: Run `python main.py` in rpi/ directory
3. **Web UI**: Run `python main.py` in UI/ directory
4. **Spike Prime**: Press center button to start uploaded program

### Verification
- Check RPI console for Pico connection messages
- Open Web UI at `http://localhost:8000`
- Verify sensor data appears in UI
- Test Spike Prime commands from UI

## Troubleshooting

### Pico Issues
- **Build errors**: Verify ARM toolchain installation and PATH
- **Upload issues**: Check USB connection and permissions
- **No serial output**: Verify baudrate and port settings

### RPI Issues
- **Connection failed**: Check USB cable and port permissions
- **No data**: Verify Pico firmware is running
- **Parse errors**: Check message format consistency

### Web UI Issues
- **Server won't start**: Check port 8000 availability
- **No WebSocket data**: Verify RPI connection
- **Simulation errors**: Check turtle graphics dependencies

### Spike Prime Issues
- **BLE connection failed**: Enable Bluetooth and check range
- **No response**: Ensure PyBricks program is running on hub
- **Command errors**: Verify command format and hub status

## Development Tips

- Use VS Code with Python and C++ extensions
- Enable auto-formatting for consistent code style
- Run tests before committing changes
- Monitor serial output for debugging
- Use Web UI simulation for testing without hardware