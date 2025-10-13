# Copyright (c) 2025 Archie Bradby
# All rights reserved.

import primeCommands

hub_name = "NSE_Pybricks"

prime = primeCommands.Prime(hub_name)

prime.moveForward(24)
prime.turnRight()
prime.moveForward(60)
prime.turnLeft()
prime.moveForward(30)

# what needs to be done:

# - change it so that it IS a blocking call. prime.moveforwared(24) should only return when the move is complete
# - do this by making the prime hub send a message back when it is done
