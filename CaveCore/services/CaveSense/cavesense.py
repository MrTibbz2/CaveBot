import serial
import serial.tools.list_ports
import json
import threading
from typing import Optional, Callable, Dict
from time import sleep


class CaveSense:
    def __init__(self, port: Optional[str] = None, baudrate: int = 115200):
        self.port = port or self._find_pico()
        self.ser = serial.Serial(self.port, baudrate, timeout=1)
        self.sensor_data: Dict[str, float] = {}
        self.status: str = "UNKNOWN"
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._callback: Optional[Callable] = None

    def _find_pico(self) -> str:
        for port in serial.tools.list_ports.comports():
            if 'ACM' in port.device or 'USB' in port.device:
                try:
                    ser = serial.Serial(port.device, 115200, timeout=0.5)
                    ser.write(b"GETSTATUS\n")
                    sleep(1)
                    line = ser.readline().decode().strip()
                    ser.close()
                    if line.startswith("{") and "status" in line:
                        return port.device
                except:
                    pass
        raise RuntimeError("Pico not found")

    def _read_loop(self):
        while self._running:
            try:
                line = self.ser.readline().decode().strip()
                if not line:
                    continue
                if line.startswith("{"):
                    data = json.loads(line)
                    if "sensor_data" in data:
                        self.sensor_data = data["sensor_data"]
                        if self._callback:
                            self._callback(self.sensor_data)
                    elif "status" in data:
                        self.status = data["status"]
            except:
                pass

    def start(self, callback: Optional[Callable] = None):
        self._callback = callback
        self._running = True
        self._thread = threading.Thread(target=self._read_loop, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join()

    def begin_scan(self):
        self.ser.write(b"BEGINSCAN\n")

    def end_scan(self):
        self.ser.write(b"ENDSCAN\n")

    def get_status(self):
        self.ser.write(b"GETSTATUS\n")

    def close(self):
        self.stop()
        self.ser.close()
