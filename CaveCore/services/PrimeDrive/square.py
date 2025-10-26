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

# wait for movement to start
start_wait_deadline = time.time() + 5.0
while not prime.isMoving():
    if time.time() > start_wait_deadline:
        print("Timeout waiting for movement to start")
        break
    time.sleep(0.05)

last_distance = 0.0
total_distance = 0.0

while prime.isMoving():
    payload = prime.return_payload()
    try:
        current = float(payload)
    except (TypeError, ValueError):
        time.sleep(0.1)
        continue
    
    moved_distance = current - last_distance
    if moved_distance > 0:
        Mapmove(moved_distance)
        total_distance += moved_distance
        print(f"Total distance moved: {total_distance}")
    
    last_distance = current
    time.sleep(0.1)

stopscan()

# prime.turnLeft()
# prime.moveForward(60)
# prime.turnRight()
# prime.moveForward(30)

