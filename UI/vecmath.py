import turtle
import math

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