// Canvas setup
const canvas = document.getElementById('map');
const ctx = canvas.getContext('2d');
import * as Map from '../map.js';






// Animation loop
function animate() {
    Map.updateMap();
    requestAnimationFrame(animate);
}
animate();


const ws = new WebSocket("ws://localhost:8000/ws");
ws.onmessage = function(event) {
    let safeData = event.data.replace(/:Infinity/g, ':null');
    const data = JSON.parse(safeData);
    if (data.type == "log") {
        logMessage(data);
    }
    if (data.type === "sensor_readings") {
        Map.addpoints(data);
        console.log(Map.points);
    } else if (data.type === "bot") {
        if (data.subtype === "move") {
            let angleRadians = Map.state.botAngle * Math.PI / 180;
            let distance = data.payload.distance;
            Map.state.botLocation.x += distance * Math.sin(angleRadians);
            Map.state.botLocation.y -= distance * Math.cos(angleRadians);
            console.log(Map.state.botLocation);
        } else if (data.subtype === "rotate") {
            Map.state.botAngle += data.payload.degrees;
            if (Map.state.botAngle >= 360) {
                Map.state.botAngle -= 360;
            }
            if (Map.state.botAngle <= 0) {
                Map.state.botAngle += 360;
            }
            console.log(Map.state.botAngle);
        }
    }
};
ws.onopen = function() {
    console.log("WebSocket connection established.");
};
ws.onclose = function() {
    console.log("WebSocket connection closed.");
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


