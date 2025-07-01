

const canvas = document.getElementById('map');
const ctx = canvas.getContext('2d');
export function toRadians(degrees) {
  return degrees * (Math.PI / 180);
}

export function getPointB(x, y, angleDegrees, distance) {
  // Use 0° as right (X+), 90° as up (Y+), 180° as left (X-), 270° as down (Y-)
  const radians = toRadians(angleDegrees);
  const newX = x + Math.cos(radians) * distance;
  const newY = y + Math.sin(radians) * distance;
  return { x: newX, y: newY };
}

export let points = [];
export const botMeasurements = {
    heightcm: 20, // height of the bot in cm
    widthcm: 20,  // width of the bot in cm
    // Match Python simulation: (0,0) is center, X+ right, Y+ up, angles: 0° right, 90° up, 180° left, 270° down
    // JS canvas: (0,0) is top-left, X+ right, Y+ down, but we keep bot (0,0) as center for math
    // Sensor config below matches Python's sensors_config
    sensors: {
        leftfront:  { x: 5,  y: 15,  angle: 90 },   // left front
        leftback:   { x: -5, y: 15,  angle: 90 },   // left back
        rightfront: { x: 5,  y: -15, angle: 270 },  // right front
        rightback:  { x: -5, y: -15, angle: 270 },  // right back
        frontleft:  { x: 15, y: 5,   angle: 0 },    // front left
        frontright: { x: 15, y: -5,  angle: 0 },    // front right
        backleft:   { x: -15, y: 5,  angle: 180 },  // back left
        backright:  { x: -15, y: -5, angle: 180 }   // back right
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


export function GetSensorVector(sensor) {
    if (botMeasurements.sensors[sensor] == null) {
        console.error(`Sensor ${sensor} not found in bot measurements.`);
        return null;
    }
    const sensorData = botMeasurements.sensors[sensor];
    // Rotate the sensor's offset by the bot's current angle
    const botAngleRad = toRadians(state.botAngle);
    const rotatedX = sensorData.x * Math.cos(botAngleRad) - sensorData.y * Math.sin(botAngleRad);
    const rotatedY = sensorData.x * Math.sin(botAngleRad) + sensorData.y * Math.cos(botAngleRad);
    // Normalize angle to [0, 360)
    let angle = (sensorData.angle + state.botAngle) % 360;
    if (angle < 0) angle += 360;
    const sensorVec = {
        x: state.botLocation.x + rotatedX,
        y: state.botLocation.y + rotatedY,
        angle: angle
    };
    return sensorVec;
}
export function CalcPoint(distance, sensor) {
    let sensorVec = GetSensorVector(sensor);
    if (sensorVec == null) {
        console.error(`Failed to get sensor vector for ${sensor}.`);
        return;

    }
    points.push(getPointB(sensorVec.x, sensorVec.y, sensorVec.angle, distance * state.scale));
}
export function addpoints(distanceReads) {
    // Clear points for each new scan to avoid clutter
    points.length = 0;
    for (let i = 0; i < Object.keys(botMeasurements.sensors).length; i++) {
        let sensor = Object.keys(botMeasurements.sensors)[i];
        let distance = distanceReads.payload[sensor];
        if (distance == null) { continue; }
        else {
            CalcPoint(distance, sensor);
        }
    }
}

export function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

export function drawBot() {
    let screenX = state.origin.x + state.botLocation.x * state.scale;
    let screenY = state.origin.y + state.botLocation.y * state.scale;

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