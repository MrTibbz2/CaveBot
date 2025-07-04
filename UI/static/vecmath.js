
// Function to call the /pointcalc API and get the calculated position
export async function getPointCalc(angle, distance) {
    try {
        const response = await fetch(`/pointcalc?angle=${encodeURIComponent(angle)}&distance=${encodeURIComponent(distance)}`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        // data: { x_pos: ..., y_pos: ... }
        return data;
    } catch (error) {
        console.error('Error fetching pointcalc:', error);
        return null;
    }
}
