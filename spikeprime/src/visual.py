import tkinter as tk
import primeCommands

def main():
    hub_name = "NSE_Pybricks"  # Change to your hub's name
    prime = primeCommands.Prime(hub_name)

    root = tk.Tk()
    root.title("Spike Prime Visual Demo")

    # Speed and duration entries
    tk.Label(root, text="Speed:").pack()
    speed_entry = tk.Entry(root)
    speed_entry.pack()
    speed_entry.insert(0, "100")

    tk.Label(root, text="Duration (ms):").pack()
    duration_entry = tk.Entry(root)
    duration_entry.pack()
    duration_entry.insert(0, "1000")

    tk.Label(root, text="Turn Angle (deg):").pack()
    angle_entry = tk.Entry(root)
    angle_entry.pack()
    angle_entry.insert(0, "90")

    # Buttons
    tk.Button(root, text="Move Forward", command=lambda: prime.moveForward(speed_entry.get(), duration_entry.get())).pack(pady=5)
    tk.Button(root, text="Move Backwards", command=lambda: prime.moveBackwards(speed_entry.get(), duration_entry.get())).pack(pady=5)
    tk.Button(root, text="Turn Left", command=lambda: prime.turnLeft(angle_entry.get())).pack(pady=5)
    tk.Button(root, text="Turn Right", command=lambda: prime.turnRight(angle_entry.get())).pack(pady=5)
    tk.Button(root, text="Stop", command=lambda: prime.stop(speed_entry.get(), duration_entry.get())).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()