import turtle
import math
import time
import threading
import websockets
# Import the RobotSimulator and the global data queue from your simulation.py
from simulation import RobotSimulator, global_sensor_data_queue
class ws:
    def __init__(self, ):
        self.ws_url = "ws://localhost:8000/ws"
        self.ws = None

    def tryconnect(self):
        """
        Attempts to connect to the WebSocket server.
        This is a placeholder for actual WebSocket connection logic.
        """
        print(f"Connecting to WebSocket at {self.ws_url}...")
        # atttempt a connection to the WebSocket server on the url
        
        # If successful, set self.ws to the connected WebSocket object
        self.ws = websockets.connect(self.ws_url)
        if not self.ws:
            print("Failed to connect to WebSocket server.")
            return False
        self.ws = True
        print("WebSocket connected.")
    
# Create a single instance of the RobotSimulator.
# This instance will manage the turtle graphics window and the robot's state.
# It's important to have only one instance for the entire application.
robot_simulator_instance = RobotSimulator()

def start_robot_simulation():
    """
    Prepares the robot simulation for manual control.
    In manual mode, there's no 'start' method to call for autonomous behavior.
    The RobotSimulator instance is simply ready to receive manual commands.
    The first scan is done upon the first manual movement.
    """
    print("API: Robot simulation ready for manual control.")

def stop_robot_simulation():
    """
    Prepares the robot simulation for shutdown.
    In manual mode, this would typically mean stopping any background processing
    or preparing for graceful exit.
    """
    print("API: Robot simulation stopping.")

def get_latest_robot_data():
    """
    Retrieves the latest robot pose and sensor readings from the shared queue.
    If the queue is empty, returns None.

    Returns:
        dict or None: A dictionary containing 'timestamp', 'robot_pose',
                      and 'sensor_readings', or None if no data is available.
    """
    try:
        # Attempt to get data from the left end of the queue (oldest data first)
        data = global_sensor_data_queue.popleft()
        return data
    except IndexError:
        # The queue is empty, so no new data is available yet
        return None

def run_turtle_mainloop(ws):
    """
    Starts the turtle graphics mainloop. This function MUST be called
    from the main thread of your application. It will block until
    the turtle window is closed.
    """
    robot_simulator_instance.add_ws(ws)  # Add the WebSocket to the simulator instance
    print("API: Robot simulation started. Ready for manual control.")
    print("API: Starting turtle mainloop in main thread.")
    robot_simulator_instance.screen.mainloop()

# --- Example Usage (for testing rb-api.py directly) ---
if __name__ == "__main__":
    print("--- Testing Robot API (Standalone) ---")
    backend = ws()
    backend.tryconnect()
    if not backend.ws:
        print("Failed to connect to WebSocket server. Exiting test.")
        exit(1)
    else: 
        print("WebSocket connection established successfully.")
    
    # 1. Set up keyboard bindings for manual control
    robot_simulator_instance.screen.listen()
    robot_simulator_instance.screen.onkey(robot_simulator_instance.move_forward, "Up")
    robot_simulator_instance.screen.onkey(robot_simulator_instance.move_backward, "Down")
    robot_simulator_instance.screen.onkey(robot_simulator_instance.turn_left, "Left")
    robot_simulator_instance.screen.onkey(robot_simulator_instance.turn_right, "Right")
    print("Use arrow keys to control the robot.")
    print("Each movement will trigger a scan and print detected walls.")

    # 2. Simulate a backend polling for data in a separate thread (optional for this manual test)
    # This thread will read data from the queue as the robot generates it via manual moves.
    def simulate_backend_polling():
        print("\n--- Backend Data Polling Started (check this console for robot data) ---")
        try:
            while True: # Run indefinitely until main program exits
                data = get_latest_robot_data()
                if data:
                    # You would send this 'data' dictionary over a WebSocket to your frontend
                    # print(f"Polling: {data['robot_pose']} - Hits: {[s for s, d in data['sensor_readings'].items() if d != float('inf')]}")
                    pass # Suppress verbose output for now
                time.sleep(0.1) # Simulate polling interval
        except Exception as e:
            print(f"Backend polling stopped due to: {e}")

    # Start the backend polling simulation in a separate thread (daemon=True means it exits with main thread)
    polling_thread = threading.Thread(target=simulate_backend_polling, daemon=True)
    polling_thread.start()

    # 3. Crucially, run the turtle graphics mainloop in the main thread
    # This call will block until the turtle window is manually closed.
    run_turtle_mainloop(backend.ws)
    
    print("--- API Test Complete (after turtle mainloop exit) ---")