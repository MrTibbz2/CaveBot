// 2025 Lachlan McKenna. All rights reserved.


// I hope to god that we never may have to touch this again.
// you touch this, i will beat you up. - mrtibbs
// hours wasted here: 18. 


import { expressions } from './expr.js';
import { BotSiml } from './siml.js';
let calculator; // Declare in outer scope so it's accessible globally
function getExpressionById(id) {
  return window.calculator.getExpressions().find(expr => expr.id === id);
}


window.getExpressionById = getExpressionById; // Expose globally for debugging
// Expose globally for debugging
export let points = [];
window.calculator = calculator; // Assign to window for global access
requestAnimationFrame(() => {
    const calcElement = document.getElementById("calculator");

    window.calculator = Desmos.GraphingCalculator(calcElement, {
        keypad: false,
        expressions: true,
        settingsMenu: false,
        
    }); // assign to outer-scoped variable

    for (const expr of expressions) {
        // Add each expression to the calculator
        window.calculator.setExpression(expr);
    }
    
    // Initialize sensor helpers after calculator is ready
    window.SensorHelpers = {
        helper_frontleft: window.calculator.HelperExpression({ latex: 's_{1}' }),
        helper_frontright: window.calculator.HelperExpression({ latex: 's_{2}' }),
        helper_backleft: window.calculator.HelperExpression({ latex: 's_{3}' }),
        helper_backright: window.calculator.HelperExpression({ latex: 's_{4}' }),
        helper_leftfront: window.calculator.HelperExpression({ latex: 's_{6}' }),
        helper_leftback: window.calculator.HelperExpression({ latex: 's_{5}' }),
        helper_rightfront: window.calculator.HelperExpression({ latex: 's_{7}' }),
        helper_rightback: window.calculator.HelperExpression({ latex: 's_{8}' }),
    };
    window.BotHelpers = {
        helper_position: window.calculator.HelperExpression({ latex: '(N,M)' }),
        helper_angle: window.calculator.HelperExpression({ latex: 'R' }),
    }
    
    
});
// Automatically resize when window size changes
window.addEventListener("resize", () => {
    if (window.calculator) {
        // Resize container first
        const mapContainer = document.getElementById("map-container");
        const calcEl = document.getElementById("calculator");

        // Update width/height
        calcEl.style.width = mapContainer.clientWidth + "px";
        calcEl.style.height = mapContainer.clientHeight + "px";

        // Tell Desmos to recompute layout
        window.calculator.resize();
    }
});


export function getSensorLocation(sensorName) {
    const helper = window.SensorHelpers[`helper_${sensorName}`];
    if (!helper) {
        console.error(`Sensor helper for ${sensorName} not found.`);
        return null;
    }
    const value = helper.valueOf();
    if (value && value.listValue && value.listValue.length === 2) {
        return {
            x: value.listValue[0],
            y: value.listValue[1]
        };
    } else {
        console.error(`Invalid value for sensor ${sensorName}:`, value);
        return null;
    }

}
export function getBotPosition() {
    const helper = window.BotHelpers.helper_position;
    if (!helper) {
        console.error(`Bot position helper not found.`);
        return null;
    }
    const value = helper.valueOf();
    if (value && value.listValue && value.listValue.length === 2) {
        return {
            x: value.listValue[0],
            y: value.listValue[1]
        };
    } else {
        console.error(`Invalid value for bot position:`, value);
        return null;
    }

}
export function getBotAngle() {
    const helper = window.BotHelpers.helper_angle;
    if (!helper) {
        console.error(`Bot angle helper not found.`);
        return null;
    }
    const value = helper.valueOf();
    return value.numericValue;
}
window.getSensorLocation = getSensorLocation; // Expose globally for debugging


export let bot = {
    get pos() { return getBotPosition() || { x: 0, y: 0 }; },
    get angle() { return getBotAngle() || 0; },
    // width: 20, // Width in cm
    // height: 20, // Height in cm // these shouldnt be needed, use only sensor offsets.
    sensors: {
        leftfront: { x: -10, y: 5, angle: 270},
        leftback: { x: -10, y: -5, angle: 270},
        rightfront: { x: 10, y: 5, angle: 90},
        rightback: { x: 10, y: -5, angle: 90},
        frontleft: { x: -5, y: 10, angle: 0},
        frontright: { x: 5, y: 10, angle: 0},
        backleft: { x: -5, y: -10, angle: 180},
        backright: { x: 5, y: -10, angle: 180}
    },
    async move(distance) {
        // Calculate new position based on current angle
        // Robot convention: 0° = North, 90° = East
        // Convert to math convention: 90° = North, 0° = East
        const mathAngle = 90 - this.angle;
        const angleRad = toRadians(mathAngle);
        const deltaX = distance * Math.cos(angleRad);
        const deltaY = distance * Math.sin(angleRad);
        const currentPos = this.pos;
        const newX = currentPos.x + deltaX;
        const newY = currentPos.y + deltaY;
        // Update the bot's position in the calculator. ids are Y_position and X_position
        const xExpr = getExpressionById("X_Position");
        const yExpr = getExpressionById("Y_Position");
        xExpr.latex = `N=${newX.toFixed(5)}`;
        yExpr.latex = `M=${newY.toFixed(5)}`;
        window.calculator.setExpression(xExpr);
        window.calculator.setExpression(yExpr);
        

    },
    rotate(degrees) {
        let newAngle = this.angle + degrees;
        if (newAngle >= 360) {
            newAngle -= 360;
        }
        if (newAngle < 0) {
            newAngle += 360;
        }
        // Update the bot's angle in the calculator
        const angleExpr = getExpressionById("Angle");
        angleExpr.latex = `R=${newAngle}`;
        window.calculator.setExpression(angleExpr);
    },


}
window.bot = bot; // Expose globally for debugging

function toRadians(degrees) {
    return degrees * (Math.PI / 180);
}
export let pointctr = 0;
export function PlotPoint(point) {
    // Store the point in our array
    PlottedPoints.push({ x: point.x, y: point.y });
    
    // Create a point expression
    const pointExpr = {
        id: `plotted_point${pointctr++}`, // Unique ID for each point
        type: 'expression',
        latex: `(${point.x}, ${point.y})`,
        pointStyle: Desmos.Styles.POINT,
        color: Desmos.Colors.BLUE,
        pointSize: "12",
    };
    
    // Add the point to the calculator
    window.calculator.setExpression(pointExpr);
}

export function getPlottedPoints() {
    return [...PlottedPoints];
}
window.getPlottedPoints = getPlottedPoints;

export function GetSensorVector(sensor) {
    if (window.bot.sensors[sensor] == null) {
        console.error(`Sensor ${sensor} not found in bot measurements.`);
        return null;
    }
    const sensorData = window.bot.sensors[sensor];
    
    let angle = (sensorData.angle + window.bot.angle) % 360;
    if (angle < 0) angle += 360;
    // All coordinates are in cartesian (X+ right, Y+ up), no canvas transform here
    const sensorVec = {
        x: window.getSensorLocation(sensor).x,
        y: window.getSensorLocation(sensor).y,
        angle: angle
    };
    return sensorVec;
}
window.GetSensorVector = GetSensorVector; // Expose globally for debugging

export function getSensorReading(sensorName, distance) {
    const sensorVec = GetSensorVector(sensorName);
    if (!sensorVec) return null;
    
    // Convert angle to standard math convention (0° = East, counterclockwise)
    const mathAngle = 90 - sensorVec.angle;
    const angleRad = toRadians(mathAngle);
    
    // Project distance from sensor position in sensor direction
    const x = sensorVec.x + distance * Math.cos(angleRad);
    const y = sensorVec.y + distance * Math.sin(angleRad);
    
    return { x, y };
}

export function DebugPlotPoint(sensor, distance) {
    const point = getSensorReading(sensor, distance);
    if (point) {
        PlotPoint(point);
    }
}
window.DebugPlotPoint = DebugPlotPoint; // Expose globally for debugging

/* 
notes for today:

- desmos uses helper functions which you can get value of like: 
var L = calculator.HelperExpression({ latex: 'L' });
L.valueOf().listValue
*/
window.BotSiml = BotSiml; // Expose globally for debugging