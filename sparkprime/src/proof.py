import asyncio
from contextlib import suppress
from bleak import BleakScanner, BleakClient
from sparkprime.src.pybricksconnect import PybricksHubClient

PYBRICKS_COMMAND_EVENT_CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"

# Example usage:
async def main():
    hub = PybricksHubClient()
    if await hub.connect():
        print("Start the program on the hub now with the button.")
        await hub.send(b"hey!!")
        print("done.")
        await hub.disconnect()

if __name__ == "__main__":
    with suppress(asyncio.CancelledError):
        asyncio.run(main())