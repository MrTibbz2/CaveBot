# Copyright (c) 2025 Lachlan McKenna (MrTibbz2)

# This source file is part of the CaveBot project, created for educational purposes.
# Unauthorized reuse or reproduction in other robotics competitions (including FLL 2025) 
# without written permission is strictly prohibited.
# Redistribution or adaptation is allowed for personal study only.

import turtle
import math


def get_point_calc(angle, distance):
    # angle in degrees, 0 = right (X+), 90 = up (Y+)
    radians = math.radians(angle)
    x_pos = math.sin(radians) * distance
    y_pos = math.cos(radians) * distance
    return {"x_pos": round(x_pos, 4), "y_pos": round(y_pos, 4)}
class TurtleVisualizer:
    def __init__(self):
        self.t = turtle.Turtle()
        self.t.speed(0)  # Fastest speed
        self.t.penup()
        self.t.goto(0, 0)
        self.t.pendown()
        self.t.setheading(90)  # Facing up (north)
        self.origin = (0, 0)

    def turn_and_move(self, angle, distance):
        """
        Turns the turtle by 'angle' degrees (left), moves forward by 'distance',
        and returns the (x, y) offset from the origin.
        0 degrees is up (north), 90 is east (right).
        """
        self.t.right(angle)
        self.t.forward(distance)
        x, y = self.t.position()
        offset_x = round(x - self.origin[0], 8)
        offset_y = round(y - self.origin[1], 8)
        self.reset()  # Reset the turtle position to origin after moving
        return (offset_x, offset_y)

    def reset(self):
        self.t.reset()
        self.t.penup()
        self.t.goto(0, 0)
        self.t.pendown()
        self.t.setheading(90)  # Facing up (north)
        self.origin = (0, 0)

# Example usage:
# visualizer = TurtleVisualizer()
# offset = visualizer.turn_and_move(45, 100)
# print("Offset from origin:", offset)
# turtle.done()