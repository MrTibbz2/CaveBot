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
        self.last_payload = None 

    def handle_disconnect(self, _):
        print("Hub was disconnected.")
        if self.main_task and not self.main_task.done():
            self.main_task.cancel()

    def handle_rx(self, _, data: bytearray):
        try:
            if data[0] == 0x01:  # "write stdout" event (0x01)
                payload = data[1:]
                self.last_payload = str(payload, 'utf-8')
                if payload == b"rdy":
                    self.ready_event.set()
                    return "rdy"
                else:
                    print("Received:", payload)
        except Exception as e:
            print(f"Error in handle_rx: {e}")

    def get_last_payload(self):
        print("Last payload from hub:", self.last_payload)
        return self.last_payload

    async def connect(self):
        try:
            device = await BleakScanner.find_device_by_name(self.hub_name)
            if device is None:
                print(f"Could not find hub with name: {self.hub_name}")
                return False

            self.main_task = asyncio.current_task()
            self.client = BleakClient(device, self.handle_disconnect)
            await self.client.__aenter__()
            await self.client.start_notify(PYBRICKS_COMMAND_EVENT_CHAR_UUID, self.handle_rx)
            print("Connected to hub.")
            return True
        except Exception as e:
            print(f"Error during connection: {e}")
            return False

    async def disconnect(self):
        try:
            if self.client:
                await self.client.__aexit__(None, None, None)
                print("Disconnected from hub.")
        except Exception as e:
            print(f"Error during disconnect: {e}")

    async def send(self, data: bytes):
        try:
            await self.ready_event.wait()
            self.ready_event.clear()
            await self.client.write_gatt_char(
                PYBRICKS_COMMAND_EVENT_CHAR_UUID,
                b"\x06" + data,
                response=True
            )
            print("sent")
        except Exception as e:
            print(f"Error during send: {e}")