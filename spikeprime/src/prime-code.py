from pybricks.pupdevices import Motor
from pybricks.hubs import PrimeHub
from pybricks.parameters import Port, Color
from pybricks.tools import wait

from usys import stdin, stdout
from uselect import poll

hub = PrimeHub()
motorA = Motor(Port.A)
motorB = Motor(Port.B)

keyboard = poll()
keyboard.register(stdin)

encoding = 'utf-8'

while True:
    stdout.buffer.write(b"rdy")

    # Read bytes until newline is received
    cmd = b""
    while not cmd.endswith(b"."):
        byte = stdin.buffer.read(1)
        if not byte:
            continue  # No data, keep waiting
        cmd += byte

    cmd = cmd.strip()  # Remove newline and any extra whitespace

    stdout.buffer.write(bytes(cmd, encoding))

    if cmd == b'allMotorsOn.':
        motorA.dc(50)
        motorB.dc(50)
    elif cmd == b'allMotorsOff.':
        motorA.dc(0)
        motorB.dc(0)
    elif cmd == b'motorAOn.':
        motorA.dc(50)
    elif cmd == b'motorAOff.':
        motorA.dc(0)
    elif cmd == b'motorBOn.':
        motorB.dc(50)
    elif cmd == b'motorBOff.':
        motorB.dc(0)
    else:
        try:
            hub.display.text(str(cmd, 'utf-8'))
        except Exception:
            hub.display.text("BAD")