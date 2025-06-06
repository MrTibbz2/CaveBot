#include "pico/stdlib.h"

int main() {
    const int LED_PIN = PICO_DEFAULT_LED_PIN;  // usually GPIO 25

    gpio_init(LED_PIN);
    gpio_set_dir(LED_PIN, GPIO_OUT);

    while (true) {
        gpio_put(LED_PIN, 1);   // LED on
        sleep_ms(500);
        gpio_put(LED_PIN, 0);   // LED off
        sleep_ms(500);
    }

    return 0;
}