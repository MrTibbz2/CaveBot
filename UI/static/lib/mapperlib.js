import * as vecmath from './vecmath.js';
import * as Graph from './map.js';

// this file took a HOT MINUTE so DONT TOUCH IT, i fucking mean it, and i fucking hate javascript. I WILL beat you up. - mrtibbz
// 
// total hours of my life I will never get back:      18.1

export function toRadians(degrees) {
  return degrees * (Math.PI / 180);
}


export function getPointB(x, y, angleDegrees, distance) {
  const radians = toRadians(angleDegrees);
  // X increases right, Y increases up
  const newX = x + Math.cos(radians) * distance;
  const newY = y + Math.sin(radians) * distance;
  return { x: newX, y: newY };
}




// Utility: Recursively round all numbers in an object
export function roundObjectNumbers(obj, decimals = 2) {
    if (typeof obj === 'number') {
        return Number(obj.toFixed(decimals));
    }
    if (Array.isArray(obj)) {
        return obj.map(v => roundObjectNumbers(v, decimals));
    }
    if (typeof obj === 'object' && obj !== null) {
        const result = {};
        for (const key in obj) {
            result[key] = roundObjectNumbers(obj[key], decimals);
        }
        return result;
    }
    return obj;
}

export function GetSensorVector(sensor, bot) {
    if (Graph.bot.sensors[sensor] == null) {
        console.error(`Sensor ${sensor} not found in bot measurements.`);
        return null;
    }
    const sensorData = Graph.bot.sensors[sensor];
    // Rotate the sensor's offset by the bot's current angle (cartesian)
    const botAngleRad = toRadians(Graph.bot.angle || 0); // Use bot.angle if available, otherwise default to 0
    // Corrected rotation for clockwise angle (0=North)
    // Rotate the sensor's offset by the bot's current angle (clockwise)
    const rotatedX = sensorData.x * Math.cos(botAngleRad) + sensorData.y * Math.sin(botAngleRad);
    const rotatedY = -sensorData.x * Math.sin(botAngleRad) + sensorData.y * Math.cos(botAngleRad);
    // Normalize angle to [0, 360)
    let angle = (sensorData.angle + Graph.bot.angle) % 360;
    if (angle < 0) angle += 360;
    // All coordinates are in cartesian (X+ right, Y+ up), no canvas transform here
    const sensorVec = {
        x: Graph.bot.pos.x + rotatedX,
        y: Graph.bot.pos.y + rotatedY,
        angle: angle
    };
    return roundObjectNumbers(sensorVec, 2);
}
export async function CalcPoint(distance, sensor) {
    const sensorVector = GetSensorVector(sensor);
    if (!sensorVector || typeof sensorVector.angle !== 'number' || typeof sensorVector.x !== 'number' || typeof sensorVector.y !== 'number') {
        console.error('CalcPoint: Invalid sensorVector for', sensor, sensorVector);
        return { x: NaN, y: NaN };
    }
    const offsets = await vecmath.getPointCalc(sensorVector.angle, distance);
    if (!offsets || typeof offsets.x_pos !== 'number' || typeof offsets.y_pos !== 'number' || isNaN(offsets.x_pos) || isNaN(offsets.y_pos)) {
        console.error('CalcPoint: Invalid offsets from vecmath.getPointCalc:', offsets);
        return { x: NaN, y: NaN };
    }
    // All coordinates are in cartesian (X+ right, Y+ up), no canvas transform here
    const point = {
        x: sensorVector.x + offsets.x_pos,
        y: sensorVector.y + offsets.y_pos
    };
    return roundObjectNumbers(point, 2);
}
export async function addpoints(distanceReads) {
    // Clear points for each new scan to avoid clutter
    
    for (let i = 0; i < Object.keys(Graph.bot.sensors).length; i++) {
        let sensor = Object.keys(Graph.bot.sensors)[i];
        let distance = distanceReads.payload[sensor];
        if (distance == null) { continue; }
        else {
            // Calculate point based on sensor and distance
            let point = await CalcPoint(distance, sensor);
            if (point.x !== NaN && point.y !== NaN) {
                Graph.PlotPoint(point);
                
            } else {
                console.error(`Invalid point for sensor ${sensor}:`, point);
            }
        }
    }
}
