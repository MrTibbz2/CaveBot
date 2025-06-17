import primeCommands

# Connects to spike prime and does some behinds the scenes stuff
prime = primeCommands.Prime("NSE_Pybricks")

# Goes forward 130 cm
prime.moveForward(130)

# Turns 180 degress (so around itself)
prime.turnRight(180)

# Goes back the way it came
prime.moveForward(130)

prime.partyTime()


