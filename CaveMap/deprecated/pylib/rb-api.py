# Copyright (c) 2025 Lachlan McKenna (MrTibbz2)

# This source file is part of the CaveBot project, created for educational purposes.
# Unauthorized reuse or reproduction in other robotics competitions (including FLL 2025) 
# without written permission is strictly prohibited.
# Redistribution or adaptation is allowed for personal study only.

import turtle
import math
import time
import threading
import websockets
import json # Added for json.dumps
import asyncio # Added for async operations and event loop
import queue # Added for queue.Empty exception

# Import the RobotSimulator and the global data queue from your simulation.py
from simulation import RobotSimulator, global_sensor_data_queue

# Create a single instance of the RobotSimulator.
robot_simulator_instance = RobotSimulator()

# Global flag to control the WebSocket sender loop
websocket_sender_running = False

async def websocket_sender_task(ws_url: str):
    """
    Asynchronously connects to the WebSocket server and sends data
    from the robot_simulator_instance's queue.
    """
    global websocket_sender_running
    websocket_sender_running = True
    print(f"WebSocket sender task: Attempting to connect to {ws_url}...")
    try:
        async with websockets.connect(ws_url) as ws:
            print("WebSocket sender task: Connected.")
            # Inform the simulator that a WebSocket sender is active
            robot_simulator_instance.add_ws_sender() # Call without argument
            
            while websocket_sender_running:
                try:
                    # Get data from the queue (non-blocking, with a timeout)
                    data = robot_simulator_instance.ws_send_queue.get(timeout=0.1)
                    await ws.send(json.dumps(data)) # Correctly send JSON string
                    print(f"WebSocket sender task: Sent data: {data['payload']}")
                except queue.Empty:
                    # No data in queue, continue loop
                    await asyncio.sleep(0.01) # Small sleep to prevent busy-waiting
                except websockets.exceptions.ConnectionClosedOK:
                    print("WebSocket sender task: Connection closed normally.")
                    break
                except Exception as e:
                    print(f"WebSocket sender task: Error sending data: {e}")
                    break # Exit loop on error
    except Exception as e:
        print(f"WebSocket sender task: Failed to connect or error during connection: {e}")
    finally:
        websocket_sender_running = False
        print("WebSocket sender task: Exited.")

def run_async_websocket_sender_in_thread(ws_url: str):
    """
    Runs the asynchronous WebSocket sender task in a new thread.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(websocket_sender_task(ws_url))
    loop.close()

def start_robot_simulation():
    """
    Prepares the robot simulation for manual control.
    """
    print("API: Robot simulation ready for manual control.")

def stop_robot_simulation():
    """
    Prepares the robot simulation for shutdown.
    """
    global websocket_sender_running
    websocket_sender_running = False # Signal the sender task to stop
    print("API: Robot simulation stopping.")

def get_latest_robot_data():
    """
    Retrieves the latest robot pose and sensor readings from the shared queue.
    """
    try:
        data = global_sensor_data_queue.popleft()
        return data
    except IndexError:
        return None

def run_turtle_mainloop_with_websocket_sender():
    """
    Starts the turtle graphics mainloop and a separate thread for WebSocket sending.
    This function MUST be called from the main thread.
    """
    # Start the WebSocket sender in a separate thread
    # It will connect to the /ws/readings endpoint of the FastAPI server
    ws_sender_thread = threading.Thread(target=run_async_websocket_sender_in_thread,
                                        args=("ws://localhost:8000/ws/readings",),
                                        daemon=True)
    ws_sender_thread.start()

    print("API: Robot simulation started. Ready for manual control.")
    print("API: Starting turtle mainloop in main thread.")
    robot_simulator_instance.screen.mainloop() # This blocks the main thread

# --- Example Usage (for testing rb-api.py directly) ---
if __name__ == "__main__":
    print("--- Testing Robot API (Standalone) ---")
    
    # 1. Set up keyboard bindings for manual control
    robot_simulator_instance.screen.listen()
    robot_simulator_instance.screen.onkey(robot_simulator_instance.move_forward, "Up")
    robot_simulator_instance.screen.onkey(robot_simulator_instance.move_backward, "Down")
    robot_simulator_instance.screen.onkey(robot_simulator_instance.turn_left, "Left")
    robot_simulator_instance.screen.onkey(robot_simulator_instance.turn_right, "Right")
    print("Use arrow keys to control the robot.")
    print("Each movement will trigger a scan and put data into the WebSocket queue.")

    # 2. Simulate a backend polling for data in a separate thread (optional for this manual test)
    def simulate_backend_polling():
        print("\n--- Backend Data Polling Started (check this console for robot data) ---")
        try:
            while True:
                data = get_latest_robot_data()
                if data:
                    pass # Suppress verbose output for now
                time.sleep(0.1)
        except Exception as e:
            print(f"Backend polling stopped due to: {e}")

    polling_thread = threading.Thread(target=simulate_backend_polling, daemon=True)
    polling_thread.start()

    # 3. Crucially, run the turtle graphics mainloop in the main thread
    # This will also start the WebSocket sender thread.
    run_turtle_mainloop_with_websocket_sender()
    
    print("--- API Test Complete (after turtle mainloop exit) ---")
