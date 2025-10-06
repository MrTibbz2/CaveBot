#!/usr/bin/env python3
from primeCommands import Prime

hub_name = input("Enter hub name: ")
prime = Prime(hub_name)

while True:
    cmd = input("> ").strip().split()
    if not cmd or cmd[0] == "quit":
        break
    
    if cmd[0] == "forward" and len(cmd) == 2:
        prime.moveForward(int(cmd[1]))
    elif cmd[0] == "backward" and len(cmd) == 2:
        prime.moveBackwards(int(cmd[1]))
    elif cmd[0] == "stop":
        prime.stop()
    elif cmd[0] == "party":
        prime.partyTime()
    elif cmd[0] == "turnto" and len(cmd) == 2:
        prime.turnTo(int(cmd[1]))
    elif cmd[0] == "left":
        prime.turnLeft()
    elif cmd[0] == "right":
        prime.turnRight()
    else:
        print("Commands: forward <dist>, backward <dist>, stop, party, turnto <angle>, left, right, quit")