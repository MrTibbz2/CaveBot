import asyncio
import websockets
import json

class CaveMapClient:
    def __init__(self, host="localhost", port=8765):
        self.host = host
        self.port = port
        self.ws = None
        self.clients = set()
    
    async def connect(self):
        self.ws = await websockets.serve(self._handler, self.host, self.port)
        print(f"Server started on ws://{self.host}:{self.port}")
        await asyncio.Future()
    
    async def _handler(self, websocket):
        self.clients.add(websocket)
        print(f"Client connected: {websocket.remote_address}")
        try:
            await websocket.wait_closed()
        finally:
            self.clients.discard(websocket)
            print(f"Client disconnected: {websocket.remote_address}")
    
    async def send(self, data):
        if not self.clients:
            print("No clients connected")
            return
        disconnected = set()
        for client in self.clients:
            try:
                await client.send(json.dumps(data))
            except websockets.exceptions.WebSocketException:
                disconnected.add(client)
        self.clients -= disconnected
    
    async def plot_points(self, points):
        if not isinstance(points, list):
            raise ValueError("points must be a list")
        for p in points:
            if "sensor" not in p or "distance" not in p:
                raise ValueError("Each point must have 'sensor' and 'distance'")
        await self.send({"plotPoints": points})
    
    async def move(self, distance):
        if not isinstance(distance, (int, float)):
            raise ValueError("distance must be a number")
        await self.send({"move": distance})
    
    async def rotate(self, degrees):
        if not isinstance(degrees, (int, float)):
            raise ValueError("degrees must be a number")
        await self.send({"rotate": degrees})
