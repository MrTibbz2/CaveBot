from pybricks.pupdevices import Motor
from pybricks.hubs import PrimeHub
from pybricks.parameters import Port, Color
from pybricks.tools import wait

# Standard MicroPython modules
from usys import stdin, stdout
from uselect import poll

hub = PrimeHub()

# Optional: Register stdin for polling. This allows
# you to wait for incoming data without blocking.
keyboard = poll()
keyboard.register(stdin)

encoding = 'utf-8'

while True:

    # Let the remote program know we are ready for a command.
    stdout.buffer.write(b"rdy")

    # Optional: Check available input.
    while not keyboard.poll(0):
        # Optional: Do something here.
        wait(10)

    # Read three bytes.
    cmd = stdin.buffer.read(6)

    if cmd == b'motor1':
        hub.light.on(Color.RED)
    elif cmd == b'motor2':
        hub.light.on(Color.GREEN)
    elif cmd == b'motor3':
        hub.light.on(Color.BLUE)
    elif cmd == b'motor4':
        hub.light.on(Color.YELLOW)
    wait(5000)



