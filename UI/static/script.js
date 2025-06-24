// Canvas setup
const canvas = document.getElementById('map');
const ctx = canvas.getContext('2d');
import * as Map from './map.js';






const ws = new WebSocket("ws://localhost:8000/ws");
ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type == "log") {
        logMessage(data);
    }
    if (data.type == "data_stream") {
        proccessMapData(data);
    }
    

};
ws.onopen = function() {
    console.log("WebSocket connection established.");
};
ws.onclose = function() {
    console.log("WebSocket connection closed.");
};
function proccessMapData(data) {
    // Process the map data and update the canvas
    if (data.subtype === "distance_read") {
        // draw points on the map based on bot location and angle

    } else if (data.subtype === "botangle") {

    } else if (data.subtype === "botpostion") {
        
    }
        
    
}
function logMessage(message) {
    const logcontainer = document.getElementById('log-container');
    const logEntry = document.createElement('div');
    logEntry.className = 'log-entry';
    logEntry.textContent = `${message.timestamp} - type: ${message.subtype}, message: ${message.payload.message}`;
    logcontainer.appendChild(logEntry);
    // Scroll to bottom to show latest message
    logcontainer.scrollTop = logcontainer.scrollHeight;
}


