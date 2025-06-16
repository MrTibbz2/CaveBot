from datasend import HubController

class Prime():

    def __init__(self, hub_name):
        self.hub = HubController(hub_name)

    def moveForward(self, speed, duration):
        self.hub.send("allMotorsOn." + speed + "." + duration + "!")
    
    def moveBackwards(self, speed, duration):
        self.hub.send("allMotorsOn." + "-" + speed + "." + duration + "!")
    
    def turnLeft(self, turnAngle):
        self.hub.send("turnLeft." + turnAngle + "!")

    def turnRight(self, turnAngle):
        self.hub.send("turnRight." + turnAngle + "!")
    
