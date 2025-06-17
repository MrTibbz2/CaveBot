from datasend import HubController
import time
import math

class Prime():

    def __init__(self, hub_name):
        self.hub = HubController(hub_name)

    def moveForward(self, distance):
        if distance == 0:
            self.hub.send("moveforward.100.0!")
            time.sleep(int(duration)/1000)
        elif distance > 0 and distance < 10:
            duration = str(math.ceil((distance/30.8) * 1000))
            self.hub.send("moveforward.100." + duration + "!")
            time.sleep(int(duration)/1000)
        elif distance >= 10:
            duration = str(math.ceil(((distance/30.8 - (distance/100)) * 1000)))
            self.hub.send("moveforward.100." + duration + "!")
            time.sleep(int(duration)/1000)
        else:
            print("Move Forward: Can't have a negative number!")
    
    def moveBackwards(self, distance):
        if distance == 0:
            self.hub.send("movebackwards.100.0!")
            time.sleep(int(duration)/1000)
        elif distance > 0 and distance < 10:
            duration = str(math.ceil((distance/30.8) * 1000))
            self.hub.send("movebackwards.100." + duration + "!")
            time.sleep(int(duration)/1000)
        elif distance >= 10:
            duration = str(math.ceil(((distance/30.8 - (distance/100)) * 1000)))
            self.hub.send("movebackwards.100." + duration + "!")
            time.sleep(int(duration)/1000)
        else:
            print("Move Backwards: Can't have a negative number!")
    
    def turnLeft(self, turnAngle):
        if turnAngle < 180:
            a = turnAngle/90
            duration = str(int((a * 300) - (a * 50)))
            self.hub.send("turnleft.100." + duration + "!")
            time.sleep(int(duration)/1000)
        elif turnAngle > 180:
            print("Just use the turnRight Command!")
        else:
            print("Error in turnLeft, might be using negatives!")

    def turnRight(self, turnAngle):
        if turnAngle <= 180:
            a = turnAngle/90
            duration = str(int((a * 300) - (a * 50)))
            self.hub.send("turnright.100." + duration + "!")
            time.sleep(int(duration)/1000)
        elif turnAngle >= 180:
            print("Just use the turnLeft Command!")
        else:
            print("Error in turnRight, might be using negatives!")
    
    def stop(self, speed, duration):
        self.hub.send("stop." + speed + "." + duration + "!")
        time.sleep(2)
    
