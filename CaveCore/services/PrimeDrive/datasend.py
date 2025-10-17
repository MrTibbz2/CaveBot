# Copyright (c) 2025 Archie Bradby
# All rights reserved.

import asyncio
from contextlib import suppress
from .pybricksconnect import PybricksHubClient
from threading import Thread
import time

class HubController:
    def __init__(self, hub_name):
        self.hub_name = hub_name
        self.hub = None
        self.loop = asyncio.new_event_loop()
        self.connected = False
        try:
            Thread(target=self._start_loop, daemon=True).start()
            self.loop.call_soon_threadsafe(self._connect)
            self.wait_until_ready(timeout=10)
        except Exception as e:
            print(f"Error starting event loop thread: {e}")

    def _start_loop(self):
        try:
            asyncio.set_event_loop(self.loop)
            self.loop.run_forever()
        except Exception as e:
            print(f"Error in event loop: {e}")

    async def _connect_async(self):
        try:
            self.hub = PybricksHubClient(self.hub_name)
            self.connected = await self.hub.connect()
        except Exception as e:
            print(f"Error in async connect: {e}")
            self.connected = False

    def _connect(self):
        try:
            asyncio.run_coroutine_threadsafe(self._connect_async(), self.loop)
        except Exception as e:
            print(f"Error in _connect: {e}")

    def send(self, msg):
        try:
            if not isinstance(msg, str):
                raise ValueError("Message must be a string.")
            if not msg.endswith("!"):
                print(msg + "\n")
                print("Command didn't have a full stop at the end. Make sure you add one!")
                return
            if self.connected:
                asyncio.run_coroutine_threadsafe(self.hub.send(bytes(msg, "utf-8")), self.loop)
                print("Sent " + msg)
            else:
                print("Not connected to hub!")
        except Exception as e:
            print(f"Error in send: {e}")
    
    def wait_until_ready(self, timeout=5, poll_interval=0.1):
        start = time.time()
        while not self.connected:
            if time.time() - start > timeout:
                print(f"Hub connection timeout after {timeout}s")
                return
            time.sleep(poll_interval)
        print("Connected to hub.")

        start = time.time()
        while True:
            if time.time() - start > timeout:
                print(f"Hub ready timeout after {timeout}s")
                return
            last = self.hub.get_last_payload()
            if last and "rdy" in last:
                print("Hub program is ready.")
                break
            time.sleep(poll_interval)