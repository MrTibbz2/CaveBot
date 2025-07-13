from fastapi import FastAPI, WebSocket, Request
from fastapi.websockets import WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio, random
import json
from datetime import datetime
import subprocess
import pylib.vecmath
from ssh_client import SSHClient
# TVisualiser = vecmath.TurtleVisualizer()
import sys
import os
import math
# This will run the command in the background, non-blocking
#process = subprocess.Popen(["C:/Python313/python.exe", "c:/Users/lachl/innovation-team/UI/pylib/rb-api.py"])


frontend_websocket = None # Initialize globally to None
simulation_process = None # Track the simulation process
ssh_client = SSHClient() # SSH client instance

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
    radians = math.radians(angle)
    x_pos = math.sin(radians) * distance
    y_pos = math.cos(radians) * distance
    return {"x_pos": round(x_pos, 4), "y_pos": round(y_pos, 4)}

@app.get("/{path:path}")
def catch_all(request: Request, path: str):
    return templates.TemplateResponse("index.html", {"request": request})
    """
    Calculate the (x, y) offset from the origin after turning by 'angle' degrees and moving 'distance' units.
    Example: /pointcalc?angle=90&distance=100
    """
    radians = math.radians(angle)
    x_pos = math.sin(radians) * distance
    y_pos = math.cos(radians) * distance
    return {"x_pos": round(x_pos, 4), "y_pos": round(y_pos, 4)}

# @app.get("/ui")
# def ui(request: Request):
#     return templates.TemplateResponse("ui.html", {"request": request})
@app.websocket("/ws/cli")
async def cli_ws(ws: WebSocket):
    await ws.accept()
    ssh_client.set_websocket(ws)
    print("CLI WebSocket connection established")
    
    try:
        while True:
            data = await ws.receive_text()
            message = json.loads(data)
            print(f"Received message: {message}")
            
            if message.get("type") == "ssh_connect":
                payload = message.get("payload", {})
                print(f"SSH connect request: {payload}")
                success = await ssh_client.connect(
                    host=payload.get("host"),
                    username=payload.get("username"),
                    password=payload.get("password"),
                    port=payload.get("port", 22)
                )
                status = "connected" if success else "failed"
                print(f"SSH connection result: {status}")
                await ws.send_text(json.dumps({
                    "type": "ssh_status",
                    "payload": {"status": status}
                }))
                
            elif message.get("type") == "cli_command":
                command = message.get("payload", {}).get("command", "")
                print(f"CLI command received: {command}")
                await ssh_client.send_command(command)
                
            elif message.get("type") == "cli_interrupt":
                print("CLI interrupt received")
                await ssh_client.send_interrupt()
                
            elif message.get("type") == "ssh_disconnect":
                print("SSH disconnect requested")
                await ssh_client.disconnect()
                await ws.send_text(json.dumps({
                    "type": "ssh_status",
                    "payload": {"status": "disconnected"}
                }))
                
    except Exception as e:
        print(f"CLI WebSocket error: {e}")
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"CLI WebSocket error: {e}")
    finally:
        print("Disconnecting SSH client")
        await ssh_client.disconnect()

@app.websocket("/ws")
async def map_ws(ws: WebSocket):
    global frontend_websocket, simulation_process
    
    # Kill existing simulation process if it exists
    if simulation_process and simulation_process.poll() is None:
        simulation_process.terminate()
        simulation_process = None
    
    frontend_websocket = ws # Set the global variable
    await ws.accept()
    simulation_process = subprocess.Popen(
        [sys.executable, os.path.join(os.path.dirname(__file__), "pylib/rb-api.py")]
    )
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


