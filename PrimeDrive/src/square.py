# Copyright (c) 2025 Archie Bradby
# All rights reserved.

import time
import primeCommands

hub_name = "NSE_Pybricks"

prime = primeCommands.Prime(hub_name)
def startscan():
    print("Starting scan...")

def stopscan():
    print("Stopping scan...")
def Mapmove(yay):
    print(f"Moving forward: {yay}")

startscan()
prime.moveForward(24)
while prime.isMoving() == False:
    time.sleep(0.1)
last_distance = 0.0
while prime.isMoving():
    moved_distance = float(prime.getDistance()) - last_distance
    Mapmove(moved_distance)
    last_distance = float(prime.return_payload())
stopscan()
    

# prime.turnLeft()
# prime.moveForward(60)
# prime.turnRight()
# prime.moveForward(30)

