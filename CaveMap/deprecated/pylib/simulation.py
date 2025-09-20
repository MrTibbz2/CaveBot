# Copyright (c) 2025 Lachlan McKenna (MrTibbz2)

# This source file is part of the CaveBot project, created for educational purposes.
# Unauthorized reuse or reproduction in other robotics competitions (including FLL 2025) 
# without written permission is strictly prohibited.
# Redistribution or adaptation is allowed for personal study only.

import turtle
import math
import time
from collections import deque
import threading
import websockets
import json
import asyncio
import queue # Add queue import
# --- Global Data Queue for Sensor Readings ---
# This deque will store sensor readings and robot pose.
# It's intended to be exported (e.g., to a web frontend via a websocket) later.
global_sensor_data_queue = deque(maxlen=100) # Max 100 entries to prevent infinite growth


class RobotSimulator:
    def __init__(self, screen_width=800, screen_height=800, sensor_range=100):
        # --- Screen Setup ---
        self.screen = turtle.Screen()
        self.screen.setup(width=screen_width, height=screen_height)
        self.screen.bgcolor("white")
        self.screen.title("Robot Maze Navigation and Sensor Simulation")
        self.screen.tracer(0) # Turn off screen updates for smoother animation
        self.ws_send_queue = queue.Queue() # Queue for outgoing WebSocket messages
        self.ws_connected_flag = False # Flag to indicate if a WebSocket sender is active
        # --- Maze Definition (Static Black Walls) ---
        self.maze_walls = [
            (-300, 300, 300, 300),  # Top outer wall
            (-300, -300, 300, -300), # Bottom outer wall
            (-300, 300, -300, -300), # Left outer wall
            (300, 300, 300, -300),  # Right outer wall
            # Inner maze walls
            (-100, 200, 100, 200),
            (100, 200, 100, 0),
            (100, 0, 200, 0),
            (-200, -100, -50, -100),
            (-50, -100, -50, -200),
            (0, -50, 0, 100),
            (50, -50, 150, -50),
            (150, -50, 150, -150),
            (-150, 50, -50, 50),
            (-150, 50, -150, 150)
        ]

        # --- Drawing Maze Walls ---
        self.maze_pen = turtle.Turtle()
        self.maze_pen.speed(0) # Fastest speed
        self.maze_pen.penup()
        self.maze_pen.hideturtle()
        self.maze_pen.pensize(3)
        self.maze_pen.pencolor("black")
        self._draw_maze()

        # --- Robot Setup ---
        self.robot = turtle.Turtle()
        self.robot.speed(0) # Fastest speed for drawing robot
        self.robot.shape("circle")
        self.robot.color("green")
        self.robot.shapesize(stretch_wid=1.5, stretch_len=1.5) # Robot size
        self.robot.penup()
        self.robot.setheading(90) # Start facing up (North)
        self.robot.goto(0, -250) # Start in a clear spot within the maze

        # Direction indicator (small blue dot on the robot)
        self.direction_indicator = turtle.Turtle()
        self.direction_indicator.speed(0) # Fastest speed
        self.direction_indicator.shape("circle")
        self.direction_indicator.color("blue")
        self.direction_indicator.shapesize(stretch_wid=0.3, stretch_len=0.3)
        self.direction_indicator.penup()
        self._update_robot_display()

        # --- Robot Movement Parameters ---
        self.move_distance = 10  # How many pixels the robot moves per step
        self.turn_angle = 90     # Always 90-degree increments for turns

        # --- Sensor Simulation Pens and Parameters ---
        self.sensor_pen = turtle.Turtle()
        self.sensor_pen.speed(0) # Fastest speed
        self.sensor_pen.penup()
        self.sensor_pen.hideturtle()
        self.sensor_pen.pencolor("red") # Color of sensor rays
        self.sensor_pen.pensize(1)

        self.sensor_dot_pen = turtle.Turtle()
        self.sensor_dot_pen.speed(0) # Fastest speed
        self.sensor_dot_pen.penup()
        self.sensor_dot_pen.hideturtle()
        self.sensor_dot_pen.color("orange") # Color of sensor origin dots

        self.sensor_range = sensor_range # Max distance a sensor can detect

        # User-provided Sensor definitions (DO NOT CHANGE THESE VALUES):
        # (local_x, local_y, ray_direction_offset_from_robot_heading)
        # These values were explicitly confirmed as correct by the user.
        self.sensors_config = {
            "leftfront": (5, 15, 90),
            "leftback": (-5, 15, 90),
            "rightfront": (5, -15, 270),
            "rightback": (-5, -15, 270),
            "frontleft": (15, 5, 0),
            "frontright": (15, -5, 0),
            "backleft": (-15, 5, 180),
            "backright": (-15, -5, 180)
        }
    def add_ws_sender(self):
        """
        Registers that a WebSocket sender is active.
        """
        self.ws_connected_flag = True
        print("WebSocket sender registered for robot simulator.")
    def _draw_maze(self):
        """Draws all maze walls on the screen."""
        for wall in self.maze_walls:
            self.maze_pen.penup()
            self.maze_pen.goto(wall[0], wall[1])
            self.maze_pen.pendown()
            self.maze_pen.goto(wall[2], wall[3])

    def _update_robot_display(self):
        """Updates the robot's position and direction indicator on the screen."""
        self.robot.goto(self.robot.xcor(), self.robot.ycor())
        
        # Position the direction indicator relative to the robot's heading
        angle_rad = math.radians(self.robot.heading())
        indicator_x = self.robot.xcor() + 15 * math.cos(angle_rad)
        indicator_y = self.robot.ycor() + 15 * math.sin(angle_rad)
        self.direction_indicator.goto(indicator_x, indicator_y)
        self.screen.update()

    def _line_segment_intersection(self, p1, p2, p3, p4):
        """
        Finds the intersection point of two line segments (p1,p2) and (p3,p4).
        Returns (x,y) if they intersect, None otherwise.
        """
        s1_x = p2[0] - p1[0]
        s1_y = p2[1] - p1[1]
        s2_x = p4[0] - p3[0]
        s2_y = p4[1] - p3[1]

        denom = (-s2_x * s1_y + s1_x * s2_y)
        if denom == 0:
            return None # Parallel or collinear

        s = (-s1_y * (p1[0] - p3[0]) + s1_x * (p1[1] - p3[1])) / denom
        t = ( s2_x * (p1[1] - p3[1]) - s2_y * (p1[0] - p3[0])) / denom

        if 0 <= s <= 1 and 0 <= t <= 1:
            # Collision detected
            intersection_x = p1[0] + (t * s1_x)
            intersection_y = p1[1] + (t * s1_y)
            return (intersection_x, intersection_y)
        return None # No collision

    def _perform_scan(self):
        """
        Performs a simulated sensor scan, updates the display, and stores
        readings in the global_sensor_data_queue. It also prints hit detections.
        """
        self.sensor_pen.clear()
        self.sensor_dot_pen.clear()
        
        robot_x, robot_y = self.robot.xcor(), self.robot.ycor()
        robot_heading = self.robot.heading()

        current_sensor_readings = {}
        
        print("\n--- Sensor Scan ---")
        for name, (local_x, local_y, ray_dir_offset) in self.sensors_config.items():
            # Rotate local sensor position to global coordinates
            rotated_x = local_x * math.cos(math.radians(robot_heading)) - local_y * math.sin(math.radians(robot_heading))
            rotated_y = local_x * math.sin(math.radians(robot_heading)) + local_y * math.cos(math.radians(robot_heading))

            sensor_origin_x = robot_x + rotated_x
            sensor_origin_y = robot_y + rotated_y
            
            self.sensor_dot_pen.penup()
            self.sensor_dot_pen.goto(sensor_origin_x, sensor_origin_y)
            self.sensor_dot_pen.dot(5, "orange") # Mark sensor origin

            # Calculate ray endpoint
            ray_direction_global = (robot_heading + ray_dir_offset) % 360
            ray_end_x = sensor_origin_x + self.sensor_range * math.cos(math.radians(ray_direction_global))
            ray_end_y = sensor_origin_y + self.sensor_range * math.sin(math.radians(ray_direction_global))

            closest_intersection = None
            min_distance = self.sensor_range

            ray_p1 = (sensor_origin_x, sensor_origin_y)
            ray_p2 = (ray_end_x, ray_end_y)

            # Check intersection with all maze walls
            for wall in self.maze_walls:
                wall_p1 = (wall[0], wall[1])
                wall_p2 = (wall[2], wall[3])

                intersection = self._line_segment_intersection(ray_p1, ray_p2, wall_p1, wall_p2)

                if intersection:
                    dist = math.dist(ray_p1, intersection)
                    if dist < min_distance:
                        min_distance = dist
                        closest_intersection = intersection

            # Draw the ray
            self.sensor_pen.penup()
            self.sensor_pen.goto(sensor_origin_x, sensor_origin_y)
            self.sensor_pen.pendown()
            if closest_intersection:
                self.sensor_pen.goto(closest_intersection[0], closest_intersection[1])
                current_sensor_readings[name] = round(min_distance, 2)
                # Print only if a wall is detected (not inf)
                print(f"  {name}: {min_distance:.2f} pixels detected at {closest_intersection}.")
                
                print(f"  {name}: {min_distance:.2f} pixels detected.")
            else:
                self.sensor_pen.goto(ray_end_x, ray_end_y)
                current_sensor_readings[name] = float('inf') # No wall detected within range

        # Store data in the shared queue
        global_sensor_data_queue.append({
            "timestamp": time.time(),
            "robot_pose": {
                "x": round(robot_x, 2),
                "y": round(robot_y, 2),
                "heading": round(robot_heading, 2)
            },
            "sensor_readings": current_sensor_readings
        })
        self.screen.update() # Update the screen after drawing all sensors
        if self.ws_connected_flag:
            data_to_send = {
                "type": "sensor_readings",
                "timestamp": time.time(),
                "payload": current_sensor_readings
            }
            self.ws_send_queue.put(data_to_send) # Put data into the queue
            print(f"data put into WebSocket queue: {current_sensor_readings}")
        else:
            print("WebSocket sender not registered. Skipping data send.")
    # --- Manual Movement Methods ---
    def move_forward(self):
        """Moves the robot forward and performs a scan."""
        self.robot.forward(self.move_distance)
        self._update_robot_display()
        self.ws_send_queue.put({
            "type": "bot",
            "timestamp": time.time(),
            "subtype": "move",
            "payload": { "distance": self.move_distance }})
        self._perform_scan()

    def move_backward(self):
        """Moves the robot backward and performs a scan."""
        self.robot.backward(self.move_distance)
        self._update_robot_display()
        self.ws_send_queue.put({
            "type": "bot",
            "timestamp": time.time(),
            "subtype": "move",
            "payload": { "distance": -1 * self.move_distance }})
        self._perform_scan()
        

    def turn_left(self):
        """Turns the robot left by 90 degrees and performs a scan."""
        self.robot.left(self.turn_angle)
        self._update_robot_display()
        self.ws_send_queue.put({
            "type": "bot",
            "timestamp": time.time(),
            "subtype": "rotate",
            "payload": { "degrees": -1 * self.turn_angle }})
        self._perform_scan()

    def turn_right(self):
        """Turns the robot right by 90 degrees and performs a scan."""
        self.robot.right(self.turn_angle)
        self._update_robot_display()
        self.ws_send_queue.put({
            "type": "bot",
            "timestamp": time.time(),
            "subtype": "rotate",
            "payload": { "degrees": self.turn_angle }})
        self._perform_scan()
