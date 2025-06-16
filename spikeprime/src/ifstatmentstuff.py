import primeCommands

prime = primeCommands.Prime("NSE_Pybricks")

time = 3

while True:
    prime.moveForward("50", "0")
    if time == 0:
        prime.stop("0", "0")
        break
    time -= 1
