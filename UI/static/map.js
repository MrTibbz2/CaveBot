

const canvas = document.getElementById('map');
const ctx = canvas.getContext('2d');

export let points = []
export const botMeasurements = {
    heightcm: 20, // height of the bot in cm
    widthcm: 20,  // width of the bot in cm
    sensors: {
        leftfront:  { x: -10, y: 5,  angle: 270 },
        leftback:   { x: -10, y: -5,  angle: 270 },
        rightfront: { x: 10,  y: 5,  angle: 90 },
        rightback:  { x: 10, y: -5,  angle: 90 },
        frontleft:  { x: -5, y: 10, angle: 0 },
        frontright: { x:  5, y: 10, angle: 0 },
        backleft:   { x: -5, y: -10, angle: 180 },
        backright:  { x:  5, y: -10, angle: 180 }
    }
};
export let state = {
    zoom: 1.0,
    scale: 0.5, //    scaling for visual display
    origin: { x: canvas.width / 2, y: canvas.height * 0.75 },
    botLocation: { x: 0, y: 0 },
    botAngle: 0,
    pointhasBeenjoined: false,
    lastpoint: { x: 0, y: 0 },
    currentpoint: { x: 0, y: 0 },
}
function ResetState() {
    state = {
    zoom: 1.0,
    origin: { x: canvas.width / 2, y: canvas.height * 0.75 }, // origin point for starting point
    botLocation: { x: 0, y: 0 },
    botAngle: 0, // angle facing in degrees, 0 is up/forward/starting point, clockwise
    
    pointreadytojoin: false,
    lastpoint: { x: 0, y: 0 }, // point to join
    currentpoint: { x: 0, y: 0 }, // point to draw
    
    }
}



export function CalcDistance(distance, sensor) {
    let sensorData = botMeasurements.sensors[sensor];
    let botAngle = state.botAngle;

    // Calculate sensor's actual position on the bot (invert y for canvas)
    let botAngleRadians = botAngle * Math.PI / 180;
    let sensorX = state.botLocation.x + sensorData.x * Math.cos(botAngleRadians) - sensorData.y * Math.sin(botAngleRadians);
    let sensorY = state.botLocation.y - (sensorData.x * Math.sin(botAngleRadians) + sensorData.y * Math.cos(botAngleRadians));

    // Calculate detected point from sensor position (invert y for canvas)
    let angleRadians = (sensorData.angle + botAngle) * Math.PI / 180;
    let x = sensorX + distance * Math.sin(angleRadians);
    let y = sensorY - distance * Math.cos(angleRadians);

    // Round to 1 decimal place
    x = Math.round(x * 10) / 10;
    y = Math.round(y * 10) / 10;
    let point = { x: x, y: y };

    // Only add if not a duplicate (within 0.2 units of any existing point)
    let isDuplicate = points.some(p => Math.abs(p.x - x) < 0.2 && Math.abs(p.y - y) < 0.2);
    if (!isDuplicate) {
        points.push(point);
    }
}
export function addpoints(distanceReads) {
    for (let i = 0; i < Object.keys(botMeasurements.sensors).length; i++) {
        let sensor = Object.keys(botMeasurements.sensors)[i];
        let distance = distanceReads.payload[sensor];
        if (distance == null) { continue; }
        else {
            CalcDistance(distance, sensor);

        }

    }
    

}

export function clearCanvas() {
     ctx.clearRect(0, 0, canvas.width, canvas.height);
 }

 export function drawBot() {
     let screenX = state.origin.x + state.botLocation.x * state.scale;
     let screenY = state.origin.y - state.botLocation.y * state.scale;
     
     ctx.save();
     ctx.translate(screenX, screenY);
     ctx.rotate((state.botAngle || 0) * Math.PI / 180);
     
     // Draw bot body
     ctx.fillStyle = 'blue';
     ctx.fillRect(-botMeasurements.widthcm * state.scale / 2, -botMeasurements.heightcm * state.scale / 2, 
                  botMeasurements.widthcm * state.scale, botMeasurements.heightcm * state.scale);
     
     // Draw direction indicator
     ctx.fillStyle = 'red';
     ctx.fillRect(-2, -botMeasurements.heightcm * state.scale / 2 - 8, 4, 8);
     
     ctx.restore();
 }

 export function updateMap() {
     clearCanvas();
     
     // Draw points as dots
     ctx.fillStyle = 'red';
     for (let point of points) {
         let screenX = state.origin.x + point.x * state.scale;
         let screenY = state.origin.y - point.y * state.scale;
         ctx.beginPath();
         ctx.arc(screenX, screenY, 2, 0, 2 * Math.PI);
         ctx.fill();
     }
     
     drawBot();
 }