# Copyright (c) 2025 Archie Bradby
# All rights reserved.

from .datasend import HubController
import time

class Prime:
    def __init__(self, hub_name):
        self.hub = HubController(hub_name)

    def moveForward(self, distance):
        self.hub.send(f"moveforward.35.{distance}!")
        time.sleep(0.5)

    def moveBackwards(self, distance):
        self.hub.send(f"movebackwards.35.{distance}!")
        time.sleep(4)

    def stop(self):
        self.hub.send(f"stop.0.0!")
        time.sleep(4)
    
    def partyTime(self):
        self.hub.send("spinaround.100.0!")
        time.sleep(4)
    
    def turnTo(self, target_angle):
        self.hub.send(f"turnto.100.{target_angle}!")
        time.sleep(4)
    
    def turnLeft(self):
        self.hub.send(f"turnRight.50.90!")
        time.sleep(4)

    def turnRight(self):
        self.hub.send(f"turnLeft.50.90!")
        time.sleep(4)

    def return_payload(self):
        return self.hub.return_payload()
    
    def isMoving(self):
        return self.hub.hub.is_moving()
        