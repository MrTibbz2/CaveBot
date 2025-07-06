import * as vecmath from './vecmath.js';
import { bot, plotPoint } from './bot.js';

// this file took a HOT MINUTE so DONT TOUCH IT, i fucking mean it, and i fucking hate javascript. I WILL beat you up. - mrtibbz
// 
// total hours of my life I will never get back:      16.6

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

export function GetSensorVector(sensor) {
    console.log(`GetSensorVector called for sensor: ${sensor}`);
    console.log('bot.sensors:', bot.sensors);
    if (bot.sensors[sensor] == null) {
        console.error(`Sensor ${sensor} not found in bot measurements.`);
        return null;
    }
    const sensorData = bot.sensors[sensor];
    console.log('sensorData:', sensorData);
    console.log('bot.angle:', bot.angle);
    console.log('bot.pos:', bot.pos);
    
    // Rotate the sensor's offset by the bot's current angle (cartesian)
    const botAngleRad = toRadians(bot.angle || 0); // Use bot.angle if available, otherwise default to 0
    // Corrected rotation for clockwise angle (0=North)
    // Rotate the sensor's offset by the bot's current angle (clockwise)
    const rotatedX = sensorData.x * Math.cos(botAngleRad) + sensorData.y * Math.sin(botAngleRad);
    const rotatedY = -sensorData.x * Math.sin(botAngleRad) + sensorData.y * Math.cos(botAngleRad);
    // Normalize angle to [0, 360)
    let angle = (sensorData.angle + bot.angle) % 360;
    if (angle < 0) angle += 360;
    // All coordinates are in cartesian (X+ right, Y+ up), no canvas transform here
    const sensorVec = {
        x: bot.pos.x + rotatedX,
        y: bot.pos.y + rotatedY,
        angle: angle
    };
    console.log('Calculated sensorVec:', sensorVec);
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
    console.log('=== ADDPOINTS DEBUG ===')
    console.log('distanceReads:', distanceReads)
    console.log('bot object:', bot)
    console.log('bot.sensors:', bot.sensors)
    console.log('bot.pos:', bot.pos)
    console.log('bot.angle:', bot.angle)
    
    for (let i = 0; i < Object.keys(bot.sensors).length; i++) {
        let sensor = Object.keys(bot.sensors)[i];
        let distance = distanceReads.payload[sensor];
        console.log(`Sensor ${sensor}: distance=${distance}`);
        if (distance == null || distance === Infinity) { 
            console.log(`Skipping sensor ${sensor} - invalid distance`);
            continue; 
        }
        else {
            console.log(`Processing sensor ${sensor} with distance ${distance}`);
            // Calculate point based on sensor and distance
            let point = await CalcPoint(distance, sensor);
            console.log(`Calculated point for ${sensor}:`, point);
            if (point.x !== NaN && point.y !== NaN) {
                console.log(`Plotting point for ${sensor}:`, point);
                plotPoint(point);
            } else {
                console.error(`Invalid point for sensor ${sensor}:`, point);
            }
        }
    }
    console.log('=== END ADDPOINTS DEBUG ===')
}
