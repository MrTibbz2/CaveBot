from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio, random
import json
from datetime import datetime

frontend_websocket = None # Initialize globally to None

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def map_ws(ws: WebSocket):
    global frontend_websocket
    frontend_websocket = ws # Set the global variable
    await ws.accept()
    await ws.send_text(json.dumps({
        "type": "log",
        "timestamp": datetime.now().isoformat(),
        "subtype": "info",
        "payload": {
            "message": "WebSocket connection established",
            
        }
    }))
    try:
        while True:
            # Keep connection alive, or handle messages from frontend if any
            await ws.receive_text() # Or just asyncio.sleep(5) if no messages expected
    except Exception as e:
        print(f"map_ws connection closed: {e}")
    finally:
        if frontend_websocket == ws: # Only clear if it's still the current connection
            frontend_websocket = None
        print("map_ws connection closed.")

@app.websocket("/ws/readings")
async def readings_ws(ws: WebSocket):
    await ws.accept()
    if frontend_websocket: # Only send if frontend is connected
        await frontend_websocket.send_text(json.dumps({
            "type": "log",
            "timestamp": datetime.now().isoformat(),
            "subtype": "info",
            "payload": {
                "message": "WebSocket connection established for sensor readings",
            }
        }))
    else:
        print("Frontend WebSocket not connected. Cannot send initial message.")

    print("yeahhh")
    while True:
        print("Waiting for data...")
        data = await ws.receive_text()
        print("Received data:", data)
        if not data:
            continue
        data = json.loads(data)
        if data.get("type") == "sensor_readings":
            if frontend_websocket: # Only send if frontend is connected
                await frontend_websocket.send_text(json.dumps(data))
            else:
                print("Frontend WebSocket not connected. Skipping sensor data forward.")
        else: 
            if frontend_websocket: # Only send if frontend is connected
                await frontend_websocket.send_text(json.dumps({
                    "type": "log",
                    "timestamp": datetime.now().isoformat(),
                    "subtype": "error",
                    "payload": {
                        "message": "Invalid data type received"
                    }
                }))
            else:
                print("Frontend WebSocket not connected. Skipping error log.")
