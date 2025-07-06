import { expressions } from "./expr.js";
import * as vecmath from './vecmath.js';
import * as MapLib from './mapperlib.js';
let calculator; // Declare in outer scope so it's accessible globally
function getExpressionById(id) {
  return window.calculator.getExpressions().find(expr => expr.id === id);
}
export let points = [];
window.calculator = calculator; // Assign to window for global access
requestAnimationFrame(() => {
    const mapContainer = document.getElementById("map-container");

    const tempcalc = document.createElement("div");
    tempcalc.id = "calculator";
    tempcalc.style.width = mapContainer.clientWidth + "px";
    tempcalc.style.height = mapContainer.clientHeight + "px";
    tempcalc.style.boxSizing = "border-box";

    mapContainer.appendChild(tempcalc);

    window.calculator = Desmos.GraphingCalculator(tempcalc, {
        keypad: false,
        expressions: false,
        settingsMenu: false,
        
    }); // assign to outer-scoped variable

    for (const expr of expressions) {
        // Add each expression to the calculator
        window.calculator.setExpression(expr);
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

export let bot = {
    pos: { x: 0, y: 0 }, // Position in cm
    angle: 0, // Angle in degrees
    width: 20, // Width in cm
    height: 20, // Height in cm
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
        const offset = await vecmath.getPointCalc(this.angle, distance) 
        console.log(offset);
        this.pos.x += offset.x_pos;
        this.pos.y += offset.y_pos;
        // Update the bot's position in the calculator
        let botExpr = {
            x: getExpressionById("X_Position"),
            y: getExpressionById("Y_Position"),
            
        }
        botExpr.x.latex = `N=${this.pos.x}`;
        botExpr.y.latex = `M=${this.pos.y}`;
        window.calculator.setExpression(botExpr.x);
        window.calculator.setExpression(botExpr.y);
        // Update the bot's position expression


    },
    rotate(degrees) {
        this.angle += degrees;
        if (this.angle >= 360) {
            this.angle -= 360;
        }
        if (this.angle < 0) {
            this.angle += 360;
        }
        // Update the bot's angle in the calculator
        const angleExpr = getExpressionById("Angle");
        angleExpr.latex = `R=${this.angle}`;
        window.calculator.setExpression(angleExpr);
    },


}
export let pointctr = 0;
export function PlotPoint(point) {
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
