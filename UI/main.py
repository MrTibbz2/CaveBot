from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio, random
import json
from datetime import datetime
import subprocess
import vecmath
TVisualiser = vecmath.TurtleVisualizer()
# This will run the command in the background, non-blocking
#process = subprocess.Popen(["C:/Python313/python.exe", "c:/Users/lachl/innovation-team/UI/rb-api.py"])


frontend_websocket = None # Initialize globally to None

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.get("/pointcalc")
def pointcalc(request: Request, angle: float = 0, distance: float = 0):
    """
    Calculate the (x, y) offset from the origin after turning by 'angle' degrees and moving 'distance' units.
    Example: /pointcalc?angle=90&distance=100
    """
    offset = TVisualiser.turn_and_move(angle, distance)
    return {"x_pos": offset[0], "y_pos": offset[1]}
# @app.get("/ui")
# def ui(request: Request):
#     return templates.TemplateResponse("ui.html", {"request": request})
@app.websocket("/ws")
async def map_ws(ws: WebSocket):
    global frontend_websocket
    frontend_websocket = ws # Set the global variable
    await ws.accept()
    process = subprocess.Popen(["C:/Python313/python.exe", "c:/Users/lachl/innovation-team/UI/rb-api.py"])
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
        
        if frontend_websocket: # Only send if frontend is connected
            await frontend_websocket.send_json(data)
        else:
            print("Frontend WebSocket not connected. Skipping sensor data forward.")
         
            
