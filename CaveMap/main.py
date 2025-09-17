# Copyright (c) 2025 Lachlan McKenna (MrTibbz2)

# This source file is part of the CaveBot project, created for educational purposes.
# Unauthorized reuse or reproduction in other robotics competitions (including FLL 2025) 
# without written permission is strictly prohibited.
# Redistribution or adaptation is allowed for personal study only.

from fastapi import FastAPI, WebSocket, Request, HTTPException
from fastapi.websockets import WebSocketDisconnect
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio, random
import json
from datetime import datetime
import subprocess
import pylib.vecmath
from database import CaveMapDatabase
from models import MapState
# DEPRECATED: SSH client functionality disabled
# from ssh_client import SSHClient
# TVisualiser = vecmath.TurtleVisualizer()
import sys
import os
import math
# This will run the command in the background, non-blocking
#process = subprocess.Popen(["C:/Python313/python.exe", "c:/Users/lachl/innovation-team/UI/pylib/rb-api.py"])


frontend_websocket = None # Initialize globally to None
simulation_process = None # Track the simulation process
# ssh_client = SSHClient() # DEPRECATED: SSH client instance
db = CaveMapDatabase() # Database instance

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

# API Endpoints for state management
@app.get("/api/state")
def get_current_state():
    """Get current bot state and map data"""
    return db.get_current_state()

@app.get("/api/states")
def list_states():
    """List all saved states"""
    return db.list_states()

@app.post("/api/states")
async def save_state(request: Request):
    """Save current state"""
    body = await request.json()
    name = body.get("name", f"State {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    description = body.get("description", "")
    state_id = db.save_state(name, description)
    return {"id": state_id, "message": "State saved successfully"}

@app.get("/api/states/{state_id}")
def get_state(state_id: str):
    """Get specific state"""
    state = db.load_state(state_id)
    if not state:
        raise HTTPException(status_code=404, detail="State not found")
    return state.dict()

@app.delete("/api/states/{state_id}")
def delete_state(state_id: str):
    """Delete specific state"""
    if db.delete_state(state_id):
        return {"message": "State deleted successfully"}
    raise HTTPException(status_code=404, detail="State not found")

@app.post("/api/bot/position")
async def update_bot_position(request: Request):
    """Update bot position"""
    body = await request.json()
    x = body.get("x", 0)
    y = body.get("y", 0)
    angle = body.get("angle", 0)
    db.update_bot_position(x, y, angle)
    return {"message": "Bot position updated"}

@app.post("/api/map/point")
async def add_map_point(request: Request):
    """Add map point"""
    body = await request.json()
    x = body.get("x")
    y = body.get("y")
    sensor = body.get("sensor")
    if x is not None and y is not None and sensor:
        db.add_map_point(x, y, sensor)
        return {"message": "Map point added"}
    raise HTTPException(status_code=400, detail="Missing required fields")

@app.get("/{path:path}")
def catch_all(request: Request, path: str):
    return templates.TemplateResponse("index.html", {"request": request})


# DEPRECATED: CLI WebSocket endpoint - functionality disabled
# @app.websocket("/ws/cli")
# async def cli_ws(ws: WebSocket):
#     await ws.accept()
#     ssh_client.set_websocket(ws)
#     print("CLI WebSocket connection established")
#     
#     try:
#         while True:
#             data = await ws.receive_text()
#             message = json.loads(data)
#             print(f"Received message: {message}")
#             
#             if message.get("type") == "ssh_connect":
#                 payload = message.get("payload", {})
#                 print(f"SSH connect request: {payload}")
#                 success = await ssh_client.connect(
#                     host=payload.get("host"),
#                     username=payload.get("username"),
#                     password=payload.get("password"),
#                     port=payload.get("port", 22)
#                 )
#                 status = "connected" if success else "failed"
#                 print(f"SSH connection result: {status}")
#                 await ws.send_text(json.dumps({
#                     "type": "ssh_status",
#                     "payload": {"status": status}
#                 }))
#                 
#             elif message.get("type") == "cli_command":
#                 command = message.get("payload", {}).get("command", "")
#                 print(f"CLI command received: {command}")
#                 await ssh_client.send_command(command)
#                 
#             elif message.get("type") == "cli_interrupt":
#                 print("CLI interrupt received")
#                 await ssh_client.send_interrupt()
#                 
#             elif message.get("type") == "ssh_disconnect":
#                 print("SSH disconnect requested")
#                 await ssh_client.disconnect()
#                 await ws.send_text(json.dumps({
#                     "type": "ssh_status",
#                     "payload": {"status": "disconnected"}
#                 }))
#                 
#     except Exception as e:
#         print(f"CLI WebSocket error: {e}")
#     except WebSocketDisconnect:
#         print("WebSocket disconnected")
#     except Exception as e:
#         print(f"CLI WebSocket error: {e}")
#     finally:
#         print("Disconnecting SSH client")
#         await ssh_client.disconnect()

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
            message = await ws.receive_text()
            # Handle frontend messages for state management
            try:
                data = json.loads(message)
                if data.get("type") == "save_state":
                    payload = data.get("payload", {})
                    state_id = db.save_state(payload.get("name", "Unnamed State"), payload.get("description", ""))
                    await ws.send_text(json.dumps({
                        "type": "state_saved",
                        "payload": {"id": state_id}
                    }))
            except json.JSONDecodeError:
                pass  # Ignore non-JSON messages
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
        
        # Store data in database
        if data.get("type") == "sensor_readings":
            for sensor_name, distance in data.get("payload", {}).items():
                if distance != float('inf') and distance is not None:
                    db.add_sensor_reading(sensor_name, distance)
        elif data.get("type") == "bot":
            # Bot movement data will be handled by frontend API calls
            pass
        
        if frontend_websocket: # Only send if frontend is connected
            await frontend_websocket.send_json(data)
        else:
            print("Frontend WebSocket not connected. Skipping sensor data forward.")


