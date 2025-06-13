import asyncio
from contextlib import suppress
from pybricksconnect import PybricksHubClient

PYBRICKS_COMMAND_EVENT_CHAR_UUID = "c5f50002-8280-46da-89f4-6d8051e4aeef"

hub_name = "NSE_Pybricks"  # Replace with your hub's name

# Example usage:
async def main():
    hub = PybricksHubClient(hub_name)
    if await hub.connect():
        while True:
            thing = input("What motor: ")
            await hub.send(bytes(thing, "utf-8"))
            print("done.")

if __name__ == "__main__":
    with suppress(asyncio.CancelledError):
        asyncio.run(main())