// Canvas setup
const canvas = document.getElementById('map');
const ctx = canvas.getContext('2d');

function setupCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    ctx.fillStyle = 'white';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
}
let state = {
    zoom: 1.0,
    origin: { x: canvas.width / 2, y: canvas.height * 0.75 }, // origin point for starting point
    botLocation: { x: 0, y: 0 },
    botAngle: 0, // angle facing in degrees, 0 is up/forward/starting point
    pointhasBeenjoined: false,
    lastpoint: { x: 0, y: 0 }, // point to join
    currentpoint: { x: 0, y: 0 }, // point to draw
    
}

setupCanvas();
function ResetState() {
    state = {
    zoom: 1.0,
    origin: { x: canvas.width / 2, y: canvas.height * 0.75 }, // origin point for starting point
    botLocation: { x: 0, y: 0 },
    botAngle: 0, // angle facing in degrees, 0 is up/forward/starting point
    pointhasBeenjoined: false,
    lastpoint: { x: 0, y: 0 }, // point to join
    currentpoint: { x: 0, y: 0 }, // point to draw
    
    }
}

const ws = new WebSocket("ws://localhost:8000/ws");
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type == "log") {
        logMessage(data);
    }
    

};
function logMessage(message) {
    const logcontainer = document.getElementById('log-container');
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    logEntry.textContent = `${message.timestamp} - type: ${message.subtype}, message: ${message.payload.message}`;
    logcontainer.appendChild(logEntry);
    // Scroll to bottom to show latest message
    logcontainer.scrollTop = logcontainer.scrollHeight;
}