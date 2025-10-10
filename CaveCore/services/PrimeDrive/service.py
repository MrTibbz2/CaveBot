from ..service import Service
from .primeCommands import Prime

class PrimeDriveService(Service):
    def __init__(self, hub_name="Pybricks Hub"):
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
    
    def move_forward(self, distance):
        if self.prime:
            self.prime.moveForward(distance)
    
    def move_backwards(self, distance):
        if self.prime:
            self.prime.moveBackwards(distance)
    
    def turn_left(self):
        if self.prime:
            self.prime.turnLeft()
    
    def turn_right(self):
        if self.prime:
            self.prime.turnRight()
    
    def turn_to(self, angle):
        if self.prime:
            self.prime.turnTo(angle)
    
    def stop(self):
        if self.prime:
            self.prime.stop()