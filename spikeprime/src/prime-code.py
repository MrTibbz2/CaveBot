from pybricks.pupdevices import Motor
from pybricks.hubs import PrimeHub
from pybricks.parameters import Port, Color, Axis
from pybricks.tools import wait, StopWatch

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

def move_forward(speed=50, howLong=0):
    motorA.dc(-speed)
    motorB.dc(speed)
    if howLong > 0:
        wait(howLong)
        motorA.dc(0)
        motorB.dc(0)

def move_backwards(speed=50, howLong=0):
    motorA.dc(speed)
    motorB.dc(-speed)
    if howLong > 0:
        wait(howLong)
        motorA.dc(0)
        motorB.dc(0)

def turn_left(speed=50, howLong=0):
    motorA.dc(speed)
    motorB.dc(speed)
    if howLong > 0:
        wait(howLong)
        motorA.dc(0)
        motorB.dc(0)

def turn_right(speed=50, howLong=0):
    motorA.dc(-speed)
    motorB.dc(-speed)
    if howLong > 0:
        wait(howLong)
        motorA.dc(0)
        motorB.dc(0)

def spin_around(speed=50, howLong=1000):
    motorA.dc(-speed)
    motorB.dc(-speed)
    colorlist = [Color.RED, Color.ORANGE, Color.YELLOW, Color.GREEN, Color.BLUE, Color.MAGENTA, Color.VIOLET]
    hub.light.animate(colorlist, 500)
    if howLong > 0:
        wait(howLong)
        motorA.dc(0)
        motorB.dc(0)

# --- NEW: gyro-based corrected movement ---

def move_forward_corrected(speed=50, howLong=0):
    initial_angle = 0
    kp = 2
    stopwatch = StopWatch()
    stopwatch.reset()
    while howLong == 0 or stopwatch.time() < howLong:
        current_angle = hub.imu.rotation(Axis.Z)
        error = current_angle - initial_angle
        correction = kp * error

        left_speed = max(min(-speed - correction, 100), -100)
        right_speed = max(min(speed - correction, 100), -100)

        motorA.dc(left_speed)
        motorB.dc(right_speed)

        wait(20)

    motorA.dc(0)
    motorB.dc(0)

def move_backwards_corrected(speed=50, howLong=0):
    stopwatch = StopWatch()
    stopwatch.reset()
    initial_angle = 0
    kp = 2

    while howLong == 0 or stopwatch.time() < howLong:
        current_angle = hub.imu.rotation(Axis.Z)
        error = current_angle - initial_angle
        correction = kp * error

        left_speed = max(min(speed - correction, 100), -100)
        right_speed = max(min(-speed - correction, 100), -100)

        motorA.dc(left_speed)
        motorB.dc(right_speed)

        wait(20)

    motorA.dc(0)
    motorB.dc(0)

def angle_error(target, current):
    # Wrap error to [-180, 180]
    return (target - current + 180) % 360 - 180

def turn_to_angle(target_angle=90, max_speed=100):
    kp = 1.5
    min_speed = 20

    while True:
        current_angle = hub.imu.rotation(Axis.Z)
        error = angle_error(target_angle, current_angle)

        if abs(error) < 1.5:
            break

        speed = kp * error

        if speed > 0:
            speed = min(speed, max_speed)
            if speed < min_speed:
                speed = min_speed
        else:
            speed = max(speed, -max_speed)
            if speed > -min_speed:
                speed = -min_speed

        motorA.dc(speed)
        motorB.dc(speed)

        wait(20)

    motorA.dc(0)
    motorB.dc(0)

    # Reset heading after turn completes, then wait briefly for IMU to settle
    hub.imu.reset_heading(0)
    wait(50)

def turn_to_command(speed=100, target_angle=90):
    turn_to_angle(target_angle, max_speed=speed)

def turn_left_gyro(speed=100, angle=90):
    current_heading = hub.imu.rotation(Axis.Z)
    target = (current_heading + angle) % 360
    turn_to_angle(target, max_speed=speed)
    hub.imu.reset_heading(0)
    wait(50)

def turn_right_gyro(speed=100, angle=90):
    current_heading = hub.imu.rotation(Axis.Z)
    target = (current_heading - angle) % 360
    turn_to_angle(target, max_speed=speed)
    hub.imu.reset_heading(0)
    wait(50)

# --- COMMAND MAP ---
command_map = {
    'moveforward': move_forward_corrected,
    'movebackwards': move_backwards_corrected,
    'stop': all_motors_off,
    'spinaround': spin_around,
    'turnto': turn_to_command,
    'turnleft': turn_left_gyro,
    'turnright': turn_right_gyro,
}

# --- COMMAND LOOP ---
while True:
    stdout.buffer.write(b"rdy")

    cmd = b""
    while not cmd.endswith(b"!"):
        byte = stdin.buffer.read(1)
        if not byte:
            continue
        cmd += byte

    cmd = cmd.strip()

    try:
        cmd_string = str(cmd, encoding)
        command, params = parse_command(cmd_string)
        speed = params[0] if len(params) > 0 else 100
        howLong = params[1] if len(params) > 1 else 0

        if command in command_map:
            command_map[command](speed, howLong)
        else:
            hub.display.text("BAD")
    except Exception as e:
        try:
            hub.display.text(str(e))
        except Exception:
            pass
