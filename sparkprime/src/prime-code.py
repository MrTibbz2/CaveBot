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
    elif cmd == b'ally.':
        hub.light.on(Color.YELLOW)
        motorA.dc(50)
        motorB.dc(50)
    elif cmd == b'alln.':
        motorA.dc(0)
        motorB.dc(0)
    else:
        # Show the received command for debugging
        try:
            hub.display.text(str(cmd, 'utf-8'))
        except Exception:
            hub.display.text("BAD")