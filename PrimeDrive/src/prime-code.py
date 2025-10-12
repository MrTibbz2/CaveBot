# Copyright (c) 2025 Archie Bradby
# All rights reserved.

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

# Global heading offset to simulate gyro zero reset
heading_offset = 0

def get_relative_heading():
    raw = hub.imu.rotation(Axis.Z)
    rel = (raw - heading_offset + 180) % 360 - 180
    return rel

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

def spin_around(speed=50, howLong=1000):
    motorA.dc(speed)
    motorB.dc(-speed)
    colorlist = [Color.RED, Color.ORANGE, Color.YELLOW, Color.GREEN, Color.BLUE, Color.MAGENTA, Color.VIOLET]
    hub.light.animate(colorlist, 500)
    if howLong > 0:
        wait(howLong)
        motorA.dc(0)
        motorB.dc(0)

def move_forward_corrected(speed=10, target_distance_cm=0):

    kp = 2
    stopwatch = StopWatch()
    stopwatch.reset()

    # Constants for distance calc
    wheel_diameter = 0.056  # meters
    wheel_circumference = wheel_diameter * 3.1416  # meters

    # Reset motor angles
    motorA.reset_angle(0)
    motorB.reset_angle(0)

    while True:
        # Calculate traveled distance
        avg_deg = (abs(motorA.angle()) + abs(motorB.angle())) / 2
        distance_m = (avg_deg / 360) * wheel_circumference
        distance_cm = distance_m * 100

        # Break if target distance reached (if given)
        if target_distance_cm > 0 and distance_cm >= target_distance_cm:
            break

        # Heading correction
        current_angle = get_relative_heading()
        error = current_angle
        correction = kp * error

        left_speed = max(min(speed + correction, 100), -100)
        right_speed = max(min(speed - correction, 100), -100)

        motorA.dc(left_speed)
        motorB.dc(-right_speed)
        print(f"Moving Forward: distance={distance_cm:.1f}cm")

        wait(50)  # Increased wait time for stability

    # Stop motors at end
    motorA.dc(0)
    motorB.dc(0)
    print(f"Reached target distance: {distance_cm:.1f} cm")


def move_backwards_corrected(speed=50, target_distance_cm=0):

    kp = 0.5
    stopwatch = StopWatch()
    stopwatch.reset()

    # Constants for distance calc
    wheel_diameter = 0.056  # meters
    wheel_circumference = wheel_diameter * 3.1416  # meters

    # Reset motor angles
    motorA.reset_angle(0)
    motorB.reset_angle(0)

    while True:
        # Calculate traveled distance
        avg_deg = (abs(motorA.angle()) + abs(motorB.angle())) / 2
        distance_m = (avg_deg / 360) * wheel_circumference
        distance_cm = distance_m * 100

        # Break if target distance reached (if given)
        if target_distance_cm > 0 and distance_cm >= target_distance_cm:
            break

        # Heading correction
        current_angle = get_relative_heading()
        error = current_angle
        correction = kp * error

        left_speed = max(min(-speed - correction, 100), -100)
        right_speed = max(min(-speed + correction, 100), -100)

        motorA.dc(left_speed)
        motorB.dc(-right_speed)
        print(f"Moving Backwards: distance={distance_cm:.1f}cm")

        wait(20)

    # Stop motors at end
    motorA.dc(0)
    motorB.dc(0)
    print(f"Reached target distance: {distance_cm:.1f} cm")


def angle_error(target, current):
    return (target - current + 180) % 360 - 180

def turn_to_angle(target_angle=90, max_speed=100):
    global heading_offset

    # Turn accuracy parameters, make sure its not too accurate or it will oscillate
    kp = 5
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

        motorA.dc(-speed)
        motorB.dc(-speed)
        print(f"Turning: current={current_angle}")

        wait(20)

    motorA.dc(0)
    motorB.dc(0)
    print(f"Reached target angle: {current_angle:.1f} degrees")

    heading_offset = hub.imu.rotation(Axis.Z)
    wait(50)

def turn_to_command(speed=100, target_angle=90):
    turn_to_angle(target_angle, max_speed=speed)

def turn_left_gyro(speed=100, angle=90):
    global heading_offset
    current_heading = hub.imu.rotation(Axis.Z)
    target = (current_heading + angle) % 360
    turn_to_angle(target, max_speed=speed)
    heading_offset = hub.imu.rotation(Axis.Z)
    print(f"heading_offset: {current_heading}")
    wait(50)

def turn_right_gyro(speed=100, angle=90):
    global heading_offset
    current_heading = hub.imu.rotation(Axis.Z)
    target = (current_heading - angle) % 360
    turn_to_angle(target, max_speed=speed)
    heading_offset = hub.imu.rotation(Axis.Z)
    print(f"heading_offset: {current_heading}")
    wait(50)

command_map = {
    'moveforward': move_forward_corrected,
    'movebackwards': move_backwards_corrected,
    'stop': all_motors_off,
    'spinaround': spin_around,
    'turnto': turn_to_command,
    'turnleft': turn_left_gyro,
    'turnright': turn_right_gyro,
}

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
