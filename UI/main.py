from fastapi import FastAPI, WebSocket, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import asyncio, random
import json
from datetime import datetime
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.websocket("/ws")
async def map_ws(ws: WebSocket):
    global frontend_websocket
    frontend_websocket = ws
    await ws.accept()
    await ws.send_text(json.dumps({
        "type": "log",
        "timestamp": datetime.now().isoformat(),
        "subtype": "info",
        "payload": {
            "message": "WebSocket connection established",
            
        }
    }))
    while True:
        #yeahhhh
        await asyncio.sleep(5)

@app.websocket("/ws/readings")
async def readings_ws(ws: WebSocket):
    await ws.accept()
    await frontend_websocket.send_text(json.dumps({
        "type": "log",
        "timestamp": datetime.now().isoformat(),
        "subtype": "info",
        "payload": {
            "message": "WebSocket connection established for sensor readings",
        }
    }))
    while True:
        print("yeahhh")
        