# Spike Prime Remote Control & Mapping Project

## Overview

This project enables remote control of a LEGO SPIKE Prime robot from your computer using Bluetooth Low Energy (BLE) and Python.  
You can send high-level movement commands (move, turn, stop, spin) from your computer, and the robot executes them using robust, sensor-corrected code running on the hub.

---

## Features

- **Wireless control** of SPIKE Prime via BLE (using [bleak](https://github.com/hbldh/bleak))
- **High-level Python API** for robot movement (`Prime` class)
- **Command-line and GUI interfaces** for sending commands
- **Sensor-corrected driving and turning** using the hub’s IMU
- **Easy setup and extensibility**

---

## Setup

### Prerequisites

- Python 3.8 or newer (recommended: 3.10+)
- [pip](https://pip.pypa.io/en/stable/installation/)
- LEGO SPIKE Prime hub with [Pybricks firmware](https://pybricks.com/learn/getting-started/install-pybricks/) installed
- BLE support on your computer

### Installation

1. **Clone this repository** and open a terminal in the project directory.
2. **Install required Python packages:**
   ```sh
   pip install bleak
   ```
   > `bleak` is the BLE backend used for communication.

3. **(Optional) For GUI:**  
   If you want to use the Tkinter GUI and get an error, install it via your system package manager:
   - macOS: `brew install python-tk`
   - Ubuntu/Debian: `sudo apt-get install python3-tk`

---

## Uploading and Running the Hub Program

1. **Connect your SPIKE Prime hub to your computer via USB.**
2. **Open [Pybricks Code](https://code.pybricks.com/)** in your browser.
3. **Open and upload `src/prime-code.py` to the hub.**
4. **Press the center button on the hub** to start the program.  
   The hub will now wait for commands from your computer.

---

## Running the Computer-Side Code

### Command-Line Demo

1. **Edit and run a demo script, for example:**
   ```python
   from primeCommands import Prime

   prime = Prime("")  # Replace with your hub's name

   prime.moveForward(50)
   prime.turnRight()
   prime.moveForward(50)
   prime.turnLeft()
   prime.partyTime()
   prime.stop()
   ```
2. **Run your script:**
   ```sh
   python3 your_demo.py
   ```

### Command-Line Interactive Control

You can use the provided CLI to send commands interactively:
```sh
python3 prime_commandline.py
```
Supported commands: `forward <cm>`, `backward <cm>`, `left`, `right`, `stop`, `party`, `quit`

---

## How It Works

- The hub runs `prime-code.py`, which listens for commands over BLE, parses them, and controls the motors.
- Your computer connects to the hub using BLE (via `bleak` and `pybricksconnect`), and sends commands using the `Prime` class.
- The `HubController` manages the BLE connection and ensures the hub is ready before sending commands.
- Commands are sent as strings (e.g., `moveforward.50.1000!`), parsed and executed by the hub.

---

## Troubleshooting

- **Hub not responding?**  
  Make sure you pressed the center button to start the program on the hub.
- **BLE errors?**  
  Ensure Bluetooth is enabled and your hub is in range.
- **ModuleNotFoundError?**  
  Double-check your `pip install` commands.
- **IMU/gyro not working?**  
  Make sure the hub is flat and running Pybricks firmware. Wait for `hub.imu.ready()` before using heading.

---