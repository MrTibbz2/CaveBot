import serial
import serial.tools.list_ports
import json
import threading
import time

class PicoSerialInterface:
    """
    A Python library to interface with the Pico microcontroller over serial.
    Abstracts serial communication, handles sending commands and receiving logs.
    """
    def __init__(self, port=None, baudrate=115200, timeout=1):
        """
        Initializes the serial interface.

        Args:
            port (str, optional): The serial port name (e.g., 'COM3' on Windows, '/dev/ttyACM0' on Linux).
                                  If None, the library will attempt to auto-detect the port.
            baudrate (int): The baud rate for the serial connection.
            timeout (int): Read timeout in seconds.
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_connection = None
        self._read_thread = None
        self._stop_event = threading.Event()
        self._log_buffer = [] # Buffer to store received log messages
        self.Core1Stream = []
        self.INFOStream = []
        self.CMDStream = []
        self.ERRStream = []
        self._lock = threading.Lock() # Lock for accessing the log buffer

    def find_pico_port(self):
        """
        Automatically searches for the Pico serial port by iterating through
        available ports and sending a test command (GETSTATE).

        Returns:
            str or None: The name of the detected Pico port, or None if not found.
        """
        print("Searching for Pico serial port...")
        ports = serial.tools.list_ports.comports()
        if not ports:
            print("No serial ports found.")
            return None

        test_command = "CMD_STATUS"
        test_timeout = 2 # seconds to wait for a response

        for port_info in ports:
            port_name = port_info.device
            print(f"Testing port: {port_name}")
            temp_serial = None
            try:
                # Attempt to connect
                temp_serial = serial.Serial(port_name, self.baudrate, timeout=self.timeout)
                # Give the Pico time to reset and initialize
                time.sleep(2)

                # Clear any initial buffer data
                temp_serial.read_all()
                self._log_buffer = [] # Clear buffer before testing

                # Send test command
                temp_serial.write(f"{test_command}\n".encode('utf-8'))
                print(f"Sent '{test_command}' to {port_name}, waiting for response...")

                # Wait for a response
                start_time = time.time()
                
                while time.time() - start_time < test_timeout:
                    if temp_serial.in_waiting > 0:
                        line = temp_serial.readline().decode('utf-8', errors='ignore').strip()
                        if line:
                            parts = line.split(':', 1)
                            identifier = parts[0].strip()
                            if identifier == "INFO":
                                return port_name
                    time.sleep(0.01) # Small delay
                print(f"No valid response from {port_name} within {test_timeout} seconds.")


            except serial.SerialException:
                pass # Ignore ports that can't be opened
            finally:
                if temp_serial and temp_serial.isOpen():
                    temp_serial.close()

        print("Pico port not found.")
        return None


    def connect(self):
        """Establishes the serial connection."""
        if self.port is None:
            self.port = self.find_pico_port()
            if self.port is None:
                print("Cannot connect: Pico port not specified and auto-detection failed.")
                return False

        try:
            self.serial_connection = serial.Serial(
                self.port,
                self.baudrate,
                timeout=self.timeout
            )
            # Give the Pico time to reset and initialize after connection
            time.sleep(2)
            print(f"Connected to {self.port}")

            # Start the background thread to read serial data
            self._stop_event.clear()
            
            return True
        except serial.SerialException as e:
            print(f"Error connecting to {self.port}: {e}")
            self.serial_connection = None
            return False

    def disconnect(self):
        """Closes the serial connection."""
        if self.serial_connection and self.serial_connection.isOpen():
            self._stop_event.set() # Signal the read thread to stop
            if self._read_thread and self._read_thread.is_alive():
                self._read_thread.join(timeout=1) # Wait for the thread to finish
            self.serial_connection.close()
            print(f"Disconnected from {self.port}")
        self.serial_connection = None

    
    def format_ostream(self):
        """Reads serial data and formats it according to Pico's output: 'IDENTIFIER: <json>'."""
        if not self.serial_connection or not self.serial_connection.isOpen():
            return
        while not self._stop_event.is_set():
            try:
                if self.serial_connection.in_waiting > 0:
                    line = self.serial_connection.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        with self._lock:
                            parts = line.split(':', 1)
                            identifier = parts[0].strip()
                            message = parts[1].strip() if len(parts) > 1 else ''
                            if identifier == "Core1":
                                try:
                                    self.Core1Stream.append(json.loads(message))
                                except Exception:
                                    pass
                            elif identifier == "INFO":
                                try:
                                    self.INFOStream.append(json.loads(message))
                                except Exception:
                                    pass
                            elif identifier == "CMD":
                                try:
                                    self.CMDStream.append(json.loads(message))
                                except Exception:
                                    pass
                            elif identifier == "ERR":
                                try:
                                    self.ERRStream.append(json.loads(message))
                                except Exception:
                                    pass
            except serial.SerialException as e:
                print(f"Error reading from serial port: {e}")
                break
            time.sleep(0.01)

    def poll_status(self, timeout=3):
        """
        Polls the Pico for its status and returns the response.

        Args:
            timeout (int): Maximum time to wait for a response in seconds.

        Returns:
            tuple:
                bool: True if the Pico is responding, False if not
                str: status
        """
        if not self.serial_connection or not self.serial_connection.isOpen():
            print("Serial connection is not open.")
            return None, None

        try:
            self.serial_connection.write(b"CMD_STATUS\n")
            start_time = time.time()
            while time.time() - start_time < timeout:
                most_recent_system_status = None
                with self._lock:
                    for item in reversed(self.INFOStream):
                        if isinstance(item, dict) and item.get("type") == "system_status":
                            most_recent_system_status = item
                            break
                if most_recent_system_status and most_recent_system_status.get("status"):
                    print("Pico is responding.")
                    return True, most_recent_system_status.get("status")
                time.sleep(0.1)
            print("No response received within the timeout period, assuming Pico is not responding.")
            return False, None 
        except serial.SerialException as e:
            print(f"Error polling status: {e}")
            return None, None
        except serial.SerialException as e:
            print(f"Error polling status: {e}")
            return None, None

    

    def __del__(self):
        """Ensures the connection is closed when the object is garbage collected."""
        self.disconnect()
