# Copyright (c) 2025 Archie Bradby
# All rights reserved.

import primeCommands

hub_name = "NSE_Pybricks"

prime = primeCommands.Prime(hub_name)

def maze_main(prime):
    prime.moveForward(60)
    prime.turnRight()
    prime.moveForward(43)
    prime.turnRight()
    prime.moveForward(40)
    prime.turnLeft()
    prime.moveForward(80)
    prime.turnLeft()
    prime.moveForward(40)
    prime.turnLeft()
    prime.moveForward(40)
    prime.turnRight()
    prime.moveForward(40)
    prime.turnLeft()
    prime.moveForward(80)
    prime.turnRight()
    prime.moveForward(40)
    prime.turnRight()
    prime.turnRight()
    prime.moveForward(40)
    prime.turnLeft()
    prime.moveForward(40)
    prime.turnLeft()
    prime.moveForward(40)
    prime.turnRight()
    prime.moveForward(80)
    prime.turnRight()
    prime.moveForward(40)
    prime.turnLeft()
    prime.moveForward(10)

# maze(prime)
def maze1(prime):
    prime.moveForward(24)
    prime.turnLeft()
    prime.moveForward(60)
    prime.turnRight()
    prime.moveForward(30)