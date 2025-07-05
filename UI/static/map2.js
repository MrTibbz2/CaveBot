let calculator; // Declare in outer scope so it's accessible globally
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
