// Canvas setup
// const canvas = document.getElementById('map');
// const ctx = canvas.getContext('2d');

import * as Maplib from './lib/mapperlib.js';
import * as Graph from './lib/map.js';




function beans() {
    let beans = 1;
    beans++;
    console.log("Beans: " + beans);
    return beans;

}
// Animation loop
function animate() {
    Maplib.updateMap();
    requestAnimationFrame(animate);
}

// animate();

const ws = new WebSocket("ws://localhost:8000/ws");
ws.onmessage = function(event) {
    let safeData = event.data.replace(/:Infinity/g, ':null');
    const data = JSON.parse(safeData);
    if (data.type == "log") {
        logMessage(data);
    }
    if (data.type === "sensor_readings") {
        Maplib.addpoints(data);
        
    } else if (data.type === "bot") {
        if (data.subtype === "move") {
            Graph.bot.move(data.payload.distance);
            
        } else if (data.subtype === "rotate") {
            Graph.bot.rotate(data.payload.degrees);
            console.log(Graph.bot.angle);
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


