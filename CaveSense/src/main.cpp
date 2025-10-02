#include "CaveSense.h"
#include "pico/stdlib.h"
#include "tusb.h"
#include "distance_sensor.h"
int main() {
    CaveSense system;
    system.main(); // Never returns
    return 0;
}
int notmain() {
    stdio_init_all();
    DistanceSensor hcsr04{pio0, 0, 0};
    while (!tud_cdc_connected()) {
        tud_task();
        sleep_ms(100);
    }
    while (true) {
        // Trigger background sense
        hcsr04.TriggerRead();
        
        // wait for sensor to get a result
        while (hcsr04.is_sensing) {
            sleep_us(100);
        }

        // Read result
        printf("Reading %d centimeters\n", hcsr04.distance);
        sleep_ms(100);
    }
}