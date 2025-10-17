# Copyright (c) 2025 Archie Bradby
# All rights reserved.

from ..service import Service
from .primeCommands import Prime

class PrimeDriveService(Service):
    def __init__(self, hub_name="NSE_Pybricks"):
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

    def moveForward(self, distance):
        if self.prime:
            self.prime.moveForward(distance)

    def moveBackwards(self, distance):
        if self.prime:
            self.prime.moveBackwards(distance)

    def stop(self):
        if self.prime:
            self.prime.stop()

    def partyTime(self):
        if self.prime:
            self.prime.partyTime()

    def turnTo(self, target_angle):
        if self.prime:
            self.prime.turnTo(target_angle)

    def turnLeft(self):
        if self.prime:
            self.prime.turnLeft()

    def turnRight(self):
        if self.prime:
            self.prime.turnRight()
