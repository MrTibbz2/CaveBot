# Spike Prime Python Project Setup

## Prerequisites

- Python 3.8 or newer (recommended: 3.10+)
- [pip](https://pip.pypa.io/en/stable/installation/) (Python package manager)
- A computer with Bluetooth Low Energy (BLE) support (for wireless connection)
- LEGO SPIKE Prime hub with [Pybricks firmware](https://pybricks.com/firmware/) installed

## Installation

Open a terminal in the project directory and run:

```sh
pip install bleak
pip install pybricksconnect
```

> **Note:**  
> `pybricksconnect` is a Python package for connecting to Pybricks hubs over BLE.  
> `bleak` is the BLE backend used by `pybricksconnect`.

## Additional Notes

- `tkinter` is used for the GUI. It is included with most Python installations.  
  If you get an error about `tkinter`, install it via your system package manager:
  - **macOS (with Homebrew):** `brew install python-tk`
  - **Ubuntu/Debian:** `sudo apt-get install python3-tk`
- You do **not** need to install the `pybricks` package on your computer unless you are developing for the hub directly.  
  The hub runs Pybricks code natively.

## Running the Project

1. **Upload your Python script to the SPIKE Prime hub** and start it by pressing the center button.
2. **Run your desired Python script** (e.g., `visualdemo.py` or `sendhi.py`) on your computer:
   ```sh
   python3 src/visualdemo.py
   ```
3. **Interact with the GUI or script** to send commands to the hub.

## Troubleshooting

- Make sure your hub is running the Pybricks firmware and your script is started before connecting.
- If you see BLE errors, ensure Bluetooth is enabled and your hub is in range.
- If you get `ModuleNotFoundError`, double-check your `pip install` commands above.

---