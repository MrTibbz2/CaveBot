from datasend import HubController
import time
import math

class Prime():

    def __init__(self, hub_name):
        self.hub = HubController(hub_name)

    def moveForward(self, distance):
        if distance == 0:
            self.hub.send("moveforward.100.0!")
            time.sleep(1)
        elif distance > 0 and distance < 10:
            duration = str(math.ceil((distance/30.8) * 1000))
            self.hub.send("moveforward.100." + duration + "!")
            time.sleep(1)
        elif distance >= 10:
            duration = str(math.ceil((distance/30.8) * 1000))
            self.hub.send("moveforward.100." + duration + "!")
            time.sleep(1)
        else:
            print("Move Forward: Can't have a negative number!")
    
    def moveBackwards(self, distance):
        if distance == 0:
            self.hub.send("movebackwards.100.0!")
            time.sleep(1)
        elif distance > 0 and distance < 10:
            duration = str(math.ceil((distance/30.8) * 1000))
            self.hub.send("movebackwards.100." + duration + "!")
            time.sleep(1)
        elif distance >= 10:
            duration = str(math.ceil((distance/30.8) * 1000))
            self.hub.send("movebackwards.100." + duration + "!")
            time.sleep(1)
        else:
            print("Move Backwards: Can't have a negative number!")
    
    def turnLeft(self, turnAngle):
        duration = str(int((turnAngle/90)*300))
        self.hub.send("turnleft.100." + duration + "!")
        time.sleep(2)

    def turnRight(self, turnAngle):
        duration = str(int((turnAngle/90)*300))
        self.hub.send("turnright.100." + duration + "!")
        time.sleep(2)
    
    def stop(self, speed, duration):
        self.hub.send("stop." + speed + "." + duration + "!")
        time.sleep(2)
    
