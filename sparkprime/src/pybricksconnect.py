import asyncio
from contextlib import suppress
from bleak import BleakScanner, BleakClient

PYBRICKS_COMMAND_EVENT_CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"

class PybricksHubClient:
    def __init__(self, hub_name):
        self.hub_name = hub_name
        self.client = None
        self.ready_event = asyncio.Event()
        self.main_task = None

    def handle_disconnect(self, _):
        print("Hub was disconnected.")
        if self.main_task and not self.main_task.done():
            self.main_task.cancel()

    def handle_rx(self, _, data: bytearray):
        if data[0] == 0x01:  # "write stdout" event (0x01)
            payload = data[1:]
            if payload == b"rdy":
                self.ready_event.set()
            else:
                print("Received:", payload)

    async def connect(self):
        device = await BleakScanner.find_device_by_name(self.hub_name)
        if device is None:
            print(f"could not find hub with name: {self.hub_name}")
            return False

        self.main_task = asyncio.current_task()
        self.client = BleakClient(device, self.handle_disconnect)
        await self.client.__aenter__()
        await self.client.start_notify(PYBRICKS_COMMAND_EVENT_CHAR_UUID, self.handle_rx)
        print("Connected to hub.")
        return True

    async def disconnect(self):
        if self.client:
            await self.client.__aexit__(None, None, None)
            print("Disconnected from hub.")

    async def send(self, data: bytes):
        await self.ready_event.wait()
        self.ready_event.clear()
        await self.client.write_gatt_char(
            PYBRICKS_COMMAND_EVENT_CHAR_UUID,
            b"\x06" + data,
            response=True
        )
        print("sent")