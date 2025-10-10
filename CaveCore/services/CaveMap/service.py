from ..service import Service
from .client import CaveMapClient
import asyncio
import threading

class CaveMapService(Service):
    def __init__(self, host="localhost", port=8765):
        super().__init__("CaveMapService")
        self.client = CaveMapClient(host, port)
        self.loop = None
        self.thread = None

    def init(self):
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._run_server, daemon=True)
        self.thread.start()
        print("CaveMapService started.")

    def _run_server(self):
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.client.connect())

    def kill(self):
        if self.loop:
            self.loop.call_soon_threadsafe(self.loop.stop)
        print("CaveMapService stopped.")

    def plot_points(self, points):
        if self.loop:
            asyncio.run_coroutine_threadsafe(self.client.plot_points(points), self.loop)

    def move(self, distance):
        if self.loop:
            asyncio.run_coroutine_threadsafe(self.client.move(distance), self.loop)

    def rotate(self, degrees):
        if self.loop:
            asyncio.run_coroutine_threadsafe(self.client.rotate(degrees), self.loop)
