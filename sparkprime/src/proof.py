import asyncio
from contextlib import suppress
from pybricksconnect import PybricksHubClient
import tkinter as tk
from threading import Thread

PYBRICKS_COMMAND_EVENT_CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"

hub_name = "NSE_Pybricks"  # Replace with your hub's name

class HubController:
    def __init__(self, hub_name):
        self.hub_name = hub_name
        self.hub = None
        self.loop = asyncio.new_event_loop()
        self.connected = False
        Thread(target=self._start_loop, daemon=True).start()
        self.loop.call_soon_threadsafe(self._connect)

    def _start_loop(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_forever()

    async def _connect_async(self):
        self.hub = PybricksHubClient(self.hub_name)
        self.connected = await self.hub.connect()

    def _connect(self):
        asyncio.run_coroutine_threadsafe(self._connect_async(), self.loop)

    def send(self, msg):
        if self.connected:
            asyncio.run_coroutine_threadsafe(self.hub.send(bytes(msg, "utf-8")), self.loop)
            print("Sent" + msg)
        else:
            print("Not connected to hub!")

def main():
    controller = HubController(hub_name)

    root = tk.Tk()
    root.title("Pybricks Hub Control")

    btn_ally = tk.Button(root, text="Send 'ally'", command=lambda: controller.send("ally."))
    btn_ally.pack(padx=20, pady=10)

    btn_alln = tk.Button(root, text="Send 'alln'", command=lambda: controller.send("alln."))
    btn_alln.pack(padx=20, pady=10)

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