from datasend import HubController
import time
import math

class Prime:
    def __init__(self, hub_name):
        self.hub = HubController(hub_name)

    def moveForward(self, distance):
        self.hub.send(f"moveforward.50.{distance}!")
        time.sleep(2)

    def moveBackwards(self, distance):
        self.hub.send(f"movebackwards.50.{distance}!")
        time.sleep(2)

    def stop(self):
        self.hub.send(f"stop.0.0!")
        time.sleep(2)
    
    def partyTime(self):
        self.hub.send("spinaround.100.0!")
        time.sleep(2)
    
    def turnTo(self, target_angle):
        self.hub.send(f"turnto.100.{target_angle}!")
        time.sleep(2)
    
    def turnLeft(self):
        self.hub.send(f"turnleft.100.90!")
        time.sleep(2)

    def turnRight(self):
        self.hub.send(f"turnright.100.90!")
        time.sleep(2)