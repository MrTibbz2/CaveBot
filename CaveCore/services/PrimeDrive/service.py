# Copyright (c) 2025 Archie Bradby
# All rights reserved.

import time
from ..service import Service
from .primeCommands import Prime

class PrimeDriveService(Service):
    def __init__(self, hub_name="NSE_Pybricks"):
        super().__init__("PrimeDriveService")
        self.hub_name = hub_name
        self.prime = None

    def init(self):
        self.prime = Prime(self.hub_name)
        print("PrimeDriveService started.")

    def kill(self):
        if self.prime:
            self.prime.stop()
        print("PrimeDriveService stopped.")

    def moveForward(self, distance):
        if self.prime:
            self.prime.moveForward(distance)

    def moveBackwards(self, distance):
        if self.prime:
            self.prime.moveBackwards(distance)

    def stop(self):
        if self.prime:
            self.prime.stop()

    def partyTime(self):
        if self.prime:
            self.prime.partyTime()

    def turnTo(self, target_angle):
        if self.prime:
            self.prime.turnTo(target_angle)

    def turnLeft(self):
        if self.prime:
            self.prime.turnLeft()

    def turnRight(self):
        if self.prime:
            self.prime.turnRight()

    def scan_and_move(self, distance, move_callback, start_scan, stop_scan):
        if not self.prime:
            return
        
        start_scan()
        self.prime.moveForward(distance)
        
        start_wait_deadline = time.time() + 5.0
        while not self.prime.isMoving():
            if time.time() > start_wait_deadline:
                print("Timeout waiting for movement to start")
                break
            time.sleep(0.05)
        
        last_distance = 0.0
        total_distance = 0.0
        
        while self.prime.isMoving():
            payload = self.prime.return_payload()
            try:
                current = float(payload)
            except (TypeError, ValueError):
                time.sleep(0.1)
                continue
            
            moved_distance = current - last_distance
            if moved_distance > 0:
                move_callback(moved_distance)
                total_distance += moved_distance
                print(f"Total distance moved: {total_distance}")
            
            last_distance = current
            time.sleep(0.1)
        
        stop_scan()

    
