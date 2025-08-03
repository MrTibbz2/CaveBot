// Copyright (c) 2025 Lachlan McKenna (MrTibbz2)

// This source file is part of the CaveBot project, created for educational purposes.
// Unauthorized reuse or reproduction in other robotics competitions (including FLL 2025) 
// without written permission is strictly prohibited.
// Redistribution or adaptation is allowed for personal study only.

import * as vecmath from '../vecmath.js';

const canvas = document.getElementById('map');
const ctx = canvas.getContext('2d');

// Cartesian plane setup: (0,0) is center, X+ right, Y+ up
// Canvas Y+ is down, so we invert Y when drawing
export function toRadians(degrees) {
  return degrees * (Math.PI / 180);
}

// Cartesian: 0° is right (X+), 90° is up (Y+), 180° is left (X-), 270° is down (Y-)
export function getPointB(x, y, angleDegrees, distance) {
  const radians = toRadians(angleDegrees);
  // X increases right, Y increases up
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
        leftfront:  { x: 5,  y: 15,  angle: 90,  color: 'blue' },   // left front
        leftback:   { x: -5, y: 15,  angle: 90,  color: 'blue' },   // left back
        rightfront: { x: 5,  y: -15, angle: 270, color: 'orange' }, // right front
        rightback:  { x: -5, y: -15, angle: 270, color: 'orange' }, // right back
        frontleft:  { x: 15, y: 5,   angle: 0,   color: 'green' },  // front left
        frontright: { x: 15, y: -5,  angle: 0,   color: 'green' },  // front right
        backleft:   { x: -15, y: 5,  angle: 180, color: 'purple' }, // back left
        backright:  { x: -15, y: -5, angle: 180, color: 'purple' }  // back right
    }
};
export let state = {
    zoom: 1.0,
    scale: 0.5, // scaling for visual display
    origin: { x: canvas.width / 2, y: canvas.height / 2 }, // center of canvas is (0,0)
    botLocation: { x: 0, y: 0 },
    botAngle: 0,
    pointhasBeenjoined: false,
    lastpoint: { x: 0, y: 0 },
    currentpoint: { x: 0, y: 0 },
}
export let drawSensors = true; // Toggle to show/hide sensor lines

function ResetState() {
    state = {
        zoom: 1.0,
        origin: { x: canvas.width / 2, y: canvas.height / 2 },
        botLocation: { x: 0, y: 0 },
        botAngle: 0,
        pointreadytojoin: false,
        lastpoint: { x: 0, y: 0 },
        currentpoint: { x: 0, y: 0 },
    };
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
    if (botMeasurements.sensors[sensor] == null) {
        console.error(`Sensor ${sensor} not found in bot measurements.`);
        return null;
    }
    const sensorData = botMeasurements.sensors[sensor];
    // Rotate the sensor's offset by the bot's current angle (cartesian)
    const botAngleRad = toRadians(state.botAngle);
    const rotatedX = sensorData.x * Math.cos(botAngleRad) - sensorData.y * Math.sin(botAngleRad);
    const rotatedY = sensorData.x * Math.sin(botAngleRad) + sensorData.y * Math.cos(botAngleRad);
    // Normalize angle to [0, 360)
    let angle = (sensorData.angle + state.botAngle) % 360;
    if (angle < 0) angle += 360;
    // All coordinates are in cartesian (X+ right, Y+ up), no canvas transform here
    const sensorVec = {
        x: state.botLocation.x + rotatedX,
        y: state.botLocation.y + rotatedY,
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
    points.length = 0;
    for (let i = 0; i < Object.keys(botMeasurements.sensors).length; i++) {
        let sensor = Object.keys(botMeasurements.sensors)[i];
        let distance = distanceReads.payload[sensor];
        if (distance == null) { continue; }
        else {
            // Calculate point based on sensor and distance
            let point = await CalcPoint(distance, sensor);
            if (point.x !== NaN && point.y !== NaN) {
                points.push(point);
            } else {
                console.error(`Invalid point for sensor ${sensor}:`, point);
            }
        }
    }
}

export function clearCanvas() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
}

export function drawBot() {
    // Convert cartesian botLocation to canvas coordinates
    let screenX = state.origin.x + state.botLocation.x * state.scale;
    let screenY = state.origin.y - state.botLocation.y * state.scale; // invert Y for canvas

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

    // Draw sensors as small lines in their direction if enabled
    if (drawSensors) {
        ctx.lineWidth = 2;
        for (const key in botMeasurements.sensors) {
            const sensor = botMeasurements.sensors[key];
            // Sensor position in bot coordinates (cartesian)
            const sensorX = sensor.x * state.scale;
            const sensorY = -sensor.y * state.scale; // invert Y for canvas
            const sensorAngleRad = ((sensor.angle + state.botAngle) || 0) * Math.PI / 180;
            const lineLength = 4; // px
            const endX = sensorX + lineLength * Math.cos(sensorAngleRad);
            const endY = sensorY - lineLength * Math.sin(sensorAngleRad);
            ctx.strokeStyle = sensor.color || 'green';
            ctx.beginPath();
            ctx.moveTo(sensorX, sensorY);
            ctx.lineTo(endX, endY);
            ctx.stroke();
        }
    }

    ctx.restore();
}

export function updateMap() {
    clearCanvas();
    // Draw points as dots (centered like bot)
    ctx.fillStyle = 'red';
    for (let point of points) {
        let screenX = state.origin.x + point.x * state.scale;
        let screenY = state.origin.y - point.y * state.scale;
        ctx.beginPath();
        ctx.arc(screenX, screenY, 2, 0, 2 * Math.PI);
        ctx.fill();
    }
    // Draw bot
    drawBot();
}

