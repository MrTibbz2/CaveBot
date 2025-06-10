what ive done so far: 
- install cmake https://cmake.org/download/
 - install ninja with choclatey: choco install ninja (you can install with brew or apt or whatever)
- might need to add cmake to PATH depending on install
- get arm-gnu-toolchain-14.2.rel1-mingw-YOUR_SYSTEM-arm-none-eabi.exe from arm developer: https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads
- will need to add to path
- install cmake tools extension
- cmake: Configure


# RPi Pico System Communication Protocol

This document outlines the communication protocol for the RPi Pico system, so that we can structure correctly.

---

### 1. Pico Output Format (Structured for Python Parsing)

All messages from the RPi Pico to the Python Controller adhere to a JSON-like string format for easy parsing into Python dictionaries.

**Format:** `<IDENTIFIER>: { "type": "<MESSAGE_TYPE>", "status": "<STATUS_CODE>", "payload": {<DATA_OR_MESSAGES>} }`

* **`<IDENTIFIER>`**: `Core1`, `Command`, `INFO`, `ERROR` (indicates message origin/category).
* **`"type"`**: Categorizes the specific message (e.g., `data_stream`, `thread_status`, `system_status`).
* **`"status"`**: Concise code indicating outcome or state (e.g., `INFO`, `success`, `thread_started`, `thread_locked`).
* **`"payload"`**: (Optional) Contains detailed data or a verbose message, often another structured object (e.g., a list of sensor readings).

---

### 2. Python Controller Input Commands

These are simple string commands sent from the Python Controller to the Pico.

* **`CMD_START_<COMMAND_NAME>`**
    * **Purpose:** Initiate a specific task on Core1 (e.g., `CMD_START_SENSORREAD`).
    * **Pico Response (Example):**
        * `Core1: { "type": "command_response", "status": "thread_started", "payload": { <data> }` (Success)
        * `ERROR: { "type": "core1_management", "status": "thread_locked"}` (Failure)

* **`CMD_STOP`**
    * **Purpose:** Terminate the currently running Core1 thread.
    * **Pico Response (Example):**
        * `Core1: { "type": "command_response", "status": "thread_stopped" }` (Success)
        * `ERROR: { "type": "core1_management", "status": "no_thread_running", "message": "No thread to stop." }` (Failure)

* **`CMD_STATUS`**
    * **Purpose:** Request current system or device status (blocking Core0 operation, as it does not use core1).
    * **Pico Response (Example):**
        * `INFO: { "type": "system_status", "status": "ready", "uptime_seconds": 3600 }`
        * `INFO: { "type": "core1_status", "status": "active", "command": "SENSOR_READ" }`



---

### 3. RPi Pico Output Messages (Examples)

Messages from the Pico examples.

#### a. Core1 Thread Outputs (Data & Status)

* **Sensor Data Stream:**
    * **Example:** `Core1: { "type": "data_stream", "status": "active", "payload": [ {"sensor_id": "front_left", "average": 150.2}, {"sensor_id": "rear_right", "average": 199.7} ] }`
    * **Description:** Transmits structured sensor data (e.g., averages for multiple sensors).

* **Thread Lifecycle Status:**
    * **Example:** `Core1: { "type": "thread_status", "event": "active", "command": "DISTANCE_MEASURE" }`
    * **Example:** `Core1: { "type": "thread_status", "event": "idle" }`

#### b. Command Execution Outputs

* **Command Success:**
    * **Example:** `Command: { "type": "execution_result", "command": "INIT", "status": "success", "message": "System initialized." }`
* **Command Failure:**
    * **Example:** `Command: { "type": "execution_result", "command": "SENSOR_CALIBRATE", "status": "failure", "error_code": "CAL_TIMEOUT", "message": "Calibration timed out." }`
* **Direct Command Output (from blocking Core0 command):**
    * **Example:** `Command: { "type": "output", "command": "GET_FIRMWARE_VER", "payload": "v1.2.3-beta" }`

#### c. Command Monitor Logs

* **General Logging:**
    * **Example:** `Command: { "type": "log", "level": "INFO", "source": "Core0_Monitor", "message": "Received CMD_START_SENSOR_READ." }`

#### d. Device Information / System Status

* **System Health:**
    * **Example:** `INFO: { "type": "system_status", "status": "ready", "details": {"firmware_version": "1.0.1"} }`
* **Device Specific Status:**
    * **Example:** `INFO: { "type": "device_status", "device": "sensor_module", "status": "online", "health": "GOOD" }`

#### e. Error Outputs

* **General Error:**
    * **Example:** `ERROR: { "type": "core1_management", "code": "THREAD_LOCKED", "message": "Core1 busy, cannot start new thread." }`
    * **Example:** `ERROR: { "type": "command_execution", "code": "SENSOR_INIT_FAIL", "message": "Failed to initialize sensor 'S3'." }`