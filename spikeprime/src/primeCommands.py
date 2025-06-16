from datasend import HubController
import time

class Prime():

    def __init__(self, hub_name):
        self.hub = HubController(hub_name)

    def moveForward(self, speed, duration):
        self.hub.send("allMotorsOn." + speed + "." + duration + "!")
        time.sleep(2)
    
    def moveBackwards(self, speed, duration):
        self.hub.send("allMotorsOn." + "-" + speed + "." + duration + "!")
        time.sleep(2)
    
    def turnLeft(self, turnAngle):
        self.hub.send("turnLeft." + turnAngle + "!")
        time.sleep(2)

    def turnRight(self, turnAngle):
        self.hub.send("turnRight." + turnAngle + "!")
        time.sleep(2)
    
