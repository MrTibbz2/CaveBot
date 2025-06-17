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

def parse_command(cmd_string):
    if cmd_string.endswith('!'):
        cmd_string = cmd_string[:-1]
    parts = cmd_string.split('.')
    command = parts[0].lower()
    params = []
    for p in parts[1:]:
        try:
            params.append(int(p))
        except Exception:
            pass
    return command, params

def all_motors_off(speed=0, howLong=0):
    motorA.dc(0)
    motorB.dc(0)

def move_forward(speed=100, howLong=0):
    motorA.dc(-speed)
    motorB.dc(speed)
    if howLong > 0:
        wait(howLong)
        motorA.dc(0)
        motorB.dc(0)

def move_backwards(speed=100, howLong=0):
    motorA.dc(speed)
    motorB.dc(-speed)
    if howLong > 0:
        wait(howLong)
        motorA.dc(0)
        motorB.dc(0)

def turn_left(speed=100, howLong=0):
    motorA.dc(speed)
    motorB.dc(speed)
    if howLong > 0:
        wait(howLong)
        motorA.dc(0)
        motorB.dc(0)

def turn_right(speed=100, howLong=0):
    motorA.dc(-speed)
    motorB.dc(-speed)
    if howLong > 0:
        wait(howLong)
        motorA.dc(0)
        motorB.dc(0)

def spin_around(speed=100, howLong=1000):
    motorA.dc(-speed)
    motorB.dc(-speed)
    colorlist = [Color.RED, Color.ORANGE, Color.YELLOW, Color.GREEN, Color.BLUE, Color.MAGENTA, Color.VIOLET]
    hub.light.animate(colorlist, 500)
    if howLong > 0:
        wait(howLong)
        motorA.dc(0)
        motorB.dc(0)

command_map = {
    'moveforward': move_forward,
    'movebackwards': move_backwards,
    'stop': all_motors_off,
    'turnleft': turn_left,
    'turnright': turn_right,
    'spinaround': spin_around,
}

while True:
    stdout.buffer.write(b"rdy")

    # Read bytes until '!' is received
    cmd = b""
    while not cmd.endswith(b"!"):
        byte = stdin.buffer.read(1)
        if not byte:
            continue  # No data, keep waiting
        cmd += byte

    cmd = cmd.strip()  # Remove whitespace

    try:
        cmd_string = str(cmd, encoding)
        command, params = parse_command(cmd_string)
        # Provide default values if not enough params
        speed = params[0] if len(params) > 0 else 100
        howLong = params[1] if len(params) > 1 else 0

        if command in command_map:
            command_map[command](speed, howLong)
        else:
            hub.display.text("BAD")
    except Exception as e:
        try:
            hub.display.text("ERR")
        except Exception:
            pass