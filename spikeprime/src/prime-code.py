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
    # Remove the trailing '!' if present
    if cmd_string.endswith('!'):
        cmd_string = cmd_string[:-1]
    # Split by '.'
    parts = cmd_string.split('.')
    # The first part is the command, the rest are parameters
    command = parts[0]
    params = []
    for p in parts[1:]:
        if p.isdigit():
            params.append(int(p))
    return command, params

def all_motors_off(speed, howLong):
    motorA.dc(0)
    motorB.dc(0)

def move_forward(speed, howLong):
    motorA.dc(-speed)
    motorB.dc(speed)
    if howLong >= 1:
        wait(howLong)
        motorA.dc(0)
        motorB.dc(0)

def move_backwards(speed, howLong):
    motorA.dc(speed)
    motorB.dc(-speed)
    if howLong >= 1:
        wait(howLong)
        motorA.dc(0)
        motorB.dc(0)

def turnLeft(speed, howLong):
    motorA.dc(speed)
    motorB.dc(speed)
    if howLong >= 1:
        wait(howLong)
        motorA.dc(0)
        motorB.dc(0)

def turnRight(speed, howLong):
    motorA.dc(-speed)
    motorB.dc(-speed)
    if howLong >= 1:
        wait(howLong)
        motorA.dc(0)
        motorB.dc(0)

command_map = {
    'moveforward': move_forward,
    'movebackwards': move_backwards,
    'motorsoff': all_motors_off,
    'turnleft': turnLeft,
    'turnright': turnRight,
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
        speed = params[0] if len(params) > 0 else 0
        howLong = params[1] if len(params) > 1 else 0

        if command in command_map:
            command_map[command](speed, howLong)
        else:
            hub.display.text(command)
    except Exception as e:
        try:
            hub.display.text("BAD")
        except Exception:
            pass