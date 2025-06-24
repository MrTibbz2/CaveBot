

const canvas = document.getElementById('map');
const ctx = canvas.getContext('2d');


export const botMeasurements = {
    heightcm: 20, // height of the bot in cm
    widthcm: 20,  // width of the bot in cm
    sensors: {
        // Front side (top edge, facing up, angle 0)
        frontLeft:  { x: -5,  y: -10, angle: 0 },   // left front sensor
        frontRight: { x:  5,  y: -10, angle: 0 },   // right front sensor
        // Right side (facing right, angle 90)
        rightFront: { x: 10,  y: -5,  angle: 90 },  // front right sensor
        rightBack:  { x: 10,  y:  5,  angle: 90 },  // back right sensor
        // Back side (bottom edge, facing down, angle 180)
        backRight:  { x:  5,  y: 10,  angle: 180 }, // right back sensor
        backLeft:   { x: -5,  y: 10,  angle: 180 }, // left back sensor
        // Left side (facing left, angle 270)
        leftBack:   { x: -10, y:  5,  angle: 270 }, // back left sensor
        leftFront:  { x: -10, y: -5,  angle: 270 }  // front left sensor
    }
};
export let state = {
    zoom: 1.0,
    origin: { x: canvas.width / 2, y: canvas.height * 0.75 }, // origin point for starting point
    botLocation: { x: 0, y: 0 },
    botAngle: 0, // angle facing in degrees, 0 is up/forward/starting point
    pointhasBeenjoined: false,
    lastpoint: { x: 0, y: 0 }, // point to join
    currentpoint: { x: 0, y: 0 }, // point to draw
    
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
export function updateMap(canvas, ctx, state) {
    

}


