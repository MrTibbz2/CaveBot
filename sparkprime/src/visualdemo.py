import asyncio
from contextlib import suppress
from pybricksconnect import PybricksHubClient
import tkinter as tk
from threading import Thread
from datasend import HubController

PYBRICKS_COMMAND_EVENT_CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"

hub_name = "NSE_Pybricks"  # Replace with your hub's name

def main():
    controller = HubController(hub_name)

    root = tk.Tk()
    root.title("Pybricks Hub Control")

    btn_allMotorsOn = tk.Button(root, text="Turn on All Motors", command=lambda: controller.send("allMotorsOn."))
    btn_allMotorsOn.pack(padx=20, pady=10)

    btn_allMotorsOff = tk.Button(root, text="Turn off All Motors", command=lambda: controller.send("allMotorsOff."))
    btn_allMotorsOff.pack(padx=20, pady=10)

    btn_motorAOn = tk.Button(root, text="Turn On Motor A", command=lambda: controller.send("motorAOn."))
    btn_motorAOn.pack(padx=20, pady=10)

    btn_motorAOff = tk.Button(root, text="Turn Off Motor A", command=lambda: controller.send("motorAOff."))
    btn_motorAOff.pack(padx=20, pady=10)

    btn_motorBOn = tk.Button(root, text="Turn On Motor B", command=lambda: controller.send("motorBOn."))
    btn_motorBOn.pack(padx=20, pady=10)

    btn_motorBOff = tk.Button(root, text="Turn Off Motor B", command=lambda: controller.send("motorBOff."))
    btn_motorBOff.pack(padx=20, pady=10)

    entry = tk.Entry(root, width=30)
    entry.pack(padx=20, pady=10)

    btn_send_entry = tk.Button(
        root,
        text="Send Entry Text",
        command=lambda: controller.send(entry.get() + ".")
    )
    btn_send_entry.pack(padx=20, pady=10)
    root.mainloop()

if __name__ == "__main__":
    with suppress(asyncio.CancelledError):
        main()