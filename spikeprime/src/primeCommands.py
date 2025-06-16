from datasend import HubController
import time

class Prime():

    def __init__(self, hub_name):
        self.hub = HubController(hub_name)

    def moveForward(self, speed, duration):
        speed = str(speed)
        duration = str(duration)
        self.hub.send("moveforward." + speed + "." + duration + "!")
        time.sleep(2)
    
    def moveBackwards(self, speed, duration):
        speed = str(speed)
        duration = str(duration)
        self.hub.send("movebackwards." + speed + "." + duration + "!")
        time.sleep(2)
    
    def turnLeft(self, turnAngle):
        duration = str((turnAngle/90)*300)
        self.hub.send("turnleft.100." + duration + "!")
        time.sleep(2)

    def turnRight(self, turnAngle):
        duration = str((turnAngle/90)*300)
        self.hub.send("turnright.100." + duration + "!")
        time.sleep(2)
    
    def stop(self, speed, duration):
        self.hub.send("stop." + speed + "." + duration + "!")
        time.sleep(2)
    
