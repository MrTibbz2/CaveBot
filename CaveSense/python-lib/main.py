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
print("Commands: 's' = status, 'start' = begin scan, 'stop' = end scan, 'd' = show data, 'q' = quit")

while True:
    cmd = input("Enter command: ").strip().lower()
    
    if cmd == 'q':
        break
    elif cmd == 's':
        device_stat_bool, status = sr.poll_status()
        if device_stat_bool:
            print(f"Device status: {status}")
        else:
            print("Failed to get device status.")
    elif cmd == 'start':
        if sr.start_sensor_scan():
            print("Sensor scan started")
        else:
            print("Failed to start sensor scan")
    elif cmd == 'stop':
        if sr.stop_sensor_scan():
            print("Sensor scan stopped")
        else:
            print("Failed to stop sensor scan")
    elif cmd == 'd':
        data = sr.get_latest_sensor_data()
        if data:
            print("Latest sensor readings:")
            for entry in data:
                if entry.get("type") == "data_stream" and "payload" in entry:
                    print(f"  {entry['payload']}")
        else:
            print("No sensor data available")
    else:
        print("Unknown command. Use 's', 'start', 'stop', 'd', or 'q'")

sr.disconnect()
print("Disconnected.")
