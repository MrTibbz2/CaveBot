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

# wait for movement to start, but avoid infinite hang
start_wait_deadline = time.time() + 5.0  # 5s timeout
while not prime.isMoving():
    if time.time() > start_wait_deadline:
        print("Timeout waiting for movement to start")
        break
    time.sleep(0.05)

# initialize baseline from payload
try:
    last_distance = float(prime.return_payload())
except (TypeError, ValueError):
    last_distance = 0.0

# monitor while moving
while prime.isMoving():
    payload = prime.return_payload()
    try:
        current = float(payload)
    except (TypeError, ValueError):
        time.sleep(0.05)
        continue
    moved_distance = current - last_distance
    Mapmove(moved_distance)
    last_distance = current
    time.sleep(0.05)

stopscan()

# prime.turnLeft()
# prime.moveForward(60)
# prime.turnRight()
# prime.moveForward(30)

