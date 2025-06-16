from datasend import HubController
import time

hub_name = "NSE_Pybricks"

controller = HubController(hub_name)

# Make sure you add a ! Eg: "Hello World!" to show the end of the bytes
cmd = "allMotorsOn.100.5000!"

controller.wait_until_ready()

# Send the string "hi" as bytes
controller.send(cmd)
print("Sent " + cmd + " to hub.")
time.sleep(2)