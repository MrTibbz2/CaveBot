from datasend import HubController

class Prime():

    def __init__(self):
        self.hub = HubController()

    def moveForward(self, speed, duration):
        self.hub.send("allMotorsOn." + speed + "." + duration + "!")
    
    def moveBackwards(self, speed, duration):
        self.hub.send("allMotorsOn." + "-" + speed + "." + duration + "!")
    
    def turnLeft(self, turnAngle):
        self.hub.send("turnLeft." + turnAngle + "!")
    
