from datasend import HubController
import time
import sys

hub_name = "NSE_Pybricks"

controller = HubController(hub_name)

# Make sure you add a full stop Eg: "Hello World."
cmd = "hi."

# Wait until connected
while not controller.connected:
    time.sleep(0.1)

print("Connected to hub.")

# Wait for 'rdy' from the hub program
while True:
    last = controller.hub.get_last_payload()
    if last and "rdy" in last:
        print("Hub program is ready.")
        break
    time.sleep(0.1)

# Send the string "hi" as bytes
controller.send(cmd)
print("Sent " + cmd + " to hub.")
time.sleep(2)