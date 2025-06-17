import primeCommands

prime = primeCommands.Prime("NSE_Pybricks")

def checkLeftAndRight():
    print("Checking left and right...")

def checkDistance():
    print("Checking distance in front")


while True:
    prime.moveForward(0)
    distance = checkDistance()
    if distance < 3:
        prime.stop(0,0)
        leftSideDistance, rightSideDistance = checkLeftAndRight()
        if leftSideDistance > rightSideDistance:
            prime.turnLeft(90, 10)
        elif leftSideDistance < rightSideDistance:
            prime.turnRight(90, 10)
        else:
            prime.turnRight(180, 10)
    