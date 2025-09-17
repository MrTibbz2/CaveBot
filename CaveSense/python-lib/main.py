import time
from src.pico_serial_interface import PicoSerialInterface
import threading 

BAUDRATE = 115200

sr = PicoSerialInterface(baudrate=BAUDRATE)
time.sleep(2)


result = sr.connect()
if not result:
    print("Failed to connect to Pico. Exiting.")
    exit(2)

# Start the read thread correctly (do not call the function, just pass the function object)
read_thread = threading.Thread(target=sr.format_ostream)
read_thread.daemon = True
read_thread.start()

print("Pico connected and read thread started.")

while True:
    input("press enter to poll device")
    device_stat_bool, status = sr.poll_status()
    if device_stat_bool:
        print(f"Device status: {status}")
    else:
        print("Failed to get device status.")
