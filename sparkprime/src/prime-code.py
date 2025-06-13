from pybricks.pupdevices import Motor
from pybricks.hubs import PrimeHub
from pybricks.parameters import Port, Color
from pybricks.tools import wait

# Standard MicroPython modules
from usys import stdin, stdout
from uselect import poll

hub = PrimeHub()
motorA = Motor(Port.A)
motorB = Motor(Port.B)

# Optional: Register stdin for polling. This allows
# you to wait for incoming data without blocking.
keyboard = poll()
keyboard.register(stdin)

encoding = 'utf-8'

while True:

    # Let the remote program know we are ready for a command.
    stdout.buffer.write(b"rdy")


    # Read three bytes.
    cmd = stdin.buffer.read(4)

    if cmd == b'on.A':
        hub.light.on(Color.YELLOW)
        motorA.dc(50)
    elif cmd == b'on.B':
        hub.light.on(Color.YELLOW)
        motorB.dc(50)
    elif cmd == b'offA':
        hub.light.on(Color.GREEN)
        motorA.dc(0)
    elif cmd == b'offB':
        hub.light.on(Color.GREEN)
        motorB.dc(0)
    elif cmd == b'ally':
        hub.light.on(Color.YELLOW)
        motorA.dc(50)
        motorB.dc(50)
    elif cmd == b'alln':
        motorA.dc(0)
        motorB.dc(0)

    else:
        hub.display.text(str(cmd, 'utf-8'))





