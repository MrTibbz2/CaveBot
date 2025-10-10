import webview
import os
import asyncio
import websockets
import json
import threading

WS_ADDRESS = "ws://localhost:8765"

window = None

async def ws_client():
    while True:
        try:
            async with websockets.connect(WS_ADDRESS) as ws:
                print(f"Connected to {WS_ADDRESS}")
                async for message in ws:
                    try:
                        data = json.loads(message)
                        if "plotPoints" in data and isinstance(data["plotPoints"], list):
                            for point in data["plotPoints"]:
                                if "sensor" in point and "distance" in point:
                                    window.evaluate_js(f'DebugPlotPoint("{point["sensor"]}", {point["distance"]})')
                        elif "move" in data and isinstance(data["move"], (int, float)):
                            window.evaluate_js(f'bot.move({data["move"]})')
                        elif "rotate" in data and isinstance(data["rotate"], (int, float)):
                            window.evaluate_js(f'bot.rotate({data["rotate"]})')
                    except (json.JSONDecodeError, KeyError, TypeError) as e:
                        print(f"Invalid message: {e}")
        except (websockets.exceptions.WebSocketException, ConnectionRefusedError) as e:
            print(f"WebSocket error: {e}. Retrying in 5s...")
            await asyncio.sleep(5)
        except Exception as e:
            print(f"Unexpected error: {e}. Retrying in 5s...")
            await asyncio.sleep(5)

def run_ws():
    asyncio.run(ws_client())

html_path = os.path.join(os.path.dirname(__file__), 'index.html')
window = webview.create_window('Desmos Calculator', html_path)
threading.Thread(target=run_ws, daemon=True).start()
webview.start(debug=True)