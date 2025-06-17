from datasend import HubController
import time
import math

class Prime:
    def __init__(self, hub_name):
        self.hub = HubController(hub_name)

    def moveForward(self, distance):
        distance = float(distance)
        if distance < 0:
            print("Move Forward: Can't have a negative number!")
            return
        if distance == 0:
            duration = "0"
        elif distance < 10:
            duration = str(math.ceil((distance / 30.8) * 1000))
        else:
            duration = str(math.ceil(((distance / 30.8 - (distance / 100)) * 1000)))
        self.hub.send(f"moveforward.100.{duration}!")
        time.sleep(int(duration) / 1000)

    def moveBackwards(self, distance):
        distance = float(distance)
        if distance < 0:
            print("Move Backwards: Can't have a negative number!")
            return
        if distance == 0:
            duration = "0"
        elif distance < 10:
            duration = str(math.ceil((distance / 30.8) * 1000))
        else:
            duration = str(math.ceil(((distance / 30.8 - (distance / 100)) * 1000)))
        self.hub.send(f"movebackwards.100.{duration}!")
        time.sleep(int(duration) / 1000)

    def turnLeft(self, turnAngle, factor):
        turnAngle = float(turnAngle)
        factor = float(factor)
        if turnAngle < 0:
            print("Error in turnLeft, might be using negatives!")
            return
        if turnAngle < 180:
            a = turnAngle / 90
            duration = str(int((a * 300) - (a * factor)))
            self.hub.send(f"turnleft.100.{duration}!")
            time.sleep(int(duration) / 1000)
        else:
            print("Just use the turnRight Command!")

    def turnRight(self, turnAngle, factor):
        turnAngle = float(turnAngle)
        factor = float(factor)
        if turnAngle < 0:
            print("Error in turnRight, might be using negatives!")
            return
        if turnAngle <= 180:
            a = turnAngle / 90
            duration = str(int((a * 300) - (a * factor)))
            self.hub.send(f"turnright.100.{duration}!")
            time.sleep(int(duration) / 1000)
        else:
            print("Just use the turnLeft Command!")

    def stop(self, speed, duration):
        speed = str(speed)
        duration = str(duration)
        self.hub.send(f"stop.{speed}.{duration}!")
        time.sleep(2)
    
    def partyTime(self):
        self.hub.send("spinaround.100.0!")
        time.sleep(2)